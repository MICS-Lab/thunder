import os
import json
import zipfile
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

from huggingface_hub import snapshot_download


CLASS_TO_ID = {
    "ADI": 0,
    "LYM": 1,
    "MUC": 2,
    "MUS": 3,
    "NCS": 4,
    "NOR": 5,
    "BLD": 6,
    "FCT": 7,
    "TUM": 8,
}

VALID_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp", ".webp"}


def download_starc9(root_folder: str) -> str:
    """
    Download the STARC-9 dataset from Hugging Face and extract all zip files.

    Final split mapping:
    - train: Training_data_normalized
    - val:   Validation_data/STANFORD-CRC-HE-VAL-SMALL
    - test:  Validation_data/STANFORD-CRC-HE-VAL-LARGE

    CURATED-TCGA is intentionally ignored here.
    """
    dataset_root = os.path.join(root_folder, "starc_9")

    snapshot_download(
        repo_id="Path2AI/STARC-9",
        repo_type="dataset",
        local_dir=dataset_root,
        local_dir_use_symlinks=False,
    )

    extract_all_zips(dataset_root)
    flatten_nested_class_dirs(dataset_root)
    return dataset_root


def extract_all_zips(root_dir: str) -> None:
    """
    Recursively extract every .zip under root_dir into a folder with the same stem.
    """
    for current_root, _, files in os.walk(root_dir):
        for file_name in files:
            if not file_name.lower().endswith(".zip"):
                continue

            zip_path = os.path.join(current_root, file_name)
            extract_dir = os.path.join(current_root, Path(file_name).stem)

            if os.path.exists(extract_dir) and any(Path(extract_dir).iterdir()):
                continue

            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)


def flatten_nested_class_dirs(root_dir: str) -> None:
    """
    Fix common extraction issue like:
        ADI/ADI/*.png
    into:
        ADI/*.png
    """
    for split_root, class_dirs in find_candidate_class_roots(root_dir):
        for class_name in class_dirs:
            class_dir = Path(split_root) / class_name
            nested_dir = class_dir / class_name
            if nested_dir.is_dir():
                for item in nested_dir.iterdir():
                    target = class_dir / item.name
                    if not target.exists():
                        item.rename(target)
                try:
                    nested_dir.rmdir()
                except OSError:
                    pass


def find_candidate_class_roots(root_dir: str) -> List[Tuple[str, List[str]]]:
    """
    Find directories that contain some/all class folders.
    """
    candidates = []
    expected = set(CLASS_TO_ID.keys())

    for current_root, dirnames, _ in os.walk(root_dir):
        present = sorted([d for d in dirnames if d in expected])
        if present:
            candidates.append((current_root, present))
    return candidates


def collect_images_from_class_root(class_root: str) -> Tuple[List[str], List[int], Dict[str, int]]:
    """
    Read all images from a directory structured like:
        class_root/
            ADI/
            LYM/
            ...
    """
    images: List[str] = []
    labels: List[int] = []
    class_counts: Dict[str, int] = defaultdict(int)

    class_root_path = Path(class_root)
    if not class_root_path.exists():
        raise FileNotFoundError(f"Class root does not exist: {class_root}")

    missing_classes = [c for c in CLASS_TO_ID if not (class_root_path / c).exists()]
    if missing_classes:
        raise FileNotFoundError(
            f"Missing expected class folders under {class_root}: {missing_classes}"
        )

    for class_name, class_id in CLASS_TO_ID.items():
        class_dir = class_root_path / class_name
        for img_path in sorted(class_dir.rglob("*")):
            if img_path.is_file() and img_path.suffix.lower() in VALID_EXTS:
                images.append(str(img_path.resolve()))
                labels.append(class_id)
                class_counts[class_name] += 1

    return images, labels, dict(class_counts)


def create_splits_starc9(base_folder: str) -> Dict:
    """
    Build train/val/test splits using only STANFORD validation sets.

    train = Training_data_normalized
    val   = Validation_data/STANFORD-CRC-HE-VAL-SMALL
    test  = Validation_data/STANFORD-CRC-HE-VAL-LARGE
    """
    dataset_root = os.path.join(base_folder, "starc_9")

    train_root = os.path.join(dataset_root, "Training_data_normalized")
    val_root = os.path.join(dataset_root, "Validation_data", "STANFORD-CRC-HE-VAL-SMALL")
    test_root = os.path.join(dataset_root, "Validation_data", "STANFORD-CRC-HE-VAL-LARGE")

    train_images, train_labels, train_counts = collect_images_from_class_root(train_root)
    val_images, val_labels, val_counts = collect_images_from_class_root(val_root)
    test_images, test_labels, test_counts = collect_images_from_class_root(test_root)

    splits = {
        "train": {"images": train_images, "labels": train_labels},
        "val": {"images": val_images, "labels": val_labels},
        "test": {"images": test_images, "labels": test_labels},
        "meta": {
            "dataset_name": "STARC_9",
            "class_to_id": CLASS_TO_ID,
            "num_classes": len(CLASS_TO_ID),
            "counts": {
                "train": {
                    "total": len(train_images),
                    "per_class": train_counts,
                },
                "val": {
                    "total": len(val_images),
                    "per_class": val_counts,
                },
                "test": {
                    "total": len(test_images),
                    "per_class": test_counts,
                },
            },
            "notes": [
                "CURATED-TCGA-CRC-HE-20K-NORMALIZED is intentionally excluded.",
                "Validation uses STANFORD-CRC-HE-VAL-SMALL only.",
                "Test uses STANFORD-CRC-HE-VAL-LARGE only.",
            ],
        },
    }

    os.makedirs(os.path.join(base_folder, "data_splits"), exist_ok=True)
    out_json = os.path.join(base_folder, "data_splits", "starc_9.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(splits, f, indent=2)

    print("\nSaved split file to:", out_json)
    print("\nSample counts")
    print("Train:", len(train_images))
    print("Val  :", len(val_images))
    print("Test :", len(test_images))

    print("\nPer-class counts")
    print("Train:", train_counts)
    print("Val  :", val_counts)
    print("Test :", test_counts)

    return splits


def main():
    """
    Edit this path before running.
    """
    base_folder = "./datasets"

    print("Downloading STARC-9...")
    dataset_root = download_starc9(base_folder)
    print("Downloaded to:", dataset_root)

    print("\nCreating splits...")
    create_splits_starc9(base_folder)

    print("\nDone.")


if __name__ == "__main__":
    main()
from typing import Dict, List, Tuple

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


def download_starc9(root_folder: str) -> None:
    """
    Download the STARC-9 dataset from Hugging Face and extract all zip files.

    Final split mapping:
    - train: Training_data_normalized
    - val:   Validation_data/STANFORD-CRC-HE-VAL-SMALL
    - test:  Validation_data/STANFORD-CRC-HE-VAL-LARGE

    CURATED-TCGA is intentionally ignored here.
    """
    from huggingface_hub import snapshot_download

    snapshot_download(
        repo_id="Path2AI/STARC-9",
        repo_type="dataset",
        local_dir=root_folder,
        local_dir_use_symlinks=False,
    )

    extract_all_zips(root_folder)


def extract_all_zips(root_dir: str) -> None:
    """
    Recursively extract every .zip under root_dir into a folder with the same stem.
    """
    import os
    from pathlib import Path

    from ..utils import unzip_file

    for current_root, _, files in os.walk(root_dir):
        for file_name in files:
            if not file_name.lower().endswith(".zip"):
                continue

            unzip_file(
                os.path.join(current_root, file_name),
                current_root,
            )

            # Renaming folder extracted from STANFORD-CRC-HE-VAL-LARGE-NORMALIZED.zip
            if file_name == "STANFORD-CRC-HE-VAL-LARGE-NORMALIZED.zip":
                os.rename(
                    os.path.join(current_root, "NORMALIZED"),
                    os.path.join(current_root, "STANFORD-CRC-HE-VAL-LARGE"),
                )


def collect_images_from_class_root(
    class_root: str,
) -> Tuple[List[str], List[int], Dict[str, int]]:
    """
    Read all images from a directory structured like:
        class_root/
            ADI/
            LYM/
            ...
    """
    from pathlib import Path

    images: List[str] = []
    labels: List[int] = []

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

    return images, labels


def create_splits_starc9(base_folder: str, dataset_cfg: dict) -> None:
    """
    Generating data splits for the STARC-9 dataset.

    :param base_folder: path to the main folder storing datasets.
    :param dataset_cfg: dataset-specific config.
    """
    import os

    from ...utils.constants import UtilsConstants
    from ...utils.utils import set_seed
    from ..data_splits import (
        check_dataset,
        create_few_shot_training_data,
        init_dict,
        save_dict,
    )

    # Setting the random seed
    set_seed(UtilsConstants.DEFAULT_SEED.value)

    # Initializing dict
    starc9_data_splits = init_dict()

    # Getting folder paths
    dataset_root = os.path.join(base_folder, "starc9")
    train_root = os.path.join(dataset_root, "Training_data_normalized")
    val_root = os.path.join(
        dataset_root,
        "Validation_data",
        "STANFORD-CRC-HE-VAL-SMALL",
    )
    test_root = os.path.join(
        dataset_root,
        "Validation_data",
        "STANFORD-CRC-HE-VAL-LARGE",
    )

    # Collecting data
    train_images, train_labels = collect_images_from_class_root(train_root)
    val_images, val_labels = collect_images_from_class_root(val_root)
    test_images, test_labels = collect_images_from_class_root(test_root)

    # Updating dict
    starc9_data_splits["train"]["images"] = train_images
    starc9_data_splits["train"]["labels"] = train_labels
    starc9_data_splits["val"]["images"] = val_images
    starc9_data_splits["val"]["labels"] = val_labels
    starc9_data_splits["test"]["images"] = test_images
    starc9_data_splits["test"]["labels"] = test_labels

    # Few-shot training data
    starc9_data_splits = create_few_shot_training_data(starc9_data_splits)

    # Checking dataset characteristics
    check_dataset(
        starc9_data_splits,
        dataset_cfg,
        base_folder,
    )

    # Saving dict
    save_dict(
        starc9_data_splits, os.path.join(base_folder, "data_splits", "starc9.json")
    )

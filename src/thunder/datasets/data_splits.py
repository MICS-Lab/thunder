import logging
import os
import random
from collections import defaultdict
from collections.abc import Callable
from pathlib import Path
from typing import List, Union


def generate_splits(datasets: Union[List[str], str]) -> None:
    """Generates the data splits for all datasets in input list.

    This function requires the `$THUNDER_BASE_DATA_FOLDER` environment variable to be set,
    which indicates the base directory where the datasets will be downloaded.

    Args:
        datasets (List[str]): List of dataset names to generate splits for or one of the following aliases: `all`, `classification`, `segmentation`.
    """

    if isinstance(datasets, str):
        datasets = [datasets]

    if len(datasets) == 1:
        if datasets[0] == "all":
            datasets = [
                "bach",
                "bracs",
                "break_his",
                "ccrcc",
                "crc",
                "esca",
                "patch_camelyon",
                "tcga_crc_msi",
                "tcga_tils",
                "tcga_uniform",
                "wilds",
                "ocelot",
                "pannuke",
                "segpath_epithelial",
                "segpath_lymphocytes",
                "mhist",
                "spider_breast",
                "spider_colorectal",
                "spider_skin",
                "spider_thorax",
            ]
        elif datasets[0] == "classification":
            datasets = [
                "bach",
                "bracs",
                "break_his",
                "ccrcc",
                "crc",
                "esca",
                "patch_camelyon",
                "tcga_crc_msi",
                "tcga_tils",
                "tcga_uniform",
                "wilds",
                "mhist",
                "spider_breast",
                "spider_colorectal",
                "spider_skin",
                "spider_thorax",
            ]
        elif datasets[0] == "segmentation":
            datasets = [
                "ocelot",
                "pannuke",
                "segpath_epithelial",
                "segpath_lymphocytes",
            ]

    base_folder = os.path.join(os.environ["THUNDER_BASE_DATA_FOLDER"], "datasets")
    data_splits_folder = os.path.join(base_folder, "data_splits")
    os.makedirs(data_splits_folder, exist_ok=True)

    # Generating data splits
    for dataset_name in datasets:
        generate_splits_for_dataset(dataset_name)


def generate_splits_for_dataset(dataset_name: str) -> None:
    """Generates the data splits for a specific dataset.

    Args:
        dataset_name (str): The name of the dataset to generate splits for.
    """
    from omegaconf import OmegaConf

    from ..utils.constants import DatasetConstants
    from .dataset import (create_splits_bach, create_splits_bracs,
                          create_splits_break_his, create_splits_ccrcc,
                          create_splits_crc, create_splits_esca,
                          create_splits_mhist, create_splits_ocelot,
                          create_splits_pannuke, create_splits_patch_camelyon,
                          create_splits_segpath_epithelial,
                          create_splits_segpath_lymphocytes,
                          create_splits_tcga_crc_msi, create_splits_tcga_tils,
                          create_splits_tcga_uniform, create_splits_wilds, 
                          create_splits_spider_breast, create_splits_spider_colorectal,
                          create_splits_spider_skin, create_splits_spider_thorax)

    DATASET_TO_FUNCTION = {
        # Classification
        "bach": create_splits_bach,
        "bracs": create_splits_bracs,
        "break_his": create_splits_break_his,
        "ccrcc": create_splits_ccrcc,
        "crc": create_splits_crc,
        "esca": create_splits_esca,
        "mhist": create_splits_mhist,
        "patch_camelyon": create_splits_patch_camelyon,
        "tcga_crc_msi": create_splits_tcga_crc_msi,
        "tcga_tils": create_splits_tcga_tils,
        "tcga_uniform": create_splits_tcga_uniform,
        "wilds": create_splits_wilds,
        "spider_breast": create_splits_spider_breast,
        "spider_colorectal": create_splits_spider_colorectal,
        "spider_skin": create_splits_spider_skin,
        "spider_thorax": create_splits_spider_thorax,
        # Segmentation
        "ocelot": create_splits_ocelot,
        "pannuke": create_splits_pannuke,
        "segpath_epithelial": create_splits_segpath_epithelial,
        "segpath_lymphocytes": create_splits_segpath_lymphocytes,
    }

    assert (
        dataset_name in DatasetConstants.DATASETS.value
    ), f"{dataset_name} is not within the list of available datasets: {DatasetConstants.DATASETS.value}."

    generate_data_splits(
        base_folder=os.path.join(os.environ["THUNDER_BASE_DATA_FOLDER"], "datasets"),
        dataset_name=dataset_name,
        dataset_yaml=f"{Path(__file__).parent.parent}/config/dataset/{dataset_name}.yaml",
        split_function=DATASET_TO_FUNCTION[dataset_name],
    )


def sorted_listdir(path: str) -> list:
    """
    Listing files in a directory and sorting them deterministically.

    :param path: path to the directory.
    :return: sorted list of files.
    """
    return sorted(os.listdir(path))


def compute_patches(
    im_filepath: str,
    mask_filepath: str,
    im_height: int,
    im_width: int,
    patch_height: int = 256,
    patch_width: int = 256,
) -> tuple[list, list]:
    """
    Computing patches for segmentation datasets.

    :param im_filepath: path to the image.
    :param mask_filepath: path to the mask.
    :param im_height: image height.
    :param im_width: image width.
    :param patch_height: patch height.
    :param patch_width: patch width.
    :return: lists of patch indices for images and masks (labels).
    """
    import numpy as np

    def get_linspace_vals(im_size, patch_size):
        nb_ticks = im_size // patch_size - 1
        values = np.linspace(0, nb_ticks * patch_size, nb_ticks + 1)
        return values

    # Getting linspace values
    x_values = get_linspace_vals(im_width, patch_width)
    y_values = get_linspace_vals(im_height, patch_height)

    # Meshgrid and conversion to positions
    xx, yy = np.meshgrid(x_values, y_values)
    positions = np.column_stack([xx.ravel(), yy.ravel()])

    images = [
        (im_filepath, int(x), int(x + patch_width), int(y), int(y + patch_height))
        for (x, y) in positions
    ]
    labels = [
        (mask_filepath, int(x), int(x + patch_width), int(y), int(y + patch_height))
        for (x, y) in positions
    ]

    return images, labels


def check_dataset(
    data_splits: dict,
    dataset_cfg: dict,
    base_folder: str,
) -> None:
    """
    Checking dataset characteristics.

    :param data_splits: data splits dictionary.
    :param dataset_cfg: dataset-specific config.
    :param base_folder: path to the main folder storing datasets.
    """
    from PIL import Image

    # Checking split sizes
    for split, nb_samples in [
        ("train", dataset_cfg.nb_train_samples),
        ("val", dataset_cfg.nb_val_samples),
        ("test", dataset_cfg.nb_test_samples),
    ]:
        images = data_splits[split]["images"]
        labels = data_splits[split]["labels"]
        assert (
            len(images) == len(labels) == nb_samples
        ), f"Got {len(images)} {split} images and {len(labels)} {split} labels, but expecting {nb_samples} {split} samples for {dataset_cfg['dataset_name']}."

    # Checking image resolution
    if "image_sizes" in dataset_cfg.keys():
        train_im_sample = data_splits["train"]["images"][0]
        if type(train_im_sample) == tuple:
            train_im_sample = train_im_sample[0]
        sample_image = Image.open(
            os.path.join(base_folder, dataset_cfg.dataset_name, train_im_sample)
        ).convert("RGB")
        assert (
            list(sample_image.size) in dataset_cfg.image_sizes
        ), f"Image size {list(sample_image.size)} is not within the list of expected sizes: {dataset_cfg.image_sizes}."

    check_dataset_md5(data_splits, dataset_cfg)


def check_dataset_md5(data_splits: dict, dataset_cfg: dict) -> None:
    """
    Checking the MD5sum of the generated split dictionnary against the expected MD5sum.
    Code for computing MD5 taken from https://stackoverflow.com/questions/5417949/computing-an-md5-hash-of-a-data-structure

    :param data_splits: data splits dictionary.
    :param dataset_cfg: dataset-specific config.
    """
    import hashlib
    import json

    if hasattr(dataset_cfg, "md5sum"):
        expected_md5 = dataset_cfg["md5sum"]
        computed_md5 = hashlib.md5(
            json.dumps(data_splits, sort_keys=True).encode("utf-8")
        ).hexdigest()
        assert (
            expected_md5 == computed_md5
        ), f"MD5 computed for the data split for the {dataset_cfg['dataset_name']} dataset did not match the expected MD5."


def create_few_shot_training_data(
    data_splits: dict,
    nb_sets_per_nb_shot: int = 1000,
):
    """
    Creating few-shot training data.

    :param data_splits: data splits dictionary.
    :param nb_sets_per_nb_shot: number of data sets to create for each number of shots.
    """
    # Creating lebel2 image dict
    train_images, train_labels = (
        data_splits["train"]["images"],
        data_splits["train"]["labels"],
    )
    label2images = defaultdict(list)
    for i in range(len(train_labels)):
        label2images[train_labels[i]].append(i)

    # Sampling data sets (images + labels) for each number of shots
    for nb_shots in data_splits["train_few_shot"].keys():
        for _ in range(nb_sets_per_nb_shot):
            few_shot_images = []
            few_shot_labels = []
            for label in label2images.keys():
                rd_images = random.sample(label2images[label], int(nb_shots))
                few_shot_images.extend(rd_images)
                few_shot_labels.extend([label for _ in range(int(nb_shots))])

            data_splits["train_few_shot"][nb_shots]["images"].append(few_shot_images)
            data_splits["train_few_shot"][nb_shots]["labels"].append(few_shot_labels)

    return data_splits


def generate_data_splits(
    base_folder: str, dataset_name: str, dataset_yaml: str, split_function: Callable
) -> None:
    """
    Generating data splits for a specific dataset.

    :param base_folder: path to the main folder storing datasets.
    :param dataset_name: name of the dataset.
    :param dataset_yaml: path to the dataset yaml config file.
    :param split_function: function to run to generate the data splits.
    """
    from omegaconf import OmegaConf

    dataset_folder = os.path.join(base_folder, dataset_name)
    if os.path.exists(dataset_folder):
        dataset_cfg = OmegaConf.load(dataset_yaml)
        split_function(base_folder, dataset_cfg)
        logging.info(f"Generated data split for {dataset_folder}.")


def get_data_from_set(dataset_folder: str, set_name: str, dataset_cfg: dict) -> list:
    """
    Retrieving images and labels for a specific set.

    :param dataset_folder: path to the main folder storing data.
    :param set_name: name of the specific set.
    :param dataset_cfg: dataset-specific config.

    :return lists of images and labels for the set.
    """
    folder = os.path.join(dataset_folder, set_name)
    images = []
    labels = []
    for subfolder in dataset_cfg.classes:
        curr_folder = os.path.join(folder, subfolder)
        curr_images = sorted_listdir(curr_folder)
        curr_images = [os.path.join(set_name, subfolder, s) for s in curr_images]
        images.extend(curr_images)
        labels.extend([dataset_cfg.class_to_id[subfolder]] * len(curr_images))
    return images, labels


def get_data_from_folder_recursive(dataset_folder: str, set_name: str, dataset_cfg: dict) -> list:
    """
    Retrieving images and labels from a folder recursively.

    use this for spider datasets : folder -> class subfolder -> wsi subfolder -> images
    """
    images = []
    labels = []
    folder = os.path.join(dataset_folder, set_name)

    for subfolder in dataset_cfg.classes:
        curr_folder = os.path.join(folder, subfolder)
        curr_images = []
        for root, _, files in os.walk(curr_folder):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    rel_dir = os.path.relpath(root, dataset_folder)
                    rel_file = os.path.join(rel_dir, file)
                    curr_images.append(rel_file)
        curr_images = sorted(curr_images)
        images.extend(curr_images)
        labels.extend([dataset_cfg.class_to_id[subfolder]] * len(curr_images))
    return images, labels


def init_dict() -> None:
    """
    Initializing data split dictionary.

    :return: init dictionary.
    """

    return {
        "train": {
            "images": [],
            "labels": [],
        },
        "val": {
            "images": [],
            "labels": [],
        },
        "test": {
            "images": [],
            "labels": [],
        },
        "train_few_shot": {
            "1": {
                "images": [],
                "labels": [],
            },
            "2": {
                "images": [],
                "labels": [],
            },
            "4": {
                "images": [],
                "labels": [],
            },
            "8": {
                "images": [],
                "labels": [],
            },
            "16": {
                "images": [],
                "labels": [],
            },
        },
    }


def save_dict(d: str, path: str) -> None:
    """
    Saving dictionary as json file.

    :param d: dict to save.
    :param path: path to json file.
    """
    import json

    with open(path, "w") as outfile:
        json.dump(d, outfile)

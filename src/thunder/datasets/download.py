import logging
import os
from pathlib import Path
from typing import List, Union

from .data_splits import generate_splits
from .dataset import *


def download_datasets(datasets: Union[List[str], str], make_splits: bool = False):
    """Downloads the benchmark datasets specified in the list of dataset names.

    This function requires the `$THUNDER_BASE_DATA_FOLDER` environment variable to be set,
    which indicates the base directory where the datasets will be downloaded.

    The list of all available datasets:
        * bach
        * bracs
        * break_his
        * ccrcc
        * crc
        * esca
        * mhist
        * ocelot
        * pannuke
        * patch_camelyon
        * segpath_epithelial
        * segpath_lymphocytes
        * tcga_crc_msi
        * tcga_tils
        * tcga_uniform
        * wilds

    Args:
        datasets (List[str] or str): A dataset name string or a List of dataset names to download or one of the following aliases: `all`, `classification`, `segmentation`.
        make_splits (bool): Whether to generate data splits for the datasets. Defaults to False.
    """
    if "THUNDER_BASE_DATA_FOLDER" not in os.environ:
        raise EnvironmentError(
            "Please set base data directory of thunder using `export THUNDER_BASE_DATA_FOLDER=/base/data/directory`"
        )

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
            ]
        elif datasets[0] == "segmentation":
            datasets = [
                "ocelot",
                "pannuke",
                "segpath_epithelial",
                "segpath_lymphocytes",
            ]

    for dataset in datasets:
        download_dataset(dataset)
        if make_splits:
            generate_splits([dataset])


def download_dataset(dataset: str):
    root_folder = os.path.join(
        os.environ["THUNDER_BASE_DATA_FOLDER"], f"datasets/{dataset}"
    )

    # if folder exists do not download again
    if os.path.exists(root_folder):
        logging.info(
            f"Folder {dataset} already exists in {root_folder}, skipping download."
        )
        return

    Path(root_folder).mkdir(parents=True, exist_ok=True)

    if dataset == "ccrcc":
        download_ccrcc(root_folder)
    elif dataset == "crc":
        download_crc(root_folder)
    elif dataset == "bach":
        download_bach(root_folder)
    elif dataset == "esca":
        download_esca(root_folder)
    elif dataset == "break_his":
        download_break_his(root_folder)
    elif dataset == "patch_camelyon":
        download_patch_camelyon(root_folder)
    elif dataset == "tcga_crc_msi":
        download_tcga_crc_msi(root_folder)
    elif dataset == "tcga_tils":
        download_tcga_tils(root_folder)
    elif dataset == "tcga_uniform":
        download_tcga_uniform(root_folder)
    elif dataset == "wilds":
        download_wilds(root_folder)
    elif dataset == "ocelot":
        download_ocelot(root_folder)
    elif dataset == "pannuke":
        download_pannuke(root_folder)
    elif dataset == "segpath_epithelial":
        download_segpath_epithelial(root_folder)
    elif dataset == "segpath_lymphocytes":
        download_segpath_lymphocytes(root_folder)
    elif dataset == "mhist":
        download_mhist(root_folder)
    elif dataset == "bracs":
        download_bracs(root_folder)
    elif dataset == "spider_breast":
        download_spider_breast(root_folder)
    elif dataset == "spider_colorectal":
        download_spider_colorectal(root_folder)
    elif dataset == "spider_skin":
        download_spider_skin(root_folder)
    elif dataset == "spider_thorax":
        download_spider_thorax(root_folder)
    else:
        raise ValueError(f"Dataset {dataset} is not supported.")

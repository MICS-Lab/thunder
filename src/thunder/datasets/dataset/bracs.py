def download_bracs(root_folder: str):
    import subprocess

    # Define the wget command
    command = [
        "wget",
        "--no-parent",
        "-nH",
        "-r",
        "--directory-prefix",
        f"{root_folder}",
        f"ftp://utente_reader:ICAR-CNR@histoimage.na.icar.cnr.it/BRACS_RoI/",
    ]
    # Execute the command
    try:
        subprocess.run(command, check=True)
    except:
        raise RuntimeError("wget is needed to download the bracs dataset.")


def create_splits_bracs(base_folder: str, dataset_cfg: dict) -> None:
    """
    Generating data splits for the BRACS dataset.

    :param base_folder: path to the main folder storing datasets.
    :param dataset_cfg: dataset-specific config.
    """
    import os

    from ...utils.constants import UtilsConstants
    from ...utils.utils import set_seed
    from ..data_splits import (
        check_dataset,
        create_few_shot_training_data,
        get_data_from_set,
        init_dict,
        save_dict,
    )

    # Setting the random seed
    set_seed(UtilsConstants.DEFAULT_SEED.value)

    # Initializing dict
    bracs_data_splits = init_dict()

    # Retrieving all images and labels
    bracs_folder = os.path.join(base_folder, "bracs", "BRACS_RoI", "latest_version")
    for data_split in ["train", "val", "test"]:
        images, labels = get_data_from_set(bracs_folder, data_split, dataset_cfg)
        images, labels = zip(
            *[
                (os.path.join("BRACS_RoI", "latest_version", im), lab)
                for im, lab in zip(images, labels)
                if ".png" in im
            ]
        )
        bracs_data_splits[data_split]["images"].extend(images)
        bracs_data_splits[data_split]["labels"].extend(labels)

    # Few-shot training data
    bracs_data_splits = create_few_shot_training_data(bracs_data_splits)

    # Checking dataset characteristics
    check_dataset(
        bracs_data_splits,
        dataset_cfg,
        base_folder,
    )

    # Saving dict
    save_dict(bracs_data_splits, os.path.join(base_folder, "data_splits", "bracs.json"))

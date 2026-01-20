import os


def download_from_url(url: str, filename: str):
    import requests
    import tqdm

    # User-Agent header is required by some servers (e.g., Zenodo) to allow downloads
    headers = {"User-Agent": "thunder-bench (https://github.com/MICS-Lab/thunder)"}
    with open(filename, "wb") as f:
        with requests.get(url, stream=True, headers=headers) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))

            # tqdm has many interesting parameters. Feel free to experiment!
            tqdm_params = {
                "desc": url,
                "total": total,
                "miniters": 1,
                "unit": "B",
                "unit_scale": True,
                "unit_divisor": 1024,
            }
            with tqdm.tqdm(**tqdm_params) as pb:
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)


def unzip_file(file_path: str, extract_dir: str):
    import zipfile

    # unzip "$1"
    # rm $1
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    os.remove(file_path)


def untar_file(file_path: str, extract_dir: str):
    import tarfile

    # tar -xvf "$1"
    # rm $1
    with tarfile.open(file_path, "r:*") as tar:
        tar.extractall(path=extract_dir)

    os.remove(file_path)


def ungzip_file(file_path: str, extract_dir: str):
    import gzip
    import shutil

    with gzip.open(file_path, "rb") as f_in:
        with open(extract_dir, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    os.remove(file_path)


def remove_symlinks(directory: str):
    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            path = os.path.join(root, name)
            if os.path.islink(path):
                os.unlink(path)


def is_dataset_available(dataset_name: str) -> bool:
    """Check if the dataset is available in the datasets directory.

    Args:
        dataset_name (str): The name of the dataset to check.

    Returns:
        bool: True if the dataset is available, False otherwise.
    """
    datasets_dir = os.path.join(os.environ["THUNDER_BASE_DATA_FOLDER"], "datasets/")
    return os.path.exists(os.path.join(datasets_dir, dataset_name))

def _has_internet(timeout: float = 3.0) -> bool:
    # Inspired from https://github.com/mahmoodlab/TRIDENT/blob/ba52a930da19d7f43586223dcc2ebfbca2271fc3/trident/IO.py
    import os
    import socket

    endpoint = os.environ.get("HF_ENDPOINT", "huggingface.co")
    if endpoint.startswith(("http://", "https://")):
        from urllib.parse import urlparse

        endpoint = urlparse(endpoint).netloc

    try:
        with socket.create_connection((endpoint, 443), timeout=timeout):
            return True
    except OSError:
        pass

    try:
        import requests

        url = f"https://{endpoint}"
        return requests.head(url, timeout=timeout).status_code < 500
    except Exception:
        return False


def _configure_outdated_checks() -> None:
    import warnings

    warnings.filterwarnings("ignore", message=r".*pkg_resources is deprecated.*")

    if _has_internet():
        return

    import os

    os.environ.setdefault("OUTDATED_IGNORE", "1")
    try:
        import outdated.utils

        outdated.utils.get_url = lambda *args, **kwargs: None
    except Exception:
        pass
    try:
        import outdated

        outdated.check_outdated = lambda *args, **kwargs: (False, None)
        outdated.warn_if_outdated = lambda *args, **kwargs: None
    except Exception:
        pass


_configure_outdated_checks()

from .benchmark import benchmark
from .datasets import download_datasets, generate_splits
from .models import download_models
from .utils import gather_results

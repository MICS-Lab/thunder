import logging
import os
from pathlib import Path
from typing import List, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Models
# Importantly, you will have to visit the Huggingface URL of all models to accept
# usage conditions to be able to download their associated checkpoints.
TAGS_FILENAMES = {
    "uni": (
        "MahmoodLab/uni",
        "pytorch_model.bin",
    ),  # UNI (https://huggingface.co/MahmoodLab/UNI)
    "uni2h": (
        "MahmoodLab/UNI2-h",
        "pytorch_model.bin",
    ),  # UNI2-h (https://huggingface.co/MahmoodLab/UNI2-h)
    "virchow": (
        "paige-ai/Virchow",
        "pytorch_model.bin",
    ),  # Virchow (https://huggingface.co/paige-ai/Virchow)
    "virchow2": (
        "paige-ai/Virchow2",
        "pytorch_model.bin",
    ),  # Virchow2 (https://huggingface.co/paige-ai/Virchow2)
    "hoptimus0": (
        "bioptimus/H-optimus-0",
        "pytorch_model.bin",
    ),  # H-optimus 0 (https://huggingface.co/bioptimus/H-optimus-0)
    "hoptimus1": (
        "bioptimus/H-optimus-1",
        "pytorch_model.bin",
    ),  # H-optimus 1 (https://huggingface.co/bioptimus/H-optimus-1)
    "conch": (
        "MahmoodLab/conch",
        "pytorch_model.bin",
    ),  # CONCH (https://huggingface.co/MahmoodLab/CONCH)
    "titan": (
        "MahmoodLab/TITAN",
        "model.safetensors",
    ),  # TITAN/CONCHv1.5 (https://huggingface.co/MahmoodLab/TITAN)
    "phikon": (
        "owkin/phikon",
        "model.safetensors",
    ),  # Phikon (https://huggingface.co/owkin/phikon)
    "phikon2": (
        "owkin/phikon-v2",
        "model.safetensors",
    ),  # Phikon2 (https://huggingface.co/owkin/phikon-v2)
    "hiboub": (
        "histai/hibou-b",
        "model.safetensors",
    ),  # Hibou-b (https://huggingface.co/histai/hibou-b)
    "hiboul": (
        "histai/hibou-L",
        "model.safetensors",
    ),  # Hibou-L (https://huggingface.co/histai/hibou-L)
    "midnight": (
        "kaiko-ai/midnight",
        "model.safetensors",
    ),  # Midnight-12k (https://huggingface.co/kaiko-ai/midnight)
    "keep": (
        "Astaxanthin/KEEP",
        "model.safetensors",
    ),  # KEEP (https://huggingface.co/Astaxanthin/KEEP)
    "quiltnetb32": (
        "wisdomik/QuiltNet-B-32",
        "pytorch_model.bin",
    ),  # QuiltNet-B-32 (https://huggingface.co/wisdomik/QuiltNet-B-32)
    "plip": (
        "vinid/plip",
        "pytorch_model.bin",
    ),  # PLIP (https://huggingface.co/vinid/plip)
    "musk": (
        "xiangjx/musk",
        "model.safetensors",
    ),  # MUSK (https://huggingface.co/xiangjx/musk)
    "dinov2base": (
        "facebook/dinov2-base",
        "model.safetensors",
    ),  # DINOv2-B (https://huggingface.co/facebook/dinov2-base)
    "dinov2large": (
        "facebook/dinov2-large",
        "model.safetensors",
    ),  # DINOv2-L (https://huggingface.co/facebook/dinov2-large)
    "vitbasepatch16224in21k": (
        "google/vit-base-patch16-224-in21k",
        "model.safetensors",
    ),  # ViT-B (https://huggingface.co/google/vit-base-patch16-224-in21k)
    "vitlargepatch16224in21k": (
        "google/vit-large-patch16-224-in21k",
        "model.safetensors",
    ),  # ViT-L (https://huggingface.co/google/vit-large-patch16-224-in21k)
    "clipvitbasepatch32": (
        "openai/clip-vit-base-patch32",
        "pytorch_model.bin",
    ),  # CLIP-B (https://huggingface.co/openai/clip-vit-base-patch32)
    "clipvitlargepatch14": (
        "openai/clip-vit-large-patch14",
        "model.safetensors",
    ),  # CLIP-L (https://huggingface.co/openai/clip-vit-large-patch14)
    "dinov3vits16pretrainlvd1689m": (
        "facebook/dinov3-vits16-pretrain-lvd1689m",
        "model.safetensors",
    ),  # DINOv3-S (https://huggingface.co/facebook/dinov3-vits16-pretrain-lvd1689m)
    "dinov3vitb16pretrainlvd1689m": (
        "facebook/dinov3-vitb16-pretrain-lvd1689m",
        "model.safetensors",
    ),  # DINOv3-B (https://huggingface.co/facebook/dinov3-vitb16-pretrain-lvd1689m)
    "dinov3vitl16pretrainlvd1689m": (
        "facebook/dinov3-vitl16-pretrain-lvd1689m",
        "model.safetensors",
    ),  # DINOv3-L (https://huggingface.co/facebook/dinov3-vitl16-pretrain-lvd1689m)
}


def download_models(models: Union[List[str], str]) -> None:
    """Download model checkpoints from Hugging Face.

    The list of all available models:
        * uni
        * uni2h
        * virchow
        * virchow2
        * hoptimus0
        * hoptimus1
        * conch
        * titan
        * phikon
        * phikon2
        * hiboub
        * hiboul
        * midnight
        * keep
        * quiltb32
        * plip
        * musk
        * dinov2base
        * dinov2large
        * dinov3vits16pretrainlvd1689m
        * dinov3vitb16pretrainlvd1689m
        * dinov3vitl16pretrainlvd1689m
        * vitbasepatch16224in21k
        * vitlargepatch16224in21k
        * clipvitbasepatch32
        * clipvitlargepatch14

    Args:
        models (List[str] or str): a list of model names or single a model name str.
    """
    if isinstance(models, str):
        models = [models]

    for model in models:
        if model not in TAGS_FILENAMES:
            raise ValueError(f"Model {model} is not available.")
        download_model(model)


def download_model(model: str) -> None:
    from huggingface_hub import hf_hub_download

    base_dir = os.path.join(os.environ["THUNDER_BASE_DATA_FOLDER"], "pretrained_ckpts")
    tag, filename = TAGS_FILENAMES[model]
    local_dir_tag = tag.split("/")[-1].replace("-v2", "2").replace("-", "").lower()
    local_dir = os.path.join(base_dir, local_dir_tag)

    os.makedirs(local_dir, exist_ok=True)
    if any(Path(local_dir).iterdir()):
        logging.info(f"Model {model} already exists in {local_dir}. Skipping download.")
        return

    try:
        logging.info(f"Downloading {filename} from {tag} to {local_dir}...")
        hf_hub_download(
            tag, filename=filename, local_dir=local_dir, force_download=True
        )

        if filename == "model.safetensors" or (
            filename == "pytorch_model.bin"
            and local_dir_tag
            in ["clipvitbasepatch32", "clipvitlargepatch14", "quiltnetb32", "plip"]
        ):
            if local_dir_tag == "keep":
                extra_files = [
                    "config.json",
                    "modeling_keep.py",
                    "tokenizer_config.json",
                    "vocab.txt",
                ]
            elif local_dir_tag == "musk":
                extra_files = []
            elif local_dir_tag in [
                "clipvitbasepatch32",
                "clipvitlargepatch14",
                "plip",
                "quiltnetb32",
            ]:
                extra_files = [
                    "config.json",
                    "preprocessor_config.json",
                    "special_tokens_map.json",
                    "tokenizer_config.json",
                    "tokenizer.json",
                ]
                if local_dir_tag != "plip":
                    extra_files.extend(["merges.txt", "vocab.json"])
            elif local_dir_tag == "midnight":
                extra_files = ["config.json"]
            elif local_dir_tag == "titan":
                extra_files = [
                    "text_transformer.py",
                    "conch_tokenizer.py",
                    "vision_transformer.py",
                    "conch_v1_5.py",
                    "tokenizer_config.json",
                    "tokenizer.json",
                    "special_tokens_map.json",
                    "conch_v1_5_pytorch_model.bin",
                ]

            else:
                extra_files = ["config.json", "preprocessor_config.json"]
            for extra_file in extra_files:
                hf_hub_download(
                    tag, filename=extra_file, local_dir=local_dir, force_download=True
                )

        if local_dir_tag == "musk":
            import subprocess

            # Define the wget command
            command = [
                "wget",
                "https://github.com/lilab-stanford/MUSK/raw/main/musk/models/tokenizer.spm",
                "--directory-prefix",
                f"{local_dir}",
            ]
            # Execute the command
            try:
                subprocess.run(command, check=True)
            except:
                raise RuntimeError(
                    "wget is needed to download MUSK tokenizer config file."
                )

        logging.info(f"Successfully downloaded {filename} from {tag}.")

    except Exception as e:
        import traceback

        logging.error(f"Failed to download {filename} from {tag}. Error: {e}")
        traceback.print_exc()

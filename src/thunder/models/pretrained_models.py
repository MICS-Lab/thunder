from abc import ABC, abstractmethod
from omegaconf import DictConfig, OmegaConf
import timm
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
import torch
from transformers import AutoImageProcessor, AutoModel

from ..utils.constants import ModelConstants


class PretrainedModel(torch.nn.Module, ABC):
    """Abstract class to be inherited by custom pretrained models."""

    @abstractmethod
    def get_transform(self):
        """Returns the transform function to be applied to the input images."""
        pass

    @abstractmethod
    def get_linear_probing_embeddings(self, x):
        """Returns the embeddings for linear probing."""
        pass

    @abstractmethod
    def get_segmentation_embeddings(self, x):
        """Returns the pixel dense embeddings for segmentation."""
        pass

    def get_embeddings(self, x, model, task_type):
        if task_type == "linear_probing":
            return self.get_linear_probing_embeddings(x)
        elif task_type == "segmentation":
            return self.get_segmentation_embeddings(x)
        else:
            raise ValueError(f"Invalid task type {task_type}")


def load_pretrained_model(cfg: DictConfig, adaptation_type: str, device: str):
    """
    Loading pretrained model.

    :param cfg: config defining the job to run.
    :param adaptation_type: type of adaptation (frozen, lora)
    :param device: device to use (cpu, cuda).
    """

    if cfg.pretrained_model.type == "python_script":
        import sys
        import importlib

        spec = importlib.util.spec_from_file_location(
            "custom_model", cfg.pretrained_model.python_script
        )
        module = importlib.util.module_from_spec(spec)
        sys.modules["custom_model"] = module
        spec.loader.exec_module(module)

        # if kwargs are not available in the config do not pass them
        if "kwargs" in cfg.pretrained_model:
            kwargs = cfg.pretrained_model.kwargs
        else:
            kwargs = {}
        pretrained_model, transform, extract_embedding = getattr(module, "get_model")(
            kwargs
        )
    else:
        pretrained_model, transform, extract_embedding = get_model(
            cfg.pretrained_model, device
        )
    pretrained_model = pretrained_model.to(device)
    if adaptation_type == "lora":
        # Train mode
        pretrained_model.train()
    else:
        # Eval model
        pretrained_model.eval()
        # Not requiring gradients
    for param in pretrained_model.parameters():
        param.requires_grad = False

    return pretrained_model, transform, extract_embedding


def get_model(model_cfg: dict, device: str):
    """
    Loading pretrained model.

    :param model_cfg: model config.
    :param device: device to use (cpu, cuda).
    """

    assert model_cfg.model_name in ModelConstants.PRETRAINED_MODELS.value, print(
        f"{model_cfg.model_name} is not within the list of available pretrained models: {ModelConstants.PRETRAINED_MODELS.value}."
    )

    if model_cfg.type == "timm":
        timm_kwargs = OmegaConf.to_container(model_cfg.timm_kwargs, resolve=True)
        if "mlp_layer" in timm_kwargs.keys():
            assert timm_kwargs["mlp_layer"] == "SwiGLUPacked"
            timm_kwargs["mlp_layer"] = timm.layers.SwiGLUPacked
        if "act_layer" in timm_kwargs.keys():
            assert timm_kwargs["act_layer"] == "SiLU"
            timm_kwargs["act_layer"] = torch.nn.SiLU

        if model_cfg.model_name == "musk":
            model, transform = get_musk(model_cfg.ckpt_path)
        else:
            model, transform = get_from_timm(
                model_cfg.hf_tag, timm_kwargs, model_cfg.ckpt_path, device
            )
    elif model_cfg.type == "safetensors":
        if model_cfg.model_name == "keep":
            model, transform = get_keep(model_cfg.ckpt_path)
        elif model_cfg.model_name == "titan":
            model, transform = get_titan(model_cfg.ckpt_path)
        elif model_cfg.model_name == "midnight":
            model, transform = get_midnight(model_cfg.ckpt_path)
        else:
            model, transform = get_from_safetensors(model_cfg.ckpt_path)
    elif model_cfg.type == "open_clip":
        model, transform = get_from_open_clip(model_cfg.ckpt_path)
    else:
        raise ValueError(f"Unkown model type {model_cfg.type} specified in yaml file.")

    if model_cfg.model_name == "conch":

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            if task_type == "linear_probing":
                emb = pretrained_model.encode_image(
                    src, proj_contrast=False, normalize=False
                )
            else:
                _, emb = pretrained_model._encode_image(src, normalize=False)
            return emb

    elif model_cfg.model_name == "keep":

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            if task_type == "linear_probing":
                emb = pretrained_model.encode_image(src)
            else:
                emb = pretrained_model.visual.forward_features(src)[:, 1:]
            return emb

    elif model_cfg.model_name == "musk":

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            if task_type == "linear_probing":
                emb = pretrained_model(
                    image=src,
                    with_head=False,
                    out_norm=False,
                    ms_aug=True,
                    return_global=True,
                )[
                    0
                ]  # keeping only vision_cls
            else:
                emb = pretrained_model.beit3(visual_tokens=src)["encoder_out"][:, 1:]

            return emb

    elif model_cfg.model_name in [
        "clipvitbasepatch32",
        "clipvitlargepatch14",
        "plip",
        "quiltnetb32",
    ]:

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            if task_type == "linear_probing":
                emb = pretrained_model.get_image_features(src)
            else:
                emb = pretrained_model.vision_model(src).last_hidden_state[:, 1:]
            return emb

    elif model_cfg.model_name in [
        "phikon",
        "phikon2",
        "dinov2base",
        "dinov2large",
        "vitbasepatch16224in21k",
        "vitlargepatch16224in21k",
    ]:

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            out = pretrained_model(src)
            if task_type == "linear_probing":
                emb = out.last_hidden_state[:, 0, :]
            else:
                emb = out.last_hidden_state[:, 1:]
            return emb

    elif model_cfg.model_name in ["hiboub", "hiboul"]:

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            out = pretrained_model(src)
            if task_type == "linear_probing":
                emb = out.pooler_output
            else:
                emb = out.last_hidden_state[:, 1:]
            return emb

    elif model_cfg.model_name in ["virchow", "virchow2"]:

        def extract_embedding(src, pretrained_model, task_type):
            out = pretrained_model(src)
            class_token = out[:, 0]
            if model_cfg.model_name == "virchow":
                patch_tokens = out[:, 1:]
            elif model_cfg.model_name == "virchow2":
                patch_tokens = out[
                    :, 5:
                ]  # tokens 1-4 are register tokens so we ignore them.
            if task_type != "segmentation":
                emb = torch.cat([class_token, patch_tokens.mean(1)], dim=-1)
                return emb
            else:
                return patch_tokens

    elif model_cfg.model_name == "midnight":

        def extract_embedding(src, pretrained_model, task_type):
            out = pretrained_model(src).last_hidden_state
            class_token = out[:, 0]
            patch_tokens = out[:, 1:]
            if task_type != "segmentation":
                emb = torch.cat([class_token, patch_tokens.mean(1)], dim=-1)
                return emb
            else:
                return patch_tokens

    else:

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            if task_type == "linear_probing":
                emb = pretrained_model(src)
            else:
                if model_cfg.model_name == "titan":
                    emb = pretrained_model.trunk(src, return_all_tokens=True)[:, 1:]
                else:
                    emb = pretrained_model.forward_features(src)[:, 1:]

                    if model_cfg.model_name == "uni2h":
                        nb_reg = 8
                    elif model_cfg.model_name in ["hoptimus0", "hoptimus1"]:
                        nb_reg = 4
                    else:
                        nb_reg = 0

                    emb = emb[:, nb_reg:]  # ignoring register tokens.

            return emb

    return model, transform, extract_embedding


def get_from_timm(hf_tag: str, timm_kwargs: dict, ckpt_path: str, device: str):
    """
    Adapted from:
    - https://huggingface.co/MahmoodLab/UNI
    - https://huggingface.co/MahmoodLab/UNI2-h
    - https://huggingface.co/bioptimus/H-optimus-0

    :param hf_tag: Huggingface model tag.
    :param timm_kargs: dictionary of timm arguments.
    :ckpt_path: path to the stored checkpoint.
    :param device: device to use (cpu, cuda).
    """

    # Model
    model = timm.create_model(hf_tag, pretrained=False, **timm_kwargs)
    model.load_state_dict(
        torch.load(ckpt_path, weights_only=True, map_location=torch.device(device)),
        strict=True,
    )

    # Transform
    transform = create_transform(
        **resolve_data_config(model.pretrained_cfg, model=model)
    )

    return model, transform


def get_from_open_clip(ckpt_path: str):
    """
    Adapted from https://huggingface.co/MahmoodLab/CONCH

    :param ckpt_path: path to the stored checkpoint.
    """
    from conch.open_clip_custom import create_model_from_pretrained

    model, transform = create_model_from_pretrained("conch_ViT-B-16", ckpt_path)

    return model, transform


def get_from_safetensors(ckpt_path: str):
    """
    Adapted from:
    - https://huggingface.co/owkin/phikon
    - https://huggingface.co/owkin/phikon-v2
    - https://huggingface.co/histai/hibou-b
    - https://huggingface.co/histai/hibou-L

    :param ckpt_path: path to the stored checkpoint.
    """
    # Model
    model = AutoModel.from_pretrained(ckpt_path)

    # Transform
    processor = AutoImageProcessor.from_pretrained(ckpt_path, use_fast=False)

    def transform(im):
        return processor(im, return_tensors="pt")["pixel_values"].squeeze(0)

    return model, transform


def get_keep(ckpt_path: str):
    """
    Adapted from:
    - https://huggingface.co/Astaxanthin/KEEP

    :param ckpt_path: path to the stored checkpoint.
    """
    from torchvision import transforms

    # Model
    model = AutoModel.from_pretrained(ckpt_path, trust_remote_code=True)

    # Transform
    transform = transforms.Compose(
        [
            transforms.Resize(
                size=224, interpolation=transforms.InterpolationMode.BICUBIC
            ),
            transforms.CenterCrop(size=(224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )

    return model, transform


def get_musk(ckpt_path: str):
    """
    Adapted from:
    - https://huggingface.co/xiangjx/musk

    :ckpt_path: path to the stored checkpoint.
    """
    from musk import utils, modeling
    from timm.data.constants import IMAGENET_INCEPTION_MEAN, IMAGENET_INCEPTION_STD
    from torchvision import transforms

    # Model
    model = timm.models.create_model("musk_large_patch16_384")
    utils.load_model_and_may_interpolate(ckpt_path, model, "model|module", "")

    # Transform
    transform = transforms.Compose(
        [
            transforms.Resize(384, interpolation=3, antialias=True),
            transforms.CenterCrop((384, 384)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=IMAGENET_INCEPTION_MEAN, std=IMAGENET_INCEPTION_STD
            ),
        ]
    )

    return model, transform


def get_midnight(ckpt_path: str):
    """
    Adapted from:
    - https://huggingface.co/kaiko-ai/midnight

    :param ckpt_path: path to the stored checkpoint.
    """
    from torchvision import transforms

    # Model
    model = AutoModel.from_pretrained(ckpt_path)

    # Transform
    transform = transforms.Compose(
        [
            transforms.Resize(224),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
        ]
    )

    return model, transform


def get_titan(ckpt_path: str):
    """
    Adapted from:
    - https://github.com/mahmoodlab/CLAM/blob/f1e93945d5f5ac6ed077cb020ed01cf984780a77/models/builder.py#L57-L66

    :param ckpt_path: path to the stored checkpoint.
    """

    # Model
    titan = AutoModel.from_pretrained("MahmoodLab/TITAN", trust_remote_code=True)
    model, transform = titan.return_conch()

    return model, transform

from abc import ABC, abstractmethod
from pathlib import Path

import timm
import torch
from omegaconf import DictConfig, OmegaConf
from timm.data import resolve_data_config
from timm.data.transforms_factory import create_transform
from transformers import AutoImageProcessor, AutoModel, AutoTokenizer

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
        import importlib
        import sys

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

    assert (
        model_cfg.model_name in ModelConstants.PRETRAINED_MODELS.value
    ), f"{model_cfg.model_name} is not within the list of available pretrained models: {ModelConstants.PRETRAINED_MODELS.value}."

    if model_cfg.type == "timm":
        timm_kwargs = OmegaConf.to_container(model_cfg.timm_kwargs, resolve=True)
        if "mlp_layer" in timm_kwargs.keys():
            assert timm_kwargs["mlp_layer"] == "SwiGLUPacked"
            timm_kwargs["mlp_layer"] = timm.layers.SwiGLUPacked
        if "act_layer" in timm_kwargs.keys():
            assert timm_kwargs["act_layer"] == "SiLU"
            timm_kwargs["act_layer"] = torch.nn.SiLU

        if model_cfg.model_name == "musk":
            model, transform, tokenizer = get_musk(model_cfg.ckpt_path)
        elif model_cfg.model_name == "provgigapath":
            model, transform = get_prov_gigapath(
                model_cfg.hf_tag, model_cfg.ckpt_path, device
            )
        elif "kaiko_vit" in model_cfg.model_name:
            model, transform = get_kaiko(
                model_cfg.timm_tag, timm_kwargs, model_cfg.ckpt_path, device
            )
        else:
            model, transform = get_from_timm(
                model_cfg.hf_tag, timm_kwargs, model_cfg.ckpt_path, device
            )
    elif model_cfg.type == "safetensors":
        if model_cfg.model_name == "keep":
            model, transform, tokenizer = get_keep(model_cfg.ckpt_path)
        elif model_cfg.model_name == "titan":
            model, transform = get_titan(model_cfg.ckpt_path)
        elif model_cfg.model_name == "midnight":
            model, transform = get_midnight(model_cfg.ckpt_path)
        elif model_cfg.model_name == "genbio-pathfm":
            model, transform = get_genbio_pathfm(model_cfg.ckpt_path)
        else:
            model, transform, tokenizer = get_from_safetensors(
                model_cfg.ckpt_path, use_fast="dinov3" in model_cfg.model_name
            )
    elif model_cfg.type == "open_clip":
        model, transform, tokenizer = get_from_open_clip(model_cfg.ckpt_path)
    elif model_cfg.type == "torch_hub":
        model, transform = get_openmidnight(model_cfg.ckpt_path)
    else:
        raise ValueError(f"Unknown model type {model_cfg.type} specified in yaml file.")

    if model_cfg.model_name == "conch":

        def extract_embedding(
            src,
            pretrained_model,
            task_type="linear_probing",
            text_aligned_im_emb=False,
            text_emb=False,
            tokenizer=tokenizer,
            device=device,
        ):
            if task_type == "linear_probing":
                if not text_aligned_im_emb and not text_emb:
                    emb = pretrained_model.encode_image(
                        src, proj_contrast=False, normalize=False
                    )
                else:
                    if not text_emb:
                        emb = pretrained_model.encode_image(
                            src, proj_contrast=True, normalize=True
                        )
                    else:
                        from conch.open_clip_custom import tokenize

                        tokenized_prompts = tokenize(tokenizer, src).to(device)
                        emb = pretrained_model.encode_text(tokenized_prompts)
            else:
                emb = pretrained_model.visual.trunk(
                    src, **pretrained_model.visual.trunk_kwargs
                )[:, 1:]
            return emb

    elif model_cfg.model_name == "keep":

        def extract_embedding(
            src,
            pretrained_model,
            task_type="linear_probing",
            text_aligned_im_emb=False,
            text_emb=False,
            tokenizer=tokenizer,
            device=device,
        ):
            if task_type == "linear_probing":
                if not text_emb:
                    emb = pretrained_model.encode_image(src)
                else:
                    tokenized_prompts = tokenizer(
                        src,
                        max_length=256,
                        padding="max_length",
                        truncation=True,
                        return_tensors="pt",
                    ).to(device)
                    emb = model.encode_text(tokenized_prompts)
            else:
                emb = pretrained_model.visual.forward_features(src)[:, 1:]
            return emb

    elif model_cfg.model_name == "musk":

        def extract_embedding(
            src,
            pretrained_model,
            task_type="linear_probing",
            text_aligned_im_emb=False,
            text_emb=False,
            tokenizer=tokenizer,
            device=device,
        ):
            if task_type == "linear_probing":
                if not text_aligned_im_emb and not text_emb:
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
                    if not text_emb:
                        emb = pretrained_model(
                            image=src,
                            with_head=True,
                            out_norm=True,
                            ms_aug=False,
                            return_global=True,
                        )[
                            0
                        ]  # keeping only vision_cls
                    else:
                        from musk import utils

                        text_ids = []
                        paddings = []
                        for txt in src:
                            txt_ids, pad = utils.xlm_tokenizer(
                                txt, tokenizer, max_len=100
                            )
                            text_ids.append(torch.tensor(txt_ids).unsqueeze(0))
                            paddings.append(torch.tensor(pad).unsqueeze(0))
                        text_ids = torch.cat(text_ids)
                        paddings = torch.cat(paddings)

                        emb = model(
                            text_description=text_ids.to(device),
                            padding_mask=paddings.to(device),
                            with_head=True,
                            out_norm=True,
                            ms_aug=False,
                            return_global=True,
                        )[
                            1
                        ]  # keeping only text_cls
            else:
                emb = pretrained_model.beit3(visual_tokens=src)["encoder_out"][:, 1:]

            return emb

    elif model_cfg.model_name in [
        "clipvitbasepatch32",
        "clipvitlargepatch14",
        "plip",
        "quiltnetb32",
    ]:

        def extract_embedding(
            src,
            pretrained_model,
            task_type="linear_probing",
            text_aligned_im_emb=False,
            text_emb=False,
            tokenizer=tokenizer,
            device=device,
        ):
            if task_type == "linear_probing":
                if not text_emb:
                    emb = pretrained_model.get_image_features(src)
                else:
                    tokenized_prompts = tokenizer(
                        src, padding=True, return_tensors="pt"
                    ).to(device)
                    emb = model.get_text_features(**tokenized_prompts)
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

    elif model_cfg.model_name in [
        "hiboub",
        "hiboul",
        "dinov3vits16pretrainlvd1689m",
        "dinov3vitb16pretrainlvd1689m",
        "dinov3vitl16pretrainlvd1689m",
    ]:

        def extract_embedding(src, pretrained_model, task_type="linear_probing"):
            out = pretrained_model(src)
            if task_type == "linear_probing":
                emb = out.pooler_output
            else:
                emb = out.last_hidden_state[:, 1:]
                if "dinov3" in model_cfg.model_name:
                    nb_reg = 4
                else:
                    nb_reg = 0
                emb = emb[:, nb_reg:]  # ignoring register tokens.

            return emb

    elif model_cfg.model_name in ["h0mini", "virchow", "virchow2"]:

        def extract_embedding(src, pretrained_model, task_type):
            out = pretrained_model(src)
            class_token = out[:, 0]
            if model_cfg.model_name == "virchow":
                patch_tokens = out[:, 1:]
            elif model_cfg.model_name == "virchow2":
                patch_tokens = out[
                    :, 5:
                ]  # tokens 1-4 are register tokens so we ignore them.
            elif model_cfg.model_name == "h0mini":
                patch_tokens = out[:, pretrained_model.num_prefix_tokens :]
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
                elif model_cfg.model_name == "openmidnight":
                    emb = pretrained_model.get_intermediate_layers(src)[0]
                elif model_cfg.model_name == "genbio-pathfm":
                    emb = pretrained_model.forward_with_patches(src)[1]
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


def get_model_from_name(model_name: str, device: str):
    """Loading pretrained model from input name.

    The list of all available models:
        * uni
        * uni2h
        * virchow
        * virchow2
        * hoptimus0
        * h0mini
        * hoptimus1
        * genbio-pathfm
        * provgigapath
        * conch
        * titan
        * phikon
        * phikon2
        * hiboub
        * hiboul
        * midnight
        * openmidnight
        * kaiko_vits8
        * kaiko_vits16
        * kaiko_vitb8
        * kaiko_vitb16
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
        model_name (str): The name of the model to use.
        device (str): Device to use (cpu, cuda).

    Returns:
        model (torch.nn.Module): Pytorch model instance.
        transform (torchvision.transforms.transforms.Compose): Transform to apply to input image.
        get_embeddings (Callable): Function to extract embeddings.

    Tip: output function `get_embeddings` signature.
        * src (torch.Tensor): Batch of transformed images with shape (B, 3, H, W).
        * pretrained_model (torch.nn.Module): Model to extract embeddings with.
        * pooled_emb (bool):  Whether to output pooled (True) or spatial (False) embeddings.
    """

    # Loading model config
    yaml_file = (
        f"{Path(__file__).parent.parent}/config/pretrained_model/{model_name}.yaml"
    )
    model_cfg = OmegaConf.load(yaml_file)

    # Getting model, transform, embedding extraction function
    model, transform, extract_embedding = get_model(model_cfg, device)

    # Defining wrapper function to get embeddings
    def get_embeddings(src, pretrained_model, pooled_emb=True):
        return extract_embedding(
            src,
            pretrained_model,
            task_type="linear_probing" if pooled_emb else "segmentation",
        )

    return model, transform, get_embeddings


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
    try:
        from conch.open_clip_custom import create_model_from_pretrained, get_tokenizer
    except ImportError:
        raise ImportError(
            "In order to use CONCH, please run the following: 'pip install git+https://github.com/Mahmoodlab/CONCH.git'"
        )

    # Model and transform
    model, transform = create_model_from_pretrained("conch_ViT-B-16", ckpt_path)

    # Tokenizer
    tokenizer = get_tokenizer()

    return model, transform, tokenizer


def get_from_safetensors(ckpt_path: str, use_fast: str = False):
    """
    Adapted from:
    - https://huggingface.co/owkin/phikon
    - https://huggingface.co/owkin/phikon-v2
    - https://huggingface.co/histai/hibou-b
    - https://huggingface.co/histai/hibou-L

    :param ckpt_path: path to the stored checkpoint.
    :param use_fast: whether to use fast image processor.
    """
    # Model
    model = AutoModel.from_pretrained(ckpt_path)

    # Transform
    processor = AutoImageProcessor.from_pretrained(ckpt_path, use_fast=use_fast)

    def transform(im):
        return processor(im, return_tensors="pt")["pixel_values"].squeeze(0)

    # Tokenizer
    if (
        "clipvitbasepatch32" in ckpt_path
        or "clipvitlargepatch14" in ckpt_path
        or "plip" in ckpt_path
        or "quiltnetb32" in ckpt_path
    ):
        tokenizer = AutoTokenizer.from_pretrained(ckpt_path)
    else:
        tokenizer = None

    return model, transform, tokenizer


def get_kaiko(timm_tag: str, timm_kwargs: dict, ckpt_path: str, device: str):
    """
    Adapted from:
    - https://github.com/kaiko-ai/towards_large_pathology_fms

    :param timm_tag: timm model tag.
    :param timm_kargs: dictionary of timm arguments.
    :param ckpt_path: path to the stored checkpoint.
    :param device: device to use (cpu, cuda).
    """
    from torchvision.transforms import v2

    # Model
    model = timm.create_model(
        timm_tag,
        pretrained=False,
        **timm_kwargs,
    )
    model.load_state_dict(
        torch.load(ckpt_path, weights_only=True, map_location=torch.device(device)),
        strict=True,
    )

    # Transform
    transform = v2.Compose(
        [
            v2.ToImage(),
            v2.Resize(size=224),
            v2.CenterCrop(size=224),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(
                mean=(0.5, 0.5, 0.5),
                std=(0.5, 0.5, 0.5),
            ),
        ]
    )

    return model, transform


def get_prov_gigapath(hf_tag: str, ckpt_path: str, device: str):
    """
    Adapted from:
    - https://huggingface.co/prov-gigapath/prov-gigapath

    Loads the Prov-GigaPath timm model from Hugging Face Hub.
    """
    from torchvision import transforms

    model = timm.create_model(
        hf_tag,
        pretrained=False,
    )

    model.load_state_dict(
        torch.load(ckpt_path, weights_only=True, map_location=torch.device(device)),
        strict=True,
    )

    # Transform
    transform = transforms.Compose(
        [
            transforms.Resize(256, interpolation=transforms.InterpolationMode.BICUBIC),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225),
            ),
        ]
    )

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

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(ckpt_path, trust_remote_code=True)

    return model, transform, tokenizer


def get_musk(ckpt_path: str):
    """
    Adapted from:
    - https://huggingface.co/xiangjx/musk

    :ckpt_path: path to the stored checkpoint.
    """
    try:
        from musk import modeling, utils
    except ImportError:
        raise ImportError(
            "In order to use MUSK, please run the following: 'pip install git+https://github.com/lilab-stanford/MUSK.git'"
        )
    import os

    from timm.data.constants import IMAGENET_INCEPTION_MEAN, IMAGENET_INCEPTION_STD
    from torchvision import transforms
    from transformers import XLMRobertaTokenizer

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

    # Tokenizer
    tokenizer = XLMRobertaTokenizer(
        ckpt_path.replace("model.safetensors", "tokenizer.spm")
    )

    return model, transform, tokenizer


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


def get_openmidnight(ckpt_path: str):
    """
    Adapted from:
    - https://huggingface.co/SophontAI/OpenMidnight

    :param ckpt_path: path to the stored checkpoint.
    """
    from torchvision import transforms

    # Model
    model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitg14_reg", weights=None)
    checkpoint = torch.load(ckpt_path, map_location="cpu")

    # Required because dinov2 is baseline 392 and openmidnight is baseline 224 resolution
    pos_embed = checkpoint["pos_embed"]
    model.pos_embed = torch.nn.parameter.Parameter(pos_embed)
    model.load_state_dict(checkpoint)

    # Transform
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
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


def get_genbio_pathfm(ckpt_path: str):
    """
    Adapted from:
    - https://github.com/genbio-ai/genbio-pathfm

    :param ckpt_path: path to the stored checkpoint.
    """
    try:
        from genbio_pathfm.model import GenBio_PathFM_Inference
    except ImportError:
        raise ImportError(
            "In order to use GenBio-PathFM, please run the following: 'pip install git+https://github.com/genbio-ai/genbio-pathfm.git'"
        )

    from torchvision import transforms

    # Model    
    model = GenBio_PathFM_Inference(ckpt_path, device="cpu")

    # Transform
    transform = transforms.Compose([
        transforms.Resize((224,224)),  
        transforms.ToTensor(),
        transforms.Normalize(
            mean=(0.697, 0.575, 0.728), 
            std=(0.188, 0.240, 0.187)
        ),
    ])

    return model, transform


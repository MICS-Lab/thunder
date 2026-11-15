from functools import partial
from operator import attrgetter

import torch
import torch.nn as nn
from omegaconf import DictConfig


def set_nested_attribute(obj, attr_string, value):
    """
    Set a nested attribute of an object using a string path.
    :param obj: object to set the attribute on.
    :param attr_string: string path to the attribute (e.g., "a.b.c").
    :param value: value to set the attribute to.
    """
    attrs = attr_string.split(".")
    current = obj
    for attr in attrs[:-1]:
        current = getattr(current, attr)
    setattr(current, attrs[-1], value)


def get_model_lora_names(
    model_name: str,
    model_type: str,
) -> tuple[str, str]:
    """
    Get the names of the LoRA blocks and qkv for a given model.
    :param model_name: name of the model.
    :param model_type: type of the model (timm, huggingface).
    """
    if model_type == "timm":
        block_name = "blocks"
        qkv_name = "attn.qkv"
    else:
        if model_name == "keep":
            block_name = "visual.blocks"
            qkv_name = "attn.qkv"
        elif model_name == "conch":
            block_name = "visual.trunk.blocks"
            qkv_name = "attn.qkv"
        elif model_name == "mettle15":
            block_name = "backbone.blocks"
            qkv_name = "attn.qkv"
        else:
            raise NotImplementedError(
                f"LoRA not implemented for {model_name} and {model_type} model type."
            )
    return block_name, qkv_name


def init_adapters(
    cfg: DictConfig, pretrained_model, device: str, hyperparam_search: bool = True
):
    """
    Initializing adapters.
    :param cfg: config defining the job to run.
    :param pretrained_model: pretrained model to augment with adapters.
    :param device: device to use (cpu, cuda).
    :param hyperparam_search: whether to perform hyperparameter search or not.
    """
    # Adapted from https://github.com/mnikitin/timm-vit-lora/blob/main/example.py
    if hyperparam_search:
        assign_lora = partial(
            GridSearchQKVLoRA,
            nb_adapters=len(cfg.adaptation.lr) * len(cfg.adaptation.weight_decay),
            rank=cfg.adaptation.lora_rank,
            alpha=cfg.adaptation.lora_alpha,
        )
    else:
        assign_lora = partial(
            QKVLoRA,
            rank=cfg.adaptation.lora_rank,
            alpha=cfg.adaptation.lora_alpha,
        )

    block_name, qkv_name = get_model_lora_names(
        cfg.pretrained_model.model_name, cfg.pretrained_model.type
    )

    for block in attrgetter(block_name)(pretrained_model):
        set_nested_attribute(
            block, qkv_name, assign_lora(attrgetter(qkv_name)(block)).to(device)
        )

    if hyperparam_search:
        for block in attrgetter(block_name)(pretrained_model):
            for i in range(len(cfg.adaptation.lr) * len(cfg.adaptation.weight_decay)):
                for param in (
                    attrgetter(qkv_name)(block).adapters[i].lora_q.parameters()
                ):
                    param.requires_grad = True
                for param in (
                    attrgetter(qkv_name)(block).adapters[i].lora_v.parameters()
                ):
                    param.requires_grad = True

    return pretrained_model


# Adapted from https://github.com/mnikitin/timm-vit-lora/tree/main
class LoRALayer(nn.Module):
    def __init__(
        self,
        in_dim: int,
        out_dim: int,
        rank: int,
        alpha: float,
    ) -> None:
        """
        Initializing LoRALayer.
        :param in_dim: dimension of the input token.
        :param out_dim: dimension of the output token.
        :param rank: LoRA bottleneck rank.
        :param alpha:
        """
        super().__init__()
        std = torch.sqrt(torch.tensor(rank).float())
        self.A = torch.nn.Parameter(torch.randn(in_dim, rank) / std)
        self.B = torch.nn.Parameter(torch.zeros(rank, out_dim))
        self.alpha = alpha / rank

    def forward(self, src: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        :param src: input tensor.
        """
        return self.alpha * (src @ self.A @ self.B)


# Adapted from https://github.com/mnikitin/timm-vit-lora/tree/main
class QKVLoRA(nn.Module):
    def __init__(
        self,
        qkv: nn.modules.linear.Linear,
        rank: int,
        alpha: float,
    ) -> None:
        """
        Initializing QKVLoRA.
        :param qkv
        :param rank
        :param alpha
        """
        super().__init__()
        self.qkv = qkv
        self.dim = qkv.in_features
        self.lora_q = LoRALayer(self.dim, self.dim, rank, alpha)
        self.lora_v = LoRALayer(self.dim, self.dim, rank, alpha)

    def forward(self, src: torch.Tensor) -> torch.Tensor:
        """
        Forward pass.
        :param src: input tensor.
        """
        qkv = self.qkv(src)

        qkv[:, :, : self.dim] += self.lora_q(src)
        qkv[:, :, 2 * self.dim :] += self.lora_v(src)
        return qkv


class GridSearchQKVLoRA(nn.Module):
    def __init__(
        self,
        qkv: nn.modules.linear.Linear,
        nb_adapters: int,
        rank: int,
        alpha: float,
    ) -> None:
        """
        Initializing GridSearchQKVLoRA.
        :param qkv
        :param nb_adapters: number of nb_adapters to train.
        :param rank
        :param alpha
        """
        super().__init__()
        self.nb_adapters = nb_adapters
        self.adapters = nn.ModuleList(
            [QKVLoRA(qkv, rank, alpha) for _ in range(self.nb_adapters)]
        )

    def forward(self, src: torch.Tensor | list) -> torch.Tensor:
        """
        Forward pass.
        :param src: input embedding.
        :return adapted tokens per adapter.
        """
        bs = src.shape[0] // self.nb_adapters
        assert src.shape[0] % self.nb_adapters == 0

        out = [
            self.adapters[i](src[i * bs : (i + 1) * bs])
            for i in range(self.nb_adapters)
        ]
        out = torch.concatenate(out, dim=0)

        return out

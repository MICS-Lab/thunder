import json
from pathlib import Path
from unittest.mock import patch

import torch
from omegaconf import OmegaConf
from PIL import Image

from thunder.models import pretrained_models
from thunder.models.download import download_models


def test_openmidnight11_download(tmp_path, monkeypatch):
    monkeypatch.setenv("THUNDER_BASE_DATA_FOLDER", str(tmp_path))
    with patch("huggingface_hub.hf_hub_download") as download:
        download_models("openmidnight11")
    assert [
        (call.args[0], call.kwargs["filename"]) for call in download.call_args_list
    ] == [
        ("medarc/OpenMidnight-1.1", "model.safetensors"),
        ("medarc/OpenMidnight-1.1", "config.json"),
    ]
    assert all(
        Path(call.kwargs["local_dir"]) == tmp_path / "pretrained_ckpts/openmidnight1.1"
        for call in download.call_args_list
    )


def test_openmidnight11_features(tmp_path, monkeypatch):
    monkeypatch.setenv("THUNDER_BASE_DATA_FOLDER", str(tmp_path))
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    cfg = OmegaConf.load(
        Path(pretrained_models.__file__).parents[1]
        / "config/pretrained_model/openmidnight11.yaml"
    )
    import timm
    from safetensors.torch import save_file

    args = dict(
        img_size=224,
        patch_size=14,
        embed_dim=32,
        depth=1,
        num_heads=4,
        num_classes=0,
        reg_tokens=4,
        global_pool="token",
    )
    cfg.timm_kwargs = {}
    reference = timm.create_model(
        "vit_tiny_patch16_224", pretrained=False, **args
    ).eval()
    save_file(reference.state_dict(), tmp_path / "model.safetensors")
    pretrained_cfg = dict(
        input_size=[3, 224, 224],
        mean=[0.5] * 3,
        std=[0.5] * 3,
        interpolation="bicubic",
        crop_pct=1.0,
        num_classes=0,
    )
    (tmp_path / "config.json").write_text(
        json.dumps(
            {
                "architecture": "vit_tiny_patch16_224",
                "pretrained_cfg": pretrained_cfg,
                "model_args": {
                    k: v for k, v in args.items() if k not in ["mlp_layer", "act_layer"]
                },
            }
        )
    )
    cfg.ckpt_path = str(tmp_path / "model.safetensors")
    model, transform, extract = pretrained_models.get_model(cfg, "cpu")
    model.eval().requires_grad_(False)
    x = transform(Image.new("RGB", (257, 231), color=(127, 91, 164))).unsqueeze(0)
    assert x.shape == (1, 3, 224, 224)
    with torch.no_grad():
        tokens = reference.forward_features(x)
        patches = tokens[:, 5:]
        pooled = tokens[:, 0]
        torch.testing.assert_close(extract(x, model, "linear_probing"), pooled)
        dense = extract(x, model, "segmentation")
        assert dense.shape == (1, 256, 32)
        torch.testing.assert_close(dense, patches)
    x.requires_grad_()
    extract(x, model, "linear_probing")[0, 0].backward()
    assert torch.isfinite(x.grad).all() and x.grad.abs().sum() > 0

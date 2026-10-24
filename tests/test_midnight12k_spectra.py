from pathlib import Path
from unittest.mock import patch

import torch
from omegaconf import OmegaConf
from PIL import Image

from thunder.models import pretrained_models
from thunder.models.download import download_models


def test_midnight12k_spectra_download(tmp_path, monkeypatch):
    monkeypatch.setenv("THUNDER_BASE_DATA_FOLDER", str(tmp_path))
    with patch("huggingface_hub.hf_hub_download") as download:
        download_models("midnight12k_spectra")
    assert [
        (call.args[0], call.kwargs["filename"]) for call in download.call_args_list
    ] == [
        ("medarc/Midnight-12k-SPECTRA", "model.safetensors"),
        ("medarc/Midnight-12k-SPECTRA", "config.json"),
    ]
    assert all(
        Path(call.kwargs["local_dir"])
        == tmp_path / "pretrained_ckpts/midnight12kspectra"
        for call in download.call_args_list
    )


def test_midnight12k_spectra_features(tmp_path, monkeypatch):
    monkeypatch.setenv("THUNDER_BASE_DATA_FOLDER", str(tmp_path))
    monkeypatch.setenv("HF_HUB_OFFLINE", "1")
    cfg = OmegaConf.load(
        Path(pretrained_models.__file__).parents[1]
        / "config/pretrained_model/midnight12k_spectra.yaml"
    )
    from transformers import Dinov2Config, Dinov2Model

    reference = Dinov2Model(
        Dinov2Config(
            hidden_size=32,
            num_hidden_layers=1,
            num_attention_heads=4,
            intermediate_size=64,
            image_size=224,
            patch_size=14,
        )
    ).eval()
    reference.save_pretrained(tmp_path)
    cfg.ckpt_path = str(tmp_path)
    model, transform, extract = pretrained_models.get_model(cfg, "cpu")
    model.eval().requires_grad_(False)
    x = transform(Image.new("RGB", (257, 231), color=(127, 91, 164))).unsqueeze(0)
    assert x.shape == (1, 3, 224, 224)
    with torch.no_grad():
        tokens = reference(x).last_hidden_state
        patches = tokens[:, 1:]
        pooled = torch.cat([tokens[:, 0], patches.mean(1)], dim=-1)
        torch.testing.assert_close(extract(x, model, "linear_probing"), pooled)
        dense = extract(x, model, "segmentation")
        assert dense.shape == (1, 256, 32)
        torch.testing.assert_close(dense, patches)
    x.requires_grad_()
    extract(x, model, "linear_probing")[0, 0].backward()
    assert torch.isfinite(x.grad).all() and x.grad.abs().sum() > 0

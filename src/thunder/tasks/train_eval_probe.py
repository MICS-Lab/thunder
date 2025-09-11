import json
import os
from collections.abc import Callable
from operator import attrgetter

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import wandb
from omegaconf import DictConfig, OmegaConf
from timm.models.vision_transformer import VisionTransformer
from torch.nn.modules.loss import _Loss
from torch.optim.optimizer import Optimizer
from torch.utils.data.dataloader import DataLoader
from tqdm import tqdm

from ..models.adapters import get_model_lora_names, init_adapters
from ..models.pretrained_models import load_pretrained_model
from ..models.task_specific_models import (ClassificationHead,
                                           GridSearchClassificationHead,
                                           GridSearchMaskTransformer,
                                           MaskTransformer)
from ..utils.calibration_metrics import compute_calibration_metrics
from ..utils.constants import UtilsConstants
from ..utils.data import PatchDataset
from ..utils.downstream_metrics import compute_metric, compute_metrics
from ..utils.utils import (get_hyperaparams_dict, local_seed, log_loss,
                           log_metrics, save_outputs, wb_mask)


def train_probe(
    cfg: DictConfig,
    data: dict,
    dataset_name: str,
    model_name: str,
    embedding_pre_loading: bool,
    image_pre_loading: bool,
    adaptation_type: str,
    task_type: str,
    criterion: _Loss,
    device: str,
    base_data_folder: str,
    base_embeddings_folder: str,
    wandb_base_folder: str,
    ckpt_folder: str,
    model_cls: Callable = None,
) -> dict:
    """
    Training a probe (classification or segmentation).
    :param cfg: config defining the job to run.
    :param data: dict containing data paths.
    :param dataset_name: name of the dataset.
    :param model_name: name of the pretrained model.
    :param embedding_pre_loading: whether to pre-load embeddings.
    :param image_pre_loading: whether to pre-load images.
    :param adaptation_type: type of adaptation (frozen, lora).
    :param task_type: tyoe of task (linear_probing, segmentation).
    :param criterion: objective to quantify model errors.
    :param device: device to use (cpu, cuda).
    :param base_data_folder: folder storing data.
    :param base_embeddings_folder: folder storing embeddings.
    :param wandb_base_folder: w&b folder.
    :param ckpt_folder: folder where to save model checkpoints.
    :return dict of best val checkpoint.
    """
    with local_seed(UtilsConstants.DEFAULT_SEED.value):
        if not embedding_pre_loading:
            # Loading pretrained model
            if model_cls is not None:
                pretrained_model = model_cls
                transform = model_cls.get_transform()
                extract_embedding = model_cls.get_embeddings
                for param in pretrained_model.parameters():
                    param.requires_grad = False
                pretrained_model.to(device)
                OmegaConf.set_struct(cfg, False)
                cfg.pretrained_model = {"emb_dim": model_cls.emb_dim}
            else:
                pretrained_model, transform, extract_embedding = load_pretrained_model(
                    cfg, adaptation_type, device
                )

            if adaptation_type == "lora":
                pretrained_model = init_adapters(cfg, pretrained_model, device)
                pretrained_model.train()
            else:
                pretrained_model.eval()
        else:
            pretrained_model = transform = extract_embedding = None

    # Dict of hyperparameters to search
    hyperparams_dict = get_hyperaparams_dict(cfg)

    # Task-specific model
    if task_type == "linear_probing":
        task_specific_model = GridSearchClassificationHead(
            len(hyperparams_dict),
            cfg.pretrained_model.emb_dim,
            cfg.dataset.nb_classes,
        )
    elif task_type == "segmentation":
        task_specific_model = GridSearchMaskTransformer(
            nb_heads=len(hyperparams_dict),
            n_cls=cfg.dataset.nb_classes,
            d_encoder=(
                cfg.pretrained_model.emb_dim_seg
                if hasattr(cfg.pretrained_model, "emb_dim_seg")
                else cfg.pretrained_model.emb_dim
            ),
            n_layers=2,
            n_heads=8,
            d_model=768,
            d_ff=3072,
            drop_path_rate=0.0,
            dropout=0.0,
        )
    task_specific_model = task_specific_model.to(device)
    task_specific_model.train()

    # Learned params
    optim_param_groups = []
    for i in range(len(hyperparams_dict)):
        optim_param_groups.append(
            {
                "params": task_specific_model.heads[i].parameters(),
                "lr": hyperparams_dict[i]["lr"],
                "weight_decay": hyperparams_dict[i]["weight_decay"],
            }
        )
    if adaptation_type == "lora":
        block_name, qkv_name = get_model_lora_names(
            cfg.pretrained_model.model_name, cfg.pretrained_model.type
        )
        for block in attrgetter(block_name)(pretrained_model):
            for i in range(len(hyperparams_dict)):
                optimized_weights = []
                optimized_weights += list(
                    attrgetter(qkv_name)(block).adapters[i].lora_q.parameters()
                )
                optimized_weights += list(
                    attrgetter(qkv_name)(block).adapters[i].lora_v.parameters()
                )
                optim_param_groups.append(
                    {
                        "params": optimized_weights,
                        "lr": hyperparams_dict[i]["lr"],
                        "weight_decay": hyperparams_dict[i]["weight_decay"],
                    }
                )

    # Optimizer
    optimizer = torch.optim.Adam(optim_param_groups)

    # Dataloaders
    dataloaders = {}
    for split in ["train", "val"]:
        split_dataset = PatchDataset(
            (
                None
                if (embedding_pre_loading and task_type != "segmentation")
                else data[split]["images"]
            ),
            (
                None
                if (embedding_pre_loading and task_type != "segmentation")
                else data[split]["labels"]
            ),
            transform,
            task_type,
            dataset_name,
            base_data_folder,
            os.path.join(base_embeddings_folder, dataset_name, model_name, split),
            image_pre_loading,
            embedding_pre_loading,
        )
        dataloaders[split] = DataLoader(
            split_dataset,
            batch_size=cfg.adaptation.batch_size,
            shuffle=True if split == "train" else False,
            num_workers=cfg.adaptation.num_workers,
        )

    # Hyperparameter search
    if task_type == "linear_probing":
        best_val_perf = -float("inf")
    elif task_type == "segmentation":
        best_val_perf = float("inf")
    best_ckpt_hyperparam_id = None

    for epoch in tqdm(range(cfg.adaptation.epochs)):
        for split in ["train", "val"]:
            if split == "train":
                if adaptation_type == "lora":
                    pretrained_model.train()
                task_specific_model.train()
            else:
                if adaptation_type == "lora":
                    pretrained_model.eval()
                task_specific_model.eval()

            (losses, metrics, task_specific_model, optimizer, *_) = train_eval(
                cfg,
                "train" if split == "train" else "eval",
                adaptation_type,
                task_type,
                criterion,
                dataloaders[split],
                pretrained_model,
                extract_embedding,
                task_specific_model,
                optimizer,
                device,
                comp_metrics=(task_type == "linear_probing"),
            )

            ckpt_epoch_dicts = {}
            for i in range(len(losses)):
                # Logging
                log_loss(
                    wandb_base_folder,
                    hyperparams_dict[i]["lr"],
                    hyperparams_dict[i]["weight_decay"],
                    losses[i],
                    split,
                    epoch,
                )
                if task_type == "linear_probing":
                    log_metrics(
                        wandb_base_folder,
                        metrics[i],
                        f"{split}_lr_{hyperparams_dict[i]['lr']}_weight_decay_{hyperparams_dict[i]['weight_decay']}",
                        epoch,
                    )

                if split == "val":
                    # Storing ckpt dict
                    ckpt_dict = {
                        "lr": hyperparams_dict[i]["lr"],
                        "weight_decay": hyperparams_dict[i]["weight_decay"],
                        "epoch": epoch,
                        "task_specific_model": {
                            k: v.cpu()
                            for k, v in task_specific_model.heads[i]
                            .state_dict()
                            .items()
                        },
                    }
                    if adaptation_type == "lora":
                        adapter_state_dicts = []
                        for block in attrgetter(block_name)(pretrained_model):
                            adapter_state_dicts.append(
                                {
                                    k: v.cpu()
                                    for k, v in attrgetter(qkv_name)(block)
                                    .adapters[i]
                                    .state_dict()
                                    .items()
                                }
                            )
                        ckpt_dict["adapters"] = adapter_state_dicts
                    ckpt_epoch_dicts[i] = ckpt_dict

                    # Updating best ckpt
                    if (
                        task_type == "linear_probing"
                        and metrics[i]["f1"]["metric_score"] > best_val_perf
                    ) or (
                        task_type == "segmentation"
                        and np.array(losses[i]).mean().item() < best_val_perf
                    ):
                        if task_type == "linear_probing":
                            best_val_perf = metrics[i]["f1"]["metric_score"]
                        elif task_type == "segmentation":
                            best_val_perf = np.array(losses[i]).mean().item()
                        best_ckpt_hyperparam_id = i
                        best_ckpt_dict = ckpt_epoch_dicts[best_ckpt_hyperparam_id]

            if split == "val" and not cfg.ckpt_saving.best_only:
                torch.save(
                    ckpt_epoch_dicts,
                    os.path.join(ckpt_folder, f"epoch_{epoch}.pth"),
                )

    # Saving all epoch ckpts (for best sweep)
    if not cfg.ckpt_saving.best_only:
        for epoch in range(cfg.adaptation.epochs):
            ckpt = torch.load(
                os.path.join(ckpt_folder, f"epoch_{epoch}.pth"),
                weights_only=True,
            )
            torch.save(
                ckpt[best_ckpt_hyperparam_id],
                os.path.join(ckpt_folder, f"epoch_{epoch}.pth"),
            )

    # Saving best ckpt
    torch.save(
        best_ckpt_dict,
        os.path.join(ckpt_folder, f"best_model.pth"),
    )

    return best_ckpt_dict


def eval_probe(
    cfg: DictConfig,
    data: dict,
    dataset_name: str,
    model_name: str,
    embedding_pre_loading: bool,
    image_pre_loading: bool,
    adaptation_type: str,
    task_type: str,
    criterion: _Loss,
    device: str,
    base_data_folder: str,
    base_embeddings_folder: str,
    wandb_base_folder: str,
    res_folder: str,
    best_ckpt_dict: dict,
    model_cls: Callable = None,
) -> None:
    """
    Evaluating a trained probe.
    :param cfg: config defining the job to run.
    :param data: dict containing data paths.
    :param dataset_name: name of the dataset.
    :param model_name: name of the pretrained model.
    :param embedding_pre_loading: whether to pre-load embeddings.
    :param image_pre_loading: whether to pre-load images.
    :param adaptation_type: type of adaptation (frozen, lora).
    :param task_type: tyoe of task (linear_probing, segmentation).
    :param criterion: objective to quantify model errors.
    :param device: device to use (cpu, cuda).
    :param base_data_folder: folder storing data.
    :param base_embeddings_folder: folder storing embeddings.
    :param wandb_base_folder: w&b folder.
    :param res_folder: folder to save results.
    :param best_ckpt_dict: ckpt dict for best probe model.
    """
    if model_cls is not None:
        OmegaConf.set_struct(cfg, False)
        cfg.pretrained_model = {"emb_dim": model_cls.emb_dim}

    # Task-specific model
    if task_type == "linear_probing":
        task_specific_model = ClassificationHead(
            cfg.pretrained_model.emb_dim, cfg.dataset.nb_classes
        )
    elif task_type == "segmentation":
        task_specific_model = MaskTransformer(
            n_cls=cfg.dataset.nb_classes,
            d_encoder=(
                cfg.pretrained_model.emb_dim_seg
                if hasattr(cfg.pretrained_model, "emb_dim_seg")
                else cfg.pretrained_model.emb_dim
            ),
            n_layers=2,
            n_heads=8,
            d_model=768,
            d_ff=3072,
            drop_path_rate=0.0,
            dropout=0.0,
        )
    task_specific_model.eval()
    task_specific_model = task_specific_model.to(device)

    # Getting best model
    task_specific_model.load_state_dict(best_ckpt_dict["task_specific_model"])

    with local_seed(UtilsConstants.DEFAULT_SEED.value):
        if not embedding_pre_loading or task_type == "segmentation":
            # Loading pretrained model
            if model_cls is not None:
                pretrained_model = model_cls
                transform = model_cls.get_transform()
                extract_embedding = model_cls.get_embeddings
                for param in pretrained_model.parameters():
                    param.requires_grad = False
                pretrained_model.to(device)
            else:
                pretrained_model, transform, extract_embedding = load_pretrained_model(
                    cfg, adaptation_type, device
                )

            if adaptation_type == "lora":
                block_name, qkv_name = get_model_lora_names(
                    cfg.pretrained_model.model_name, cfg.pretrained_model.type
                )
                pretrained_model = init_adapters(
                    cfg, pretrained_model, device, hyperparam_search=False
                )

                block_name, qkv_name = get_model_lora_names(
                    cfg.pretrained_model.model_name, cfg.pretrained_model.type
                )
                for block_id, block in enumerate(
                    attrgetter(block_name)(pretrained_model)
                ):
                    attrgetter(qkv_name)(block).load_state_dict(
                        best_ckpt_dict["adapters"][block_id]
                    )

            pretrained_model.eval()
        else:
            pretrained_model, transform, extract_embedding = None, None, None

    # Test dataset and dataloader
    test_dataset = PatchDataset(
        (
            None
            if (embedding_pre_loading and task_type != "segmentation")
            else data["test"]["images"]
        ),
        (
            None
            if (embedding_pre_loading and task_type != "segmentation")
            else data["test"]["labels"]
        ),
        transform,
        task_type,
        dataset_name,
        base_data_folder,
        os.path.join(base_embeddings_folder, dataset_name, model_name, "test"),
        image_pre_loading,
        embedding_pre_loading if task_type == "linear_probing" else False,
    )
    test_dataloader = DataLoader(
        test_dataset,
        batch_size=cfg.adaptation.batch_size,
        shuffle=False,
        num_workers=cfg.adaptation.num_workers,
    )

    # Test evaluation
    (
        test_losses,
        test_metrics,
        _,
        _,
        test_viz_pred,
        test_viz_gt,
        test_viz_im,
    ) = train_eval(
        cfg,
        "eval",
        adaptation_type,
        task_type,
        criterion,
        test_dataloader,
        pretrained_model,
        extract_embedding,
        task_specific_model,
        None,
        device,
        hyperparam_search=False,
    )
    # list has only one element
    test_losses = test_losses[0]
    test_metrics = test_metrics[0]
    test_viz_pred = test_viz_pred[0]

    # Logging
    log_loss(
        wandb_base_folder,
        best_ckpt_dict["lr"],
        best_ckpt_dict["weight_decay"],
        test_losses,
        "test",
        cfg.adaptation.epochs,
    )
    log_metrics(
        wandb_base_folder,
        test_metrics,
        f"test_lr_{best_ckpt_dict['lr']}_weight_decay_{best_ckpt_dict['weight_decay']}",
        cfg.adaptation.epochs,
    )

    if task_type == "segmentation":
        mask_list = wb_mask(
            test_viz_im.permute((0, 2, 3, 1)).cpu().numpy(),
            test_viz_pred.cpu().numpy(),
            test_viz_gt.cpu().numpy(),
            cfg.dataset.classes,
        )
        wandb.log(
            {
                f"{wandb_base_folder}/test_predictions_lr_{best_ckpt_dict['lr']}_weight_decay_"
                f"{best_ckpt_dict['weight_decay']}": mask_list
            }
        )
    # Saving metric values
    save_outputs(res_folder, test_metrics)


def train_eval(
    cfg: DictConfig,
    run_type: str,
    adaptation_type: str,
    task_type: str,
    criterion: _Loss,
    dataloader: DataLoader,
    pretrained_model: VisionTransformer,
    extract_embedding: Callable,
    task_specific_model: ClassificationHead,
    optimizer: Optimizer,
    device: str,
    hyperparam_search: bool = True,
    comp_metrics: bool = True,
):
    """
    Performing one training or evaluation loop.

    :param cfg: config defining the job to run.
    :param run_type: type of run (train or eval).
    :param adaptation_type: type of adaptation (frozen, lora).
    :param task_type: type of task (classification, segmentation).
    :param criterion: objective to quantify model errors.
    :param dataloader: dataloader to load data batches.
    :param pretrained_model: pretrained model to use.
    :param extract_embedding: function to extract an embedding vector from an input image with the pretrained model.
    :param task_specific_model: specific model used to predict task-related information.
    :param optimizer to use if training.
    :param device: device to use (cpu, cuda).
    :param hyperparam_search: whether to perform hyperparameter search or not.
    :param comp_metrics: whether to compute metrics or not.
    """

    tot_loss = []
    all_out = []
    all_label = []
    for batch_id, batch in tqdm(
        enumerate(dataloader), total=len(dataloader), disable=hyperparam_search
    ):
        # Batch data
        if "emb" in batch.keys():
            emb = batch["emb"].to(device)
            compute_emb = False
        else:
            image = batch["image"].to(device)
            compute_emb = True
        label = batch["label"].to(device)

        if run_type == "train":
            # Zero the parameter gradients
            optimizer.zero_grad()

        # Forward pass
        with torch.set_grad_enabled(run_type == "train"):
            if compute_emb:
                if adaptation_type == "lora" and hyperparam_search:
                    block_name, _ = get_model_lora_names(
                        cfg.pretrained_model.model_name, cfg.pretrained_model.type
                    )
                    bs = image.shape[0]
                    nb_adapters = attrgetter(block_name)(pretrained_model)[
                        0
                    ].attn.qkv.nb_adapters
                    image = image.repeat(nb_adapters, 1, 1, 1)
                emb = extract_embedding(image, pretrained_model, task_type)

                if adaptation_type == "lora" and hyperparam_search:
                    emb = [emb[i * bs : (i + 1) * bs] for i in range(nb_adapters)]

            outputs = task_specific_model(emb)
            if type(outputs) != list:
                outputs = [outputs]

            if task_type == "segmentation":
                for i in range(len(outputs)):
                    outputs[i] = nn.functional.interpolate(
                        outputs[i], (label.shape[1], label.shape[2]), mode="bilinear"
                    )

        if task_type == "linear_probing":
            label = label.view(-1)
        loss = 0
        for i in range(len(outputs)):
            output = outputs[i]
            if task_type == "segmentation":
                # Applying masking (removing pixels where gt == -1)
                curr_loss = criterion(output, label, label != -1)

                if comp_metrics:
                    unmasked_label = [l != -1 for l in label]
                    label = [l[u] for l, u in zip(label, unmasked_label)]
                    out = []
                    for o, m in zip(output, unmasked_label):
                        out.append(
                            torch.cat(
                                [o[c][m].unsqueeze(-1) for c in range(o.shape[0])],
                                dim=-1,
                            )
                        )
            else:
                out = []
                for c in range(output.shape[1]):
                    out.append(output[:, c].unsqueeze(-1))
                out = torch.cat(out, dim=-1)
                curr_loss = criterion(out, label)
            loss += curr_loss

            # Logging
            if batch_id == 0:
                tot_loss.append([curr_loss.item()])
                if comp_metrics:
                    all_out.append(
                        [[o.detach().cpu() for o in out]]
                        if task_type == "segmentation"
                        else [out.detach().cpu()]
                    )
            else:
                tot_loss[i].append(curr_loss.item())
                if comp_metrics:
                    all_out[i].append(
                        [o.detach().cpu() for o in out]
                        if task_type == "segmentation"
                        else out.detach().cpu()
                    )
        # Logging
        if comp_metrics:
            if task_type == "segmentation":
                all_label.extend([l.cpu() for l in label])
            else:
                all_label.append(label.cpu())

        if run_type == "train":
            # Compute gradients
            loss.backward()

            # Backward pass - model update
            optimizer.step()

    # Vizualizing the last batch
    viz_pred = []
    for i in range(len(outputs)):
        viz_pred.append(outputs[i].argmax(dim=1))
    viz_gt = batch["label"]
    viz_gt[viz_gt == -1] = 0

    if "viz_image" in batch.keys():
        viz_im = batch["viz_image"]
    else:
        viz_im = None

    if comp_metrics:
        if task_type == "segmentation":
            metrics = []
            for i in range(len(all_out)):
                all_out[i] = [
                    F.softmax(item, dim=1) for batch in all_out[i] for item in batch
                ]
                all_metrics = [
                    compute_metrics(o, None, l, True, compute_ci=False)
                    for o, l in zip(all_out[i], all_label)
                    if len(l) > 0
                ]
                weights = np.array([len(l) for l in all_label if len(l) > 0]).astype(
                    np.float32
                )

                # Finding background-only masks
                bg_only = np.array([l.sum().item() == 0 for l in all_label if len(l) > 0])
                freq_bg_only = bg_only.sum().item() / len(bg_only)
                no_bg_only_weight = max(
                    1.0, freq_bg_only * cfg.task.no_bg_only_weight_test
                )
                weights[~bg_only] *= no_bg_only_weight

                # Averaging per-image performance and computing confidence intervals
                all_metrics_out = {}
                for key in all_metrics[0]:
                    metric_vals = [d[key]["metric_score"] for d in all_metrics]
                    all_metrics_out[key] = compute_metric(
                        weights.tolist(),
                        metric_vals,
                        lambda weights, metric_vals: np.average(
                            metric_vals, weights=weights
                        ),
                    )
                    all_metrics_out[f"per_sample_{key}"] = metric_vals
                metrics.append(all_metrics_out)
        else:
            # Computing metrics
            all_label = torch.cat(all_label)
            metrics = []
            for i in range(len(all_out)):
                all_out[i] = torch.cat(all_out[i])
                all_out[i] = F.softmax(all_out[i], dim=1)
                classification_metrics = compute_metrics(
                    all_out[i], None, all_label, compute_ci=(not hyperparam_search)
                )
                conformal_metrics = compute_calibration_metrics(
                    all_out[i], all_label, compute_ci=(not hyperparam_search)
                )
                curr_metrics = (
                    classification_metrics | conformal_metrics
                )  # merging dictionaries
                metrics.append(curr_metrics)
    else:
        metrics = None

    return tot_loss, metrics, task_specific_model, optimizer, viz_pred, viz_gt, viz_im

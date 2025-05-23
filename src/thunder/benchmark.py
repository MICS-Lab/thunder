import os

import hydra
from omegaconf import DictConfig
from typing import Callable

from .datasets.utils import is_dataset_available
from .models.utils import is_model_available, load_custom_model_from_file


def benchmark(
    model: str | Callable,
    dataset: str,
    task: str,
    loading_mode: str = "online_loading",
    lora: bool = False,
    ckpt_save_all: bool = False,
    online_wandb: bool = False,
    **kwargs,
):
    """
    Runs a benchmark for a pretrained model on a dataset with a task-specific approach.

    where options are:
        - dataset: *bach*, *bcss*, *bracs*, *break_his*, *ccrcc*, *crc*, *esca*, *mhist*, *ocelot*, *pannuke*, *patch_camelyon*, *segpath_epithelial*, *segpath_lymphocytes*, *tcga_crc_msi*, *tcga_tils*, *tcga_uniform*, *wilds*
        - model: *hiboub*, *hiboul*, *hoptimus0*, *hoptimus1*, *midnight*, *phikon*, *phikon2*, *uni*, *uni2h*, *virchow*, *virchow2*, *conch*, *titan*, *keep*, *musk*, *plip*, *quiltnetb32*, *dinov2base*, *dinov2large*, *vitbasepatch16224in21k*, *vitlargepatch16224in21k*, *clipvitbasepatch32*, *clipvitlargepatch14*
        - task: *adversarial_attack_linear*, *alignment_scoring*, *image_retrieval*, *knn*, *linear_probing*, *pre_computing_embeddings*, *segmentation*, *simple_shot*, *transformation_invariance*
        - loading_mode: *online_loading*, *image_pre_loading*, *embedding_pre_loading*

    Args:
        model (str): The name of the pretrained model to use.
        dataset (str): The name of the dataset to use.
        task (str): The name of the task to perform.
        loading_mode (str): The type of data loading to use.
        lora (bool): Whether to use LoRA (Low-Rank Adaptation) for model adaptation. Default is False.
        ckpt_save_all (bool): Whether to save all checkpoints during training. Default is False which means that only the best is saved.
        online_wandb (bool): Whether to use online mode for Weights & Biases (wandb) logging. Default is False which means offline mode.
    """
    from hydra import compose, initialize
    from omegaconf import OmegaConf

    from .utils.config import get_config

    wandb_mode = "online" if online_wandb else "offline"
    adaptation_type = "lora" if lora else "frozen"
    ckpt_saving = "save_ckpts_all_epochs" if ckpt_save_all else "save_best_ckpt_only"
    model_name = model if isinstance(model, str) else None

    if model_name and model_name.startswith("custom:"):
        model = load_custom_model_from_file(model_name.split(":")[1])
        model_name = None

    # Get Config
    cfg = get_config(
        task,
        ckpt_saving,
        dataset,
        model_name,
        adaptation_type,
        loading_mode,
        wandb_mode,
        **kwargs,
    )

    if not is_dataset_available(dataset):
        from . import download_datasets

        download_datasets(dataset, make_splits=True)

    if model_name and not is_model_available(model_name):
        from . import download_models

        download_models(model)

    if isinstance(model, str):
        # If model is a string, cfg is already populated with the model details
        run_benchmark(cfg)
    else:
        # If model is a callable, pass it directly to the benchmark function
        run_benchmark(cfg, model)


def run_benchmark(cfg: DictConfig, model_cls: Callable = None) -> None:
    """
    Benchmarking a pretrained model on a dataset with a task-specific approach.

    :param cfg: config defining the job to run.
    """

    import numpy as np
    import torch
    import wandb
    from omegaconf import OmegaConf

    from .tasks.adversarial_attack_linear import adversarial_attack_linear
    from .tasks.alignment_scoring import alignment_scoring
    from .tasks.image_retrieval import image_retrieval
    from .tasks.knn_classification import knn
    from .tasks.pre_computing_patch_embeddings import pre_computing_patch_embeddings
    from .tasks.simple_shot import simple_shot
    from .tasks.train_eval_probe import eval_probe, train_probe
    from .tasks.transformation_invariance import transformation_invariance
    from .utils.constants import UtilsConstants
    from .utils.data import get_data, load_embeddings
    from .utils.dice_loss import multiclass_dice_loss
    from .utils.utils import set_seed

    # Setting the random seed
    set_seed(UtilsConstants.DEFAULT_SEED.value)

    # Getting device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Checking task, data and adaptation are compatible
    base_data_folder = cfg.dataset.base_data_folder
    base_embeddings_folder = cfg.task.base_embeddings_folder
    task_type = cfg.task.type
    task_compatible_adaptation_types = cfg.task.compatible_adaptation_types
    data_compatible_tasks = cfg.dataset.compatible_tasks
    adaptation_type = cfg.adaptation.type
    dataset_name = cfg.dataset.dataset_name
    model_name = (
        cfg.pretrained_model.model_name if model_cls is None else model_cls.name
    )
    image_pre_loading = cfg.data_loading.image_pre_loading
    embedding_pre_loading = cfg.data_loading.embedding_pre_loading
    assert task_type in data_compatible_tasks, print(
        f"The chosen task ({task_type}) is not within the compatible task types for "
        f"the chosen dataset: {data_compatible_tasks}."
    )
    assert adaptation_type in task_compatible_adaptation_types, print(
        f"The chosen adaptation type ({adaptation_type}) is not within the compatible "
        f"adaptation types for the chosen task: {task_compatible_adaptation_types}."
    )
    assert not (image_pre_loading and embedding_pre_loading), print(
        "We do not pre-load both images and embeddings."
    )

    # W&B login
    wandb.login()

    # W&B run
    wandb.init(
        project=f"thunder_{task_type}",
        name=f"|{task_type}| |{adaptation_type}| |{dataset_name}| |{model_name}|",
        tags=[task_type, adaptation_type, dataset_name, model_name],
        config=OmegaConf.to_container(cfg, resolve=True),
        dir=os.path.join(os.environ["THUNDER_BASE_DATA_FOLDER"], "outputs/"),
        mode=cfg.wandb.mode,
    )
    wandb_base_folder = f"|{task_type}| |{adaptation_type}| |{dataset_name}|"
    ckpt_folder = os.path.join(
        os.environ["THUNDER_BASE_DATA_FOLDER"],
        "outputs",
        "ckpts",
        dataset_name,
        model_name,
        adaptation_type,
    )
    os.makedirs(ckpt_folder, exist_ok=True)

    # Folder to save results
    res_folder = os.path.join(
        os.environ["THUNDER_BASE_DATA_FOLDER"],
        "outputs",
        "res",
        dataset_name,
        model_name,
        task_type,
        adaptation_type,
    )
    os.makedirs(res_folder, exist_ok=True)

    if task_type in ["linear_probing", "segmentation"]:
        # Criterion
        if task_type == "linear_probing":
            criterion = torch.nn.CrossEntropyLoss()
        elif task_type == "segmentation":
            criterion = multiclass_dice_loss

        # Loading data
        if not embedding_pre_loading or task_type == "segmentation":
            data = get_data(dataset_name, base_data_folder)
        else:
            data = None

        # Probe training
        if not os.path.exists(os.path.join(ckpt_folder, "best_model.pth")):
            best_ckpt_dict = train_probe(
                cfg,
                data,
                dataset_name,
                model_name,
                embedding_pre_loading,
                image_pre_loading,
                adaptation_type,
                task_type,
                criterion,
                device,
                base_data_folder,
                base_embeddings_folder,
                wandb_base_folder,
                ckpt_folder,
                model_cls,
            )
        else:
            print(
                f"Found already trained best model {os.path.join(ckpt_folder, 'best_model.pth')}. "
                f"Not re-training."
            )
            best_ckpt_dict = torch.load(
                os.path.join(ckpt_folder, "best_model.pth"), weights_only=True
            )
        # Probe evaluation
        eval_probe(
            cfg,
            data,
            dataset_name,
            model_name,
            embedding_pre_loading,
            image_pre_loading,
            adaptation_type,
            task_type,
            criterion,
            device,
            base_data_folder,
            base_embeddings_folder,
            wandb_base_folder,
            res_folder,
            best_ckpt_dict,
            model_cls,
        )

    elif task_type in [
        "alignment_scoring",
        "embedding_space_visualization",
        "emir",
        "image_retrieval",
        "knn",
        "knn_ensembling",
        "pre_computing_embeddings",
        "simple_shot",
    ]:
        embeddings_folder = os.path.join(
            base_embeddings_folder,
            dataset_name,
            model_name,
        )

        if not os.path.exists(embeddings_folder):
            print(
                f"No pre-computed embeddings found for the (dataset, model) pair "
                f"({dataset_name}, {model_name}). Computing them."
            )

            pre_computing_patch_embeddings(
                cfg,
                embeddings_folder,
                device,
                dataset_name,
                base_data_folder,
                data_compatible_tasks,
                adaptation_type,
                base_embeddings_folder,
                model_name,
                image_pre_loading,
                embedding_pre_loading,
                model_cls,
            )

        else:
            print(
                f"Pre-computed embeddings already found for the (dataset, model) pair "
                f"({dataset_name}, {model_name}). Not re-computing them."
            )

        if task_type in [
            "alignment_scoring",
            "embedding_space_visualization",
            "emir",
            "image_retrieval",
            "knn",
            "knn_ensembling",
            "simple_shot",
        ]:
            # Loading embeddings and labels
            splits = ["train", "val"]
            if task_type in ["image_retrieval", "knn", "knn_ensembling", "simple_shot"]:
                splits.append("test")
            embs, labels = load_embeddings(embeddings_folder, splits)

            if task_type == "alignment_scoring":
                alignment_scoring(
                    base_embeddings_folder,
                    model_name,
                    dataset_name,
                    int(cfg.task.max_nb_embeddings_comp),
                    torch.Tensor(np.concatenate([embs["train"], embs["val"]], axis=0)),
                    res_folder,
                    wandb_base_folder,
                )
            elif task_type == "image_retrieval":
                k_vals = cfg.task.k_vals
                image_retrieval(
                    embs["train"],
                    labels["train"],
                    embs["test"],
                    labels["test"],
                    base_data_folder,
                    dataset_name,
                    k_vals,
                    res_folder,
                    wandb_base_folder,
                )
            elif task_type == "knn":
                k_vals = cfg.task.k_vals
                knn(
                    embs,
                    labels,
                    k_vals,
                    res_folder,
                    wandb_base_folder,
                )
            elif task_type == "simple_shot":
                simple_shot(
                    dataset_name,
                    base_data_folder,
                    embs["train"],
                    embs["test"],
                    labels["test"],
                    res_folder,
                    wandb_base_folder,
                )

    if task_type == "transformation_invariance":
        transformation_invariance(
            cfg,
            dataset_name,
            model_name,
            image_pre_loading,
            adaptation_type,
            device,
            base_data_folder,
            wandb_base_folder,
            res_folder,
        )
    elif task_type == "adversarial_attack_linear":
        adversarial_attack_linear(
            cfg,
            dataset_name,
            model_name,
            image_pre_loading,
            adaptation_type,
            device,
            base_data_folder,
            wandb_base_folder,
            res_folder,
            model_cls,
        )



## Hyperparameters
You should keep all thunder default hyperparameters for all tasks and datasets, except for the `segpath_epithelial` and `segpath_lymphocytes` datasets (`segmentation` task) for which you must override the number of epochs to `9` and `21` respectively (because of the size of the datasets). See [this tutorial](https://mics-lab.github.io/thunder/custom_config/) for more details about how to override the default configuration.

**CLI**
```bash
# Evaluating hiboub on segpath_epithelial
thunder benchmark hiboub segpath_epithelial segmentation --loading-mode=embedding_pre_loading --adaptation.epochs=9

# Evaluating hiboub on segpath_lymphocytes
thunder benchmark hiboub segpath_lymphocytes segmentation --loading-mode=embedding_pre_loading --adaptation.epochs=21
```

**API**
```python
import thunder

# Evaluating hiboub on segpath_epithelial
thunder.benchmark(
    "hiboub",
    dataset="segpath_epithelial",
    task="segmentation",
    loading_mode="embedding_pre_loading",
    **{"adaptation.epochs": 9})

# Evaluating hiboub on segpath_lymphocytes
thunder.benchmark(
    "hiboub",
    dataset="segpath_lymphocytes",
    task="segmentation",
    loading_mode="embedding_pre_loading",
     **{"adaptation.epochs": 21})
```

## Reproducing leaderboard results on a SLURM cluster

To reproduce the [THUNDER leaderboards](https://mics-lab.github.io/thunder/leaderboards/) for a given model, we provide a SLURM array script at `scripts/benchmark_all_tasks.sh`. It evaluates a single model across all benchmark datasets and their associated tasks, launching one array task per dataset.

```console
sbatch scripts/benchmark_all_tasks.sh <model_name>
```

The script also accepts a custom model, by passing a `custom:` path to your model definition file (see [Benchmarking a Custom Model](https://mics-lab.github.io/thunder/custom_model/)):

```console
sbatch scripts/benchmark_all_tasks.sh custom:/path/to/your/model.py
```

> **GPU memory**: the segmentation datasets (array indices 16–19) require a GPU with **at least 32 GB of VRAM**. The classification datasets fit on smaller GPUs.

Once all array tasks have completed, gather the per-run outputs into a single results table:

```console
thunder results-summary
```

The reproduced leaderboard scores are the rows whose `dataset` column starts with `benchmark_`. These rows are the aggregated means intended to match the values reported in the [THUNDER leaderboards](https://mics-lab.github.io/thunder/leaderboards/).

> **Note**: all results reported in the [THUNDER leaderboards](https://mics-lab.github.io/thunder/leaderboards/) were produced using V100 GPUs. Running on different hardware may lead to small numerical differences.

### Running without internet access

On compute nodes without internet access, all models and datasets must be downloaded beforehand from a node that does have connectivity, using the `thunder download-models <model>` command. You should then force offline mode by uncommenting the following lines in the script:

```bash
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```
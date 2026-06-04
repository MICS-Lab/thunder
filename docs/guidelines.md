

## Hyperparameters
You should keep all thunder default hyperparameters for all tasks and datasets, except for the `segpath_epithelial` and `segpath_lymphocytes` datasets (`segmentation` task) for which you must override the number of epochs to `9` and `21` respectively (because of the size of the datasets). See [this tutorial](https://mics-lab.github.io/thunder/custom_config/) for more details about how to override the default configuration.

**CLI**
```bash
# Evaluating hiboub on segpath_epithelial
thunder benchmark hiboub segpath_epithelial segmentation --loading-mode=embedding_pre_loading --adaptation.epochs 9

# Evaluating hiboub on segpath_lymphocytes
thunder benchmark hiboub segpath_lymphocytes segmentation --loading-mode=embedding_pre_loading --adaptation.epochs 21
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

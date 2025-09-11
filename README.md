
# Tile-level Histopathology image Understanding benchmark

<img src="https://raw.githubusercontent.com/MICS-Lab/thunder/main/docs/banner.png" />

<div align="center">

[![Paper](https://img.shields.io/badge/THUNDER-arXiv.2507.07860-purple.svg)](https://arxiv.org/abs/2507.07860)
[![Python application](https://github.com/MICS-lab/thunder/actions/workflows/ci.yml/badge.svg)](https://github.com/MICS-lab/thunder/actions/workflows/ci.yml)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue)](https://mics-lab.github.io/thunder/)
[![License](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://github.com/MICS-Lab/thunder/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

</div>

We introduce **THUNDER**, a comprehensive benchmark designed to rigorously compare foundation models across various downstream tasks in computational pathology. THUNDER enables the evaluation and analysis of feature representations, robustness, and uncertainty quantification of these models across different datasets. Our benchmark encompasses a diverse collection of well-established datasets, covering multiple cancer types, image magnifications, and varying image and sample sizes. We propose an extensive set of tasks aimed at thoroughly assessing the capabilities and limitations of foundation models in digital pathology.

&#9889; **Paper**: [THUNDER: Tile-level Histopathology image UNDERstanding benchmark](https://arxiv.org/abs/2507.07860)\
&#9889; **Homepage/Documentation**: [THUNDER docs](https://mics-lab.github.io/thunder/)\
&#9889; **Leaderboard**: [THUNDER leaderboard](https://mics-lab.github.io/thunder/leaderboard/)

## Overview

We propose a benchmark to compare and study foundation models across three axes: (i) downstream task performance, (ii) feature space comparisons, and (iii) uncertainty and robustness. Our current version integrates 23 foundation models, vision-only, vision-language, trained on pathology or natural images, on 16 datasets covering different magnifications and organs. THUNDER also supports the use of new user-defined models for direct comparisons.

<img src="https://raw.githubusercontent.com/MICS-Lab/thunder/main/docs/overview.png" />


## Usage
To learn more about how to use `thunder`, please visit our [documentation](https://mics-lab.github.io/thunder/).

An API and command line interface (CLI) are provided to allow users to download datasets, models, and run benchmarks. The API is designed to be user-friendly and allows for easy integration into existing workflows. The CLI provides a convenient way to access the same functionality from the command line.

> [!IMPORTANT]
> **Downloading supported foundation models**: you will have to visit the Huggingface URL of supported models you wish to use in order to accept usage conditions.

<details>
<summary>List of Huggingface URLs</summary>

* UNI: https://huggingface.co/MahmoodLab/UNI
* UNI2-h: https://huggingface.co/MahmoodLab/UNI2-h
* Virchow: https://huggingface.co/paige-ai/Virchow
* Virchow2: https://huggingface.co/paige-ai/Virchow2
* H-optimus-0: https://huggingface.co/bioptimus/H-optimus-0
* H-optimus-1: https://huggingface.co/bioptimus/H-optimus-1
* CONCH: https://huggingface.co/MahmoodLab/CONCH
* TITAN/CONCHv1.5: https://huggingface.co/MahmoodLab/TITAN
* Phikon: https://huggingface.co/owkin/phikon
* Phikon2: https://huggingface.co/owkin/phikon-v2
* Hibou-b: https://huggingface.co/histai/hibou-b
* Hibou-L: https://huggingface.co/histai/hibou-L
* Midnight-12k: https://huggingface.co/kaiko-ai/midnight
* KEEP: https://huggingface.co/Astaxanthin/KEEP
* QuiltNet-B-32: https://huggingface.co/wisdomik/QuiltNet-B-32
* PLIP: https://huggingface.co/vinid/plip
* MUSK: https://huggingface.co/xiangjx/musk
* DINOv2-B: https://huggingface.co/facebook/dinov2-base
* DINOv2-L: https://huggingface.co/facebook/dinov2-large
* ViT-B: https://huggingface.co/google/vit-base-patch16-224-in21k
* ViT-L: https://huggingface.co/google/vit-large-patch16-224-in21k
* CLIP-B: https://huggingface.co/openai/clip-vit-base-patch32
* CLIP-L: https://huggingface.co/openai/clip-vit-large-patch14

</details>

### API Usage
When using the API you can run the following code to download datasets, models and run a benchmark:

```python
from thunder import benchmark

benchmark("phikon", "break_his", "knn")
```

### CLI Usage
When using the CLI you can run the following command to see all available options,

```console
thunder --help
```

In order to reproduce the above example you can run the following command:

```console
thunder benchmark phikon break_his knn
```

### Extracting embeddings with any supported foundation model (API Usage)
We also provide a [`get_model_from_name`](https://mics-lab.github.io/thunder/api/#thunder.models.get_model_from_name) function through our API to extract embeddings using any foundation model we support on your own data. Below is an example if you want to get the Pytorch callable, transforms and function to extract embeddings for `uni2h`:

```python
from thunder.models import get_model_from_name

model, transform, get_embeddings = get_model_from_name("uni2h", device="cuda")
```

## Installing thunder

Code tested with Python 3.10. To replicate, you can create the following conda environment and activate it,
```console
conda create -n thunder_env python=3.10
conda activate thunder_env
```

To install `thunder` run one of the following commands:

#### From PyPi
```console
pip install thunder-bench
```

#### From Source
```console
pip install -e . # install the package in editable mode
```
```console
pip install . # install the package
```

Before running `thunder`, ensure that the environment variable `THUNDER_BASE_DATA_FOLDER` is defined. This variable specifies the path where outputs, foundation models, and datasets will be stored. You can set it by running:

```console
export THUNDER_BASE_DATA_FOLDER="/path/to/your/data/folder"
```

Replace `/path/to/your/data/folder` with your desired storage directory.

If you want to use the CONCH and MUSK models, you should install them as follows:

```console
pip install git+https://github.com/Mahmoodlab/CONCH.git # CONCH
pip install git+https://github.com/lilab-stanford/MUSK.git # MUSK
```
from setuptools import find_packages, setup

setup(
    name="thundr",
    version="0.1.0",
    description="THUNDER: Tile-level Histopathology image UNDERstanding benchmark",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "einops==0.8.1",
        "einops_exts==0.0.4",
        "click==8.1.0",
        "fairscale==0.4.13",
        "gdown==5.2.0",
        "h5py==3.12.1",
        "huggingface-hub==0.27.1",
        "hydra-core==1.3.2",
        "matplotlib==3.9.2",
        "mkdocs==1.6.1",
        "mkdocstrings==0.29.1",
        "mkdocstrings-python==1.16.10",
        "mkdocs-material==9.6.11",
        "numpy==1.24.3",
        "omegaconf==2.3.0",
        "openpyxl==3.1.5",
        "pandas==2.2.3",
        "ijson==3.4.0",
        "pillow==11.0.0",
        "plotly==6.0.0",
        "scikit-learn==1.6.1",
        "tabulate==0.9.0",
        "timm==1.0.13",
        "torch==2.5.1",
        "torchaudio==2.5.1",
        "torchvision==0.20.1",
        "tqdm==4.66.5",
        "transformers==4.48.0",
        "wandb==0.19.4",
        "wilds==2.0.0",
        "kornia==0.8.0",
        "typer==0.15.3",
        "conch @ git+https://github.com/Mahmoodlab/CONCH.git",
        "musk @ git+https://github.com/lilab-stanford/MUSK.git",
    ],
    extras_require={
        "dev": ["pytest"],
    },
    python_requires=">=3.10,<3.11",
    entry_points={
        "console_scripts": [
            "thunder = thunder.main:app",
        ],
    },
    package_data={"thunder": ["config/**/*.yaml"]},
)

from enum import Enum


class ModelConstants(Enum):
    PRETRAINED_MODELS = [
        # Histo-image models
        "hiboub",
        "hiboul",
        "hoptimus0",
        "hoptimus1",
        "midnight",
        "phikon",
        "phikon2",
        "uni",
        "uni2h",
        "virchow",
        "virchow2",
        # Histo-image-language models
        "conch",
        "titan",
        "keep",
        "musk",
        "plip",
        "quiltnetb32",
        # Natural-image models
        "dinov2base",
        "dinov2large",
        "vitbasepatch16224in21k",
        "vitlargepatch16224in21k",
        # Natural-image-language models
        "clipvitbasepatch32",
        "clipvitlargepatch14",
    ]


class DatasetConstants(Enum):
    DATASETS = [
        "bach",
        "bracs",
        "break_his",
        "ccrcc",
        "crc",
        "esca",
        "mhist",
        "ocelot",
        "pannuke",
        "patch_camelyon",
        "segpath_epithelial",
        "segpath_lymphocytes",
        "tcga_crc_msi",
        "tcga_tils",
        "tcga_uniform",
        "wilds",
        "spider_breast",
        "spider_colorectal",
        "spider_skin",
        "spider_thorax",
    ]


class UtilsConstants(Enum):
    DEFAULT_SEED = 0

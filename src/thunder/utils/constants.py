from enum import Enum


class ModelConstants(Enum):
    PRETRAINED_MODELS = [
        # Histo-image models
        "hiboub",
        "hiboul",
        "hoptimus0",
        "h0mini",
        "hoptimus1",
        "genbio-pathfm",
        "kaiko_vits8",
        "kaiko_vits16",
        "kaiko_vitb8",
        "kaiko_vitb16",
        "midnight",
        "openmidnight",
        "phikon",
        "phikon2",
        "uni",
        "uni2h",
        "virchow",
        "virchow2",
        "provgigapath",
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
        "dinov3vits16pretrainlvd1689m",
        "dinov3vitb16pretrainlvd1689m",
        "dinov3vitl16pretrainlvd1689m",
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
        "spider_breast",
        "spider_colorectal",
        "spider_skin",
        "spider_thorax",
        "tcga_crc_msi",
        "tcga_tils",
        "tcga_uniform",
        "wilds",
    ]


class UtilsConstants(Enum):
    DEFAULT_SEED = 0

    # Adapted from:
    # - https://github.com/mahmoodlab/CONCH/blob/main/prompts/crc100k_prompts_all_per_class.json#L64-L87
    # - https://github.com/MAGIC-AI4Med/KEEP/blob/573404dc768c627ee823f37753148f9ab1fe2769/training/path_training/data_proc_group.py#L37-L59
    # - https://github.com/lilab-stanford/MUSK/blob/fc9421aaebb2a3651fed5b69558c306f2836c228/benchmarks/clip_benchmark/datasets/histopathology_datasets.py#L69-L72
    # - https://github.com/LAION-AI/CLIP_benchmark/blob/5001237076a5d9a2662e366b73f1791b82ade1a1/clip_benchmark/datasets/en_zeroshot_classification_templates.json#L244-L247
    VLM_TEMPLATES = [
        "CLASSNAME.",
        "CLASSNAME is shown.",
        "CLASSNAME is present.",
        "CLASSNAME, H&E.",
        "CLASSNAME, H&E stain.",
        "shows CLASSNAME.",
        "presence of CLASSNAME.",
        "this is CLASSNAME.",
        "there is CLASSNAME.",
        "an example of CLASSNAME.",
        "an image of CLASSNAME.",
        "an image showing CLASSNAME.",
        "an H&E image of CLASSNAME.",
        "an H&E image showing CLASSNAME.",
        "an H&E stained image of CLASSNAME.",
        "an H&E stained image showing CLASSNAME.",
        "a histopathological image of CLASSNAME.",
        "a histopathological image showing CLASSNAME.",
        "a histopathology image of CLASSNAME.",
        "a histopathology image showing CLASSNAME.",
    ]

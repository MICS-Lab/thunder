import logging
import os

import pandas as pd

METRICS = [
    "accuracy",
    "balanced_accuracy",
    "f1",
    "jaccard",
    "roc_auc",
    "ECE",
    "MCE",
    "SCE",
    "ACE",
    "TACE",
]

TASK2CATS = {
    "adversarial_attack": ["adversarial", "clean", "drop"],
    "simple_shot": ["1", "2", "4", "8", "16"],
    "image_retrieval": ["1", "3", "5", "10"],
}

VAL_TYPES = ["metric_score", "ci_low", "ci_high"]

# Datasets used for benchmark means
CLS_DATASETS = [
    "bach",
    "bracs",
    "break_his",
    "ccrcc",
    "crc",
    "esca",
    "mhist",
    "patch_camelyon",
    "spider_breast",
    "spider_colorectal",
    "spider_skin",
    "spider_thorax",
    "wilds",
    "tcga_crc_msi",
    "tcga_tils",
    "tcga_uniform",
]

SEG_DATASETS = [
    "pannuke",
    "ocelot",
    "segpath_epithelial",
    "segpath_lymphocytes",
]

# Benchmark definitions: name -> (task, datasets, setting, list of metrics)
# Metrics and settings chosen to match the THUNDER leaderboards: https://mics-lab.github.io/thunder/leaderboards/
BENCHMARKS = {
    "benchmark_linear_probing": ("linear_probing", CLS_DATASETS, "", ["f1"]),
    "benchmark_calibration": ("linear_probing", CLS_DATASETS, "", ["ECE"]),
    "benchmark_knn": ("knn", CLS_DATASETS, "", ["f1"]),
    "benchmark_simple_shot": ("simple_shot", CLS_DATASETS, "16", ["f1"]),
    "benchmark_adversarial_attack": (
        "adversarial_attack",
        CLS_DATASETS,
        "drop",
        ["f1"],
    ),
    "benchmark_segmentation": ("segmentation", SEG_DATASETS, "", ["f1"]),
}


def extract_value_from_large_json(
    file_path: str, target_keys: list, val_types: list, categories: list = None
) -> dict:
    """
    Extracts values from a large JSON file using ijson.
    :param file_path: Path to the JSON file.
    :param target_keys: List of keys to extract values for.
    :param val_types: List of types of values to consider.
    :param categories: List of first-level keys (each pointing to a dict).

    :return: Dictionary with keys and their corresponding values.
    """

    import ijson

    if categories is None:
        values_dict = {
            key: {val_type: None for val_type in val_types} for key in target_keys
        }
    else:
        values_dict = {
            cat: {
                key: {val_type: None for val_type in val_types} for key in target_keys
            }
            for cat in categories
        }

    with open(file_path, "rb") as f:  # Open the file in binary mode
        parser = ijson.parse(f)
        current_key = None
        current_val_type = None
        if categories is not None:
            current_cat = None
        for _, event, value in parser:
            if categories is None:
                if event == "map_key" and value in target_keys:
                    current_key = value
                elif event == "map_key" and value in val_types:
                    current_val_type = value
                elif (
                    current_key is not None
                    and current_val_type is not None
                    and event
                    in [
                        "string",
                        "number",
                        "boolean",
                        "null",
                    ]
                ):
                    values_dict[current_key][current_val_type] = value
                    current_val_type = None
            else:
                if event == "map_key" and value in categories:
                    current_cat = value
                elif event == "map_key" and value in target_keys:
                    current_key = value
                elif event == "map_key" and value in val_types:
                    current_val_type = value
                elif (
                    current_key is not None
                    and current_val_type is not None
                    and event
                    in [
                        "string",
                        "number",
                        "boolean",
                        "null",
                    ]
                ):
                    values_dict[current_cat][current_key][current_val_type] = value
                    current_val_type = None

    return values_dict


def compute_benchmarks(df):
    """
    Compute aggregated benchmark mean rows, one set per model.

    For a given model, a benchmark mean is only computed when results are
    available for ALL datasets of the corresponding task, and only for
    adaptation=frozen. Any model/task missing one or more datasets is skipped
    rather than averaged over a partial set.

    The resulting benchmark rows are intended to match the numbers reported in
    the THUNDER leaderboards: https://mics-lab.github.io/thunder/leaderboards/

    :param df: DataFrame of per-dataset results.
    :return: DataFrame of aggregated benchmark rows.
    """

    bench_rows = []

    # Only consider frozen adaptation everywhere.
    frozen = df[df["adaptation"] == "frozen"]

    for model in sorted(frozen["model"].unique()):
        model_df = frozen[frozen["model"] == model]

        for bench_name, (task, datasets, setting, metrics) in BENCHMARKS.items():
            sub = model_df[
                (model_df["task"] == task) & (model_df["setting"] == setting)
            ]

            for metric in metrics:
                metric_sub = sub[sub["metric"] == metric]

                # Datasets present for this (task, setting, metric)
                present = set(metric_sub["dataset"].unique())
                required = set(datasets)

                # Only compute if ALL required datasets are available.
                if not required.issubset(present):
                    continue

                # Restrict to required datasets and average.
                metric_sub = metric_sub[metric_sub["dataset"].isin(datasets)]
                mean_score = round(metric_sub["metric_score"].mean(), 1)

                bench_rows.append(
                    {
                        "dataset": bench_name,
                        "model": model,
                        "task": task,
                        "adaptation": "frozen",
                        "metric": metric,
                        "metric_score": mean_score,
                        "ci_low": None,
                        "ci_high": None,
                        "setting": setting,
                    }
                )

    return pd.DataFrame(bench_rows)


def gather_results():
    import glob

    logging.info("Gathering results...")
    results_dir = os.path.join(os.environ["THUNDER_BASE_DATA_FOLDER"], "outputs", "res")
    results_files = glob.glob(f"{results_dir}/**/*.json", recursive=True)

    res = []
    for file in results_files:
        dataset, model, task, adaptation, _ = file.split("res/")[1].split("/")

        # Init base dict
        base_dict = {
            "dataset": dataset,
            "model": model,
            "task": task,
            "adaptation": adaptation,
        }

        # Extracting results
        if task in TASK2CATS.keys():
            categories = TASK2CATS[task]
            result_dicts = extract_value_from_large_json(
                file, METRICS, VAL_TYPES, categories
            )
        else:
            result_dicts = {
                "": extract_value_from_large_json(file, METRICS, VAL_TYPES),
            }

        # Populating rows of results
        for setting, result_dict in result_dicts.items():
            for metric in METRICS:
                metric_dict = base_dict.copy()
                metric_dict["metric"] = metric
                value_dict = result_dict[metric]
                write_line = True
                for val_type in value_dict.keys():
                    value = value_dict[val_type]
                    if value is not None:
                        value = round(100 * value, 1)
                    else:
                        write_line = False
                    metric_dict[val_type] = value

                if write_line:
                    metric_dict["setting"] = setting
                    res.append(metric_dict)

    df = pd.DataFrame(res)

    # Compute benchmark mean rows and prepend them to the top of the CSV.
    bench_df = compute_benchmarks(df)
    if not bench_df.empty:
        df = pd.concat([bench_df, df], ignore_index=True)

    df.to_csv(os.path.join(results_dir, "results.csv"), index=False)
    logging.info(f"Saved at: {os.path.join(results_dir, 'results.csv')}")
    logging.info(
        "The setting column corresponds to: (i) Adversarial/Clean/Drop for adversarial_attack, (ii) nb shots for simple_shot, (iii) k for image_retrieval. "
        "'metric_score' is the metric value for the considered test set, 'ci_low' and 'ci_high' are lower and upper bounds of 95% bootstrap confidence interval."
        "Rows with dataset starting by 'benchmark_' are aggregated means intended to reproduce the results reported in the THUNDER leaderboards: https://mics-lab.github.io/thunder/leaderboards/"
    )

#!/bin/bash
#SBATCH --job-name=thunder_eval
#SBATCH --output=outputs/slurm/%x_%A_%a.out
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --time=20:00:00
#SBATCH --array=0-19
#
# Usage: sbatch benchmark_all_tasks.sh <model_name>
#
# GPU memory: the segmentation datasets (array indices 16-19) require a GPU with
# at least 32 GB of VRAM. The classification datasets fit on smaller GPUs.

MODEL_NAME=$1
if [ -z "$MODEL_NAME" ]; then
    echo "Error: usage: sbatch benchmark_all_tasks.sh <model_name>"
    exit 1
fi
# --- Classification datasets (indices 0-15) ---
CLS_DATASETS=(
    "bach" "bracs" "break_his" "ccrcc" "crc" "esca" "mhist" "patch_camelyon"
    "spider_breast" "spider_colorectal" "spider_skin" "spider_thorax" "wilds"
    "tcga_crc_msi" "tcga_tils" "tcga_uniform"
)
# --- Segmentation datasets (indices 16-19) ---
SEG_DATASETS=(
    "pannuke" "ocelot" "segpath_epithelial" "segpath_lymphocytes"
)
ALL_DATASETS=("${CLS_DATASETS[@]}" "${SEG_DATASETS[@]}")
NUM_CLS=${#CLS_DATASETS[@]}


dataset=${ALL_DATASETS[$SLURM_ARRAY_TASK_ID]}
if [ "$SLURM_ARRAY_TASK_ID" -ge "$NUM_CLS" ]; then
    MODE="segmentation"
else
    MODE="classification"
fi

# --- Per-dataset adaptation epochs (segmentation only; empty = use default) ---
declare -A SEG_EPOCHS=(
    ["segpath_epithelial"]=9
    ["segpath_lymphocytes"]=21
)

# In case there is no internet connection (e.g. firewalled compute nodes),
# uncomment the two lines below to force HuggingFace/Transformers offline mode.
# Models/datasets must already downloaded.
#export HF_HUB_OFFLINE=1
#export TRANSFORMERS_OFFLINE=1

echo "=============================================="
echo " Running Task ID: ${SLURM_ARRAY_TASK_ID}"
echo " Model:           ${MODEL_NAME}"
echo " Mode:            ${MODE}"
echo " Dataset:         ${dataset}"
echo "=============================================="

# --- Pre-compute embeddings (needed for pre-loading tasks) ---
echo "+ thunder benchmark ${MODEL_NAME} ${dataset} pre_computing_embeddings"
thunder benchmark "${MODEL_NAME}" "${dataset}" pre_computing_embeddings

{ set +x; } 2>/dev/null
# --- Run tasks depending on inferred mode ---
if [ "$MODE" = "segmentation" ]; then
    EPOCHS_FLAG=""
    if [ -n "${SEG_EPOCHS[$dataset]}" ]; then
        EPOCHS_FLAG="--adaptation.epochs ${SEG_EPOCHS[$dataset]}"
    fi
    set -x
    thunder benchmark "${MODEL_NAME}" "${dataset}" segmentation --loading-mode=embedding_pre_loading ${EPOCHS_FLAG}
else
    set -x
    thunder benchmark "${MODEL_NAME}" "${dataset}" knn
    thunder benchmark "${MODEL_NAME}" "${dataset}" linear_probing --loading-mode=embedding_pre_loading
    thunder benchmark "${MODEL_NAME}" "${dataset}" simple_shot --loading-mode=embedding_pre_loading
    thunder benchmark "${MODEL_NAME}" "${dataset}" adversarial_attack
fi

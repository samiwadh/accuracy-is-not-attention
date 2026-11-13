# Accuracy Is Not Attention

Code and results for the paper **"Accuracy Is Not Attention: Confounders of Grad-CAM Comparisons Between Correct and Misclassified Medical Image Predictions"** (Abdul Sami, University of Milano-Bicocca, 2026).

The question: when Grad-CAM heatmaps of correct and misclassified predictions differ, does that show where the model looked, or how the analysis was done? Across four annotated datasets, two architectures and 15 trained models, the differences were explained by lesion size, typical lesion position, the explanation target and Grad-CAM's ReLU.

## What is in this repository

| Path | Content |
|---|---|
| `Accuracy_Is_Not_Attention_v5.ipynb` | The full analysis: data loading, training, evaluation, Grad-CAM, statistics, figures |
| `results/table_*_all_runs.csv` | All result tables used in the paper (one file per analysis, all runs) |
| `results/protocol_frozen.json` | SIIM-ACR analysis plan, stored with its SHA-256 hash before training |
| `paper/` | Manuscript (PDF and LaTeX) |
| `requirements.txt` | Python packages |

Per-image results and the trained models (27 checkpoints) are on Kaggle:
https://www.kaggle.com/datasets/samiwadho/accuracy-is-not-attention-grad-cam-artefacts

## Datasets

Images are **not** redistributed. Download them from the original sources and place them under `Dataset/`:

| Folder | Dataset | Used for |
|---|---|---|
| `Dataset/skin` | ISIC 2016 (Task 1 masks + Task 3 labels) | main analysis |
| `Dataset/chest_xray` | NIH ChestX-ray14, archives `images_001`, `images_002`, `Data_Entry_2017.csv`, `BBox_List_2017.csv` | main analysis |
| `Dataset/siim` | SIIM-ACR pneumothorax, PNG release (vbookshelf, Kaggle) | replication |
| `Dataset/brain_figshare` | figshare brain tumour dataset (Cheng et al.) | main analysis, DenseNet121 |
| `Dataset/brain` | Kaggle brain tumour MRI (Nickparvar) | classification only |
| `Dataset/histopathology` | BACH (ICIAR 2018) | classification only |

The notebook converts figshare and SIIM-ACR to PNG on first use and checks the masks visually.

## How to run

Tested on Windows 11, Python 3.9, TensorFlow 2.10 with an NVIDIA RTX 3050 (6 GB). TensorFlow above 2.10 does not use the GPU on native Windows.

1. Create the environment: `pip install -r requirements.txt` (plus CUDA 11.2 / cuDNN 8.1 for the GPU).
2. Put `resnet50_weights.h5` and `densenet121_weights_tf_dim_ordering_tf_kernels_notop.h5` (Keras ImageNet weights, no top) in the project folder.
3. Set `PROJECT_DIR` in the configuration cell.
4. In the first cell (the launcher) choose the runs, e.g. `RUN_ORDER = ["v3_skin", "v3_chest", "v2_main", "siim", "densenet_brain"]`, restart the kernel and run **only that cell**. It runs every other cell once per profile and combines the tables at the end. Do not use "Run All".

| Profile | Output folder | Content |
|---|---|---|
| `v3_skin` | `outputs/v3_strong_skin` | dermoscopy, ResNet50, 384 px |
| `v3_chest` | `outputs/v3_strong_chest` | ChestX-ray14, ResNet50 |
| `v2_main` | `outputs/v2_corrected` | brain MRI (main) + baseline models for all datasets |
| `siim` | `outputs/v5_siim` | SIIM-ACR replication |
| `densenet_brain` | `outputs/v5_densenet_brain` | brain MRI, DenseNet121 |

Each profile trains three seeds (42, 43, 44); finished checkpoints are reused on later runs.

## History

The analysis was corrected and extended several times (input scaling, unfreezing, held-out annotations, fixed explanation target, patient-level bootstrap, ReLU analysis, deletion test, SIIM-ACR, DenseNet121). Every change and its effect on the results is listed in Appendix E of the paper.

## Citation

See `CITATION.cff`.

## License

Code: see `LICENSE`. Datasets keep their original licences.

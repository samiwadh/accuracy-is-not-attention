# Accuracy Is Not Attention: Splits, Results and Weights

Companion dataset to the paper **"Accuracy Is Not Attention: Grad-CAM Lesion Localisation in Correct and Misclassified Predictions Across Medical Imaging Domains"** (Abdul Sami, University of Milano-Bicocca, 2026).

Code: [GitHub](GITHUB_LINK) · Paper: [preprint](PAPER_LINK)

## What this dataset contains

This dataset contains the **artefacts produced by the study**, not the raw medical images. The raw images belong to their original publishers; download them from the links below.

| Folder | Contents |
|---|---|
| `manifests/` | One CSV per dataset with the exact **train/val/test assignment** of every image, its patient or group ID, label and ground-truth reference. Paths are relative to the original dataset folders. |
| `tables/` | All paper tables (classification, localisation, seed consistency, border attention, pointing game), the exclusion/audit log and the run configuration (library versions, hyper-parameters). |
| `per_run/<dataset>/seed_<s>/` | For each of the 15 runs (5 datasets × seeds 42, 43, 44): test predictions with class probabilities, per-image Grad-CAM localisation metrics (energy inside the lesion, IoU at 5 thresholds, pointing game, border energy, centre-prior baseline), statistics, training log and checkpoint information. |
| `weights/<dataset>/seed_<s>/best.weights.h5` | Trained ResNet50 checkpoints (Keras/TensorFlow 2.10, weights only). Rebuild the model with `build_model()` from the GitHub notebook, then call `load_weights()`. |
| `figures/` | All paper figures. |

## Source datasets (download separately)

| Dataset | Source | Licence |
|---|---|---|
| ISIC 2016 (dermoscopy) | https://challenge.isic-archive.com/data/ | see source |
| Brain Tumor MRI (Nickparvar) | https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset | see source |
| Brain tumor dataset (Cheng et al., figshare) | https://figshare.com/articles/dataset/brain_tumor_dataset/1512427 | see source |
| NIH ChestX-ray14 (`images_001`, `images_002`) | https://nihcc.app.box.com/v/ChestXray-NIHCC | free use with citation |
| BACH / ICIAR 2018 (microscopy) | https://iciar2018-challenge.grand-challenge.org/ | CC BY-NC-ND 4.0 |

## How to use

- **Reuse the splits:** join `manifests/manifest_<dataset>.csv` on the `path` column with your local copy of the dataset.
- **Analyse the results without training:** `per_run/*/seed_*/localisation_per_sample.csv` holds one row per test image and explanation target.
- **Reproduce the paper:** place the weights under `outputs/v2_corrected/<dataset>/seed_<s>/` and run the GitHub notebook with `FORCE_RETRAIN = False`.

## Licence

Released under **CC BY-NC-SA 4.0** for non-commercial research use. The models were trained on datasets with non-commercial terms (e.g. BACH), so commercial use is not permitted. Please cite the paper and the original datasets.

## Citation

Sami, A. (2026). Accuracy Is Not Attention: Grad-CAM Lesion Localisation in Correct and Misclassified Predictions Across Medical Imaging Domains. Preprint. [DOI/link]

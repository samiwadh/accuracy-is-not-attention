# Accuracy Is Not Attention

**Grad-CAM lesion localisation in correct and misclassified predictions across medical imaging domains**

Abdul Sami · Department of Informatics, Systems and Communication, University of Milano-Bicocca, Milan, Italy

[Paper (preprint)](PAPER_LINK) · [Kaggle dataset: splits, results, weights]([KAGGLE_LINK](https://www.kaggle.com/datasets/samiwadho/accuracy-is-not-attention-grad-cam-artefacts)) · DOI: [ZENODO_DOI](ZENODO_LINK)

---

## Overview

Grad-CAM heatmaps are often shown on a few correctly classified images as evidence that a medical image classifier "looks at the right place". This repository asks two questions quantitatively:

1. **RQ1.** Does Grad-CAM lesion attention follow classification accuracy across imaging domains?
2. **RQ2.** Within a domain, does lesion attention differ between correctly classified and misclassified images *of the same class*?

An identical ImageNet-pretrained ResNet50 pipeline was trained with three seeds on five public datasets from four modalities. On the three datasets with expert localisation annotations, Grad-CAM was computed from logits for a fixed target and compared with a model-free centre-prior baseline.

## Main findings

| Finding | Evidence |
|---|---|
| Lesion attention is dissociated from accuracy | Brain MRI (figshare): balanced accuracy 0.880, but only about 4% of Grad-CAM energy inside the tumour (centre prior: 0.037) |
| Grad-CAM peaks miss lesions more often than a fixed centre point | Pointing game, correct predictions: skin 0.44–0.62 vs 0.99; chest 0.10–0.14 vs 0.24; brain 0.08–0.10 vs 0.12 |
| Missed malignant skin lesions receive less lesion attention | Pooled Δ = −0.205, 95% CI [−0.282, −0.129], same sign in all 3 seeds |
| No "correct region, wrong class" pattern | Chest: Δ = −0.006 [−0.051, 0.042]; brain MRI: sign inconsistent across seeds |
| Missed findings attend more to image borders (exploratory) | Chest: Δ border energy +0.085 to +0.091, all seeds |
| An uncorrected pipeline produced a spurious 24× effect | See paper §5.5 and Table 7 |

## Datasets

The raw datasets are **not** redistributed here. Download them from the original sources under their own licences, and place them as shown in [Folder layout](#folder-layout).

| Folder | Dataset | Source | What was used | Accessed | Licence |
|---|---|---|---|---|---|
| `skin` | ISIC 2016 (ISBI challenge), Part 3B + Part 1 masks | https://challenge.isic-archive.com/data/ | 900 train + 379 test images, all with masks | Jul 2026 | see source (verify) |
| `brain` | Brain Tumor MRI Dataset (M. Nickparvar) | https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset | Release with 7,200 images (Training/Testing) | Jun 2026 | see Kaggle page |
| `brain_figshare` | Brain tumor dataset (J. Cheng et al.) | https://figshare.com/articles/dataset/brain_tumor_dataset/1512427 | 3,064 slices, 233 patients, tumour masks | Oct 2026 | see figshare page |
| `chest_xray` | NIH ChestX-ray14 | https://nihcc.app.box.com/v/ChestXray-NIHCC | Archive parts `images_001` + `images_002` (14,999 images, patients 1–3923), `Data_Entry_2017.csv`, `BBox_List_2017.csv` | Jul 2026 | NIH: free use with citation |
| `histopathology` | BACH, ICIAR 2018 (microscopy "Photos") | https://iciar2018-challenge.grand-challenge.org/ | 399 images; original `.tif` converted losslessly to `.png` | Jul 2026 | CC BY-NC-ND 4.0 |

> The Kaggle brain collection includes figshare images, so the two brain experiments are separate tasks, not independent domains.

### Folder layout

```
Dataset/
├── skin/
│   ├── Train/ ISBI2016_ISIC_Part3B_Training_Data/, ISBI2016_ISIC_Part3B_Training_GroundTruth.csv,
│   │          ISBI2016_ISIC_Part1_Training_GroundTruth/
│   └── Test/  ISBI2016_ISIC_Part3B_Test_Data/, ISBI2016_ISIC_Part3B_Test_GroundTruth.csv,
│              ISBI2016_ISIC_Part1_Test_GroundTruth/
├── brain/           Training/{glioma,meningioma,notumor,pituitary}/  Testing/{...}/
├── brain_figshare/  mat/*.mat   (converted to png/ by prepare_brain_figshare() in the notebook)
├── chest_xray/      images/*.png  Data_Entry_2017.csv  BBox_List_2017.csv
└── histopathology/  Photos/{Normal,Benign,InSitu,Invasive}/*.png
```

## Repository structure

```
├── notebooks/Cross_Domain_GradCAM_v2_FINAL.ipynb   # full pipeline, cells 1–14
├── results/        # tables, manifests (data splits), exclusion log, run configuration
├── figures/        # all paper figures
├── paper/          # manuscript (LaTeX + PDF)
├── kaggle/         # metadata for the Kaggle artefact dataset
├── prepare_release.py   # builds results/ and the Kaggle folder from outputs/, with relative paths
├── requirements.txt
└── CITATION.cff
```

## Reproducing the results

**Environment used:** Windows 10, Python 3.9.25, TensorFlow 2.10.0, NVIDIA RTX 3050 Laptop GPU (6 GB). Exact versions are in `results/run_config.json`.

```bash
pip install -r requirements.txt
```

1. Download the datasets into `Dataset/` (see above) and the Keras ResNet50 ImageNet *notop* weights file as `resnet50_weights.h5`.
2. Open the notebook and set `PROJECT_DIR` in **Cell 1**.
3. For figshare, run `prepare_brain_figshare()` once (needs `h5py`), then check the mask overlay cell.
4. Run all cells in order.

| Cell | Purpose | Training? |
|---|---|---|
| 1–9 | Configuration, data loading and auditing, model, training, evaluation, Grad-CAM and statistics functions | no |
| **10** | Trains 5 datasets × 3 seeds, evaluates, runs Grad-CAM. `FORCE_RETRAIN = False` re-uses saved checkpoints | **yes (~7 h)** |
| 11, 11a, 11b | Aggregation, seed consistency, pooled endpoint | no |
| 12 | Figures | no |
| 14 | Final paper numbers, class-split border analysis, Fig. 2. Run after Cell 12 | no |

Every number in the paper is produced by these cells and saved under `outputs/v2_corrected/`. Nothing is typed by hand.

**Pre-trained weights.** To skip training, download the 15 checkpoints from the [Kaggle dataset](KAGGLE_LINK), place them in `outputs/v2_corrected/<domain>/seed_<s>/best.weights.h5`, and run with `FORCE_RETRAIN = False`.

## Method summary

- **Model:** ResNet50 (ImageNet), GAP → BatchNorm → Dropout 0.4 → Dense logits. Stage 1 trains the head only; Stage 2 unfreezes the conv5 stage with BatchNorm frozen. The checkpoint with the lowest validation loss is used for everything. Seeds 42, 43, 44 on a fixed split.
- **Splits:** patient-level wherever patient IDs exist (chest, figshare). All chest bounding-box patients are held out in the test set. Exact and near-duplicate audits are run for the Kaggle brain set.
- **Grad-CAM:** computed from logits with a fixed target (positive-class margin, or the true-class logit), from `conv5_block3_out`.
- **Primary endpoint:** share of Grad-CAM energy inside the lesion, declared in advance. Secondary: IoU at τ = 0.3–0.7 and the pointing game. Baselines: centre prior and uniform map.
- **Statistics:** comparisons within the same true class; bootstrap 95% CIs, Mann–Whitney U, permutation test, Cliff's δ, Holm correction; per-seed results plus an image-level pooled bootstrap.

## Citation

```bibtex
@misc{sami2026accuracy,
  author = {Sami, Abdul},
  title  = {Accuracy Is Not Attention: Grad-CAM Lesion Localisation in Correct and
            Misclassified Predictions Across Medical Imaging Domains},
  year   = {2026},
  note   = {Preprint. Code: https://github.com/samiwadh/accuracy-is-not-attention}
}
```

Please also cite the original datasets: Gutman et al. 2016 (ISIC), Nickparvar 2021, Cheng et al. 2015, Wang et al. 2017 (ChestX-ray14), Aresta et al. 2019 (BACH).

## Licence

Code: MIT (see `LICENSE`). The datasets keep their original licences; this repository does not redistribute them.

## Contact

Abdul Sami · a.sami7@campus.unimib.it

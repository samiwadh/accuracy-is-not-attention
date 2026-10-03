"""Build the shareable release from outputs/v2_corrected/.

Creates two folders next to this script:
  results/            small files for GitHub (tables, manifests, logs, config)
  kaggle_upload/      everything for the Kaggle artefact dataset (+ optional weights)

All absolute Windows paths inside CSV files (column 'path' and 'gt_ref') are
rewritten as paths relative to the Dataset folder, e.g. 'chest_xray/images/00000001_000.png'.
This removes your personal folder names and makes the files usable on any computer.
No raw images are copied.
"""
import os, glob, shutil, json
import pandas as pd

PROJECT_DIR = r"D:\01 Research work\Papar\0 Project\1 Cross-Domain Explanation Degradation Study\Source code"
OUTPUT_DIR = os.path.join(PROJECT_DIR, "outputs", "v2_corrected")
BASE_DIR = os.path.join(PROJECT_DIR, "Dataset")
INCLUDE_WEIGHTS = True          # 15 x ~95 MB; Kaggle only (never GitHub)

HERE = os.path.dirname(os.path.abspath(__file__))
GH = os.path.join(HERE, "results")
KG = os.path.join(HERE, "kaggle_upload")
PATH_COLS = ("path", "gt_ref")


def to_relative(value):
    if not isinstance(value, str) or not value:
        return value
    try:
        rel = os.path.relpath(value, BASE_DIR)
    except ValueError:                      # different drive on Windows
        return value
    return rel.replace("\\", "/") if not rel.startswith("..") else value


def copy_csv(src, dst):
    df = pd.read_csv(src)
    for c in PATH_COLS:
        if c in df.columns:
            df[c] = df[c].map(to_relative)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    df.to_csv(dst, index=False)
    leftover = [c for c in PATH_COLS if c in df.columns and df[c].astype(str).str.contains(r"[A-Za-z]:\\", regex=True).any()]
    if leftover:
        print(f"  WARNING: absolute paths remain in {dst} ({leftover})")


def copy_any(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if src.endswith(".csv"):
        copy_csv(src, dst)
    else:
        shutil.copy2(src, dst)


def main():
    for d in (GH, KG):
        if os.path.exists(d):
            shutil.rmtree(d)
    # top-level tables, manifests, logs, config and figures
    for f in sorted(glob.glob(os.path.join(OUTPUT_DIR, "*"))):
        if os.path.isdir(f):
            continue
        name = os.path.basename(f)
        sub = "figures" if name.endswith(".png") else ("manifests" if name.startswith("manifest_") else "tables")
        copy_any(f, os.path.join(KG, sub, name))
        if not name.endswith(".png"):
            copy_any(f, os.path.join(GH, sub, name))
    # per-domain, per-seed results
    n_w = 0
    for seed_dir in sorted(glob.glob(os.path.join(OUTPUT_DIR, "*", "seed_*"))):
        domain, seed = seed_dir.split(os.sep)[-2:]
        for f in sorted(glob.glob(os.path.join(seed_dir, "*"))):
            name = os.path.basename(f)
            if name.endswith(".h5"):
                if INCLUDE_WEIGHTS:
                    copy_any(f, os.path.join(KG, "weights", domain, seed, name)); n_w += 1
                continue
            copy_any(f, os.path.join(KG, "per_run", domain, seed, name))
    # the run config contains your local paths only indirectly; keep env + cfg only
    cfg = os.path.join(OUTPUT_DIR, "run_config.json")
    if os.path.exists(cfg):
        with open(cfg) as fh:
            j = json.load(fh)
        for d in (GH, KG):
            with open(os.path.join(d, "tables", "run_config.json"), "w") as fh:
                json.dump(j, fh, indent=2)
    size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(KG) for f in fs) / 1e6
    print(f"GitHub results/: {sum(len(fs) for _, _, fs in os.walk(GH))} files")
    print(f"Kaggle upload: {sum(len(fs) for _, _, fs in os.walk(KG))} files, {n_w} weight files, {size:.0f} MB")


if __name__ == "__main__":
    main()

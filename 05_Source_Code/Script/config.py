"""
config.py — Pusat konfigurasi & reproduktibilitas.
Semua seed, path, skema split, dan parameter terpusat di sini.

Replikasi paper:
  Pratiwi, I.Y.R., Asmara, R.A., Rahutomo, F. (2017).
  "Study of hoax news detection using naive bayes classifier in
   Indonesian language." ICTS 2017. DOI: 10.1109/ICTS.2017.8265649
Dataset: Indonesian Hoax News Detection (Mendeley, CC BY 4.0)
         DOI: 10.17632/p3hfgr5j3m.1  — file "600 news with valid hoax label.csv"
"""

from pathlib import Path
import os, random

SEED = 42

ROOT = Path(__file__).resolve().parent          # .../05_Source_Code/Script
SRC = ROOT.parent                                # .../05_Source_Code
PROJECT = SRC.parent                             # .../Abiansyah_UAS_AI

DATA_RAW = PROJECT / "04_Dataset" / "Raw_Dataset"
DATA_PROCESSED = PROJECT / "04_Dataset" / "Processed_Dataset"
MODEL_DIR = PROJECT / "06_Model"
RESULT_DIR = PROJECT / "07_Hasil_Eksperimen"
VIZ_DIR = PROJECT / "08_Visualisasi"

# Skema training-testing sesuai paper (train ratio)
SPLIT_SCHEMES = {"60-40": 0.60, "70-30": 0.70, "80-20": 0.80}

# Kandidat nama kolom (file Mendeley bisa beda penamaan)
TEXT_CANDIDATES = ["berita", "news", "text", "isi", "content", "judul", "title", "Headline"]
LABEL_CANDIDATES = ["tagging", "label", "hoax", "valid", "class", "kategori", "Label"]

# TF-IDF
TFIDF_PARAMS = dict(lowercase=True, max_features=5000, ngram_range=(1, 1))

# Naive Bayes (metode usulan/paper) — alpha akan dicari (paper memakai tuning alpha)
NB_ALPHA_GRID = [0.01, 0.1, 0.5, 1.0]

# Baseline pembanding
# SVM linear & Logistic Regression


def set_seed(seed: int = SEED):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass


def ensure_dirs():
    for d in (DATA_PROCESSED, MODEL_DIR, RESULT_DIR, VIZ_DIR):
        d.mkdir(parents=True, exist_ok=True)

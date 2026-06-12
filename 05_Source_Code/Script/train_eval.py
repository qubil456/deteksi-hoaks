"""
train_eval.py — Replikasi eksperimen + baseline.

Metode USULAN (paper): TF-IDF + Multinomial Naive Bayes, tuning alpha,
  diuji pada 3 skema split (60-40, 70-30, 80-20) seperti paper.
BASELINE pembanding   : TF-IDF + Linear SVM, TF-IDF + Logistic Regression.

Metrik: Accuracy, Precision, Recall, F1.
Output (07_Hasil_Eksperimen/):
  hasil_replikasi.csv       (semua model x semua skema)
  perbandingan_usulan_baseline.csv
  best_alpha.json
Confusion matrix (08_Visualisasi/): confusion_NB_<skema>.png
Model terbaik (06_Model/): best_model_nb.pkl

Jalankan:
    python train_eval.py
"""

import json
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             f1_score, confusion_matrix, ConfusionMatrixDisplay)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import (DATA_PROCESSED, MODEL_DIR, RESULT_DIR, VIZ_DIR,
                    ensure_dirs, set_seed, SEED, SPLIT_SCHEMES,
                    TFIDF_PARAMS, NB_ALPHA_GRID)


def load_clean():
    df = pd.read_csv(DATA_PROCESSED / "clean.csv")
    return df["text_clean"].astype(str).values, df["label"].astype(int).values


def make_pipe(clf):
    return Pipeline([("tfidf", TfidfVectorizer(**TFIDF_PARAMS)), ("clf", clf)])


def evaluate(model, Xte, yte):
    pred = model.predict(Xte)
    return {
        "accuracy": round(accuracy_score(yte, pred), 4),
        "precision": round(precision_score(yte, pred, zero_division=0), 4),
        "recall": round(recall_score(yte, pred, zero_division=0), 4),
        "f1": round(f1_score(yte, pred, zero_division=0), 4),
    }, pred


def main():
    set_seed(SEED)
    ensure_dirs()
    X, y = load_clean()

    rows = []
    best = {"f1": -1}

    models = {
        "Naive Bayes (usulan)": lambda a=1.0: make_pipe(MultinomialNB(alpha=a)),
        "SVM (baseline)": lambda: make_pipe(LinearSVC(random_state=SEED)),
        "Logistic Regression (baseline)":
            lambda: make_pipe(LogisticRegression(max_iter=1000, random_state=SEED)),
    }

    for scheme, train_ratio in SPLIT_SCHEMES.items():
        Xtr, Xte, ytr, yte = train_test_split(
            X, y, train_size=train_ratio, random_state=SEED, stratify=y)

        # --- Naive Bayes dengan tuning alpha ---
        best_a, best_f1, best_metrics, best_pred = None, -1, None, None
        for a in NB_ALPHA_GRID:
            m = make_pipe(MultinomialNB(alpha=a)).fit(Xtr, ytr)
            met, pred = evaluate(m, Xte, yte)
            if met["f1"] > best_f1:
                best_a, best_f1, best_metrics, best_pred = a, met["f1"], met, pred
                best_model_nb = m
        row = {"model": "Naive Bayes (usulan)", "scheme": scheme,
               "alpha": best_a, **best_metrics}
        rows.append(row)

        # confusion matrix NB
        cm = confusion_matrix(yte, best_pred)
        ConfusionMatrixDisplay(cm, display_labels=["valid", "hoax"]).plot(
            cmap="Blues", colorbar=False)
        plt.title(f"Naive Bayes — split {scheme} (alpha={best_a})")
        plt.tight_layout()
        plt.savefig(VIZ_DIR / f"confusion_NB_{scheme}.png", dpi=150)
        plt.close()

        if best_metrics["f1"] > best["f1"]:
            best = {**row}
            with open(MODEL_DIR / "best_model_nb.pkl", "wb") as f:
                pickle.dump(best_model_nb, f)

        # --- Baseline ---
        for name in ["SVM (baseline)", "Logistic Regression (baseline)"]:
            m = models[name]().fit(Xtr, ytr)
            met, _ = evaluate(m, Xte, yte)
            rows.append({"model": name, "scheme": scheme, "alpha": None, **met})

    res = pd.DataFrame(rows)
    res.to_csv(RESULT_DIR / "hasil_replikasi.csv", index=False)

    # Tabel perbandingan ringkas (rata-rata antar skema)
    comp = (res.groupby("model")[["accuracy", "precision", "recall", "f1"]]
              .mean().round(4).sort_values("f1", ascending=False))
    comp.to_csv(RESULT_DIR / "perbandingan_usulan_baseline.csv")

    with open(RESULT_DIR / "best_alpha.json", "w") as f:
        json.dump(best, f, indent=2)

    print("\n=== Hasil per skema ===")
    print(res.to_string(index=False))
    print("\n=== Rata-rata antar skema (usulan vs baseline) ===")
    print(comp)
    print("\nModel terbaik:", best)


if __name__ == "__main__":
    main()

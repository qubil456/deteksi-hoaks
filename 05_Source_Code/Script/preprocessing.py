"""
preprocessing.py — Memuat dataset hoaks (Mendeley), membersihkan teks
Indonesia, dan menyiapkannya untuk TF-IDF.

Output: Processed_Dataset/clean.csv  (kolom: text_clean, label  [1=hoax,0=valid])

Jalankan:
    python preprocessing.py
"""

import re
import json
import pandas as pd

from config import (DATA_RAW, DATA_PROCESSED, ensure_dirs,
                    TEXT_CANDIDATES, LABEL_CANDIDATES, set_seed, SEED)

# Stopword Indonesia ringkas (tanpa dependensi eksternal).
# Untuk hasil lebih baik, bisa diganti Sastrawi: pip install Sastrawi
STOPWORDS_ID = set("""
yang di ke dari dan atau untuk pada dengan dalam adalah ini itu akan tidak
ada para juga sudah saya kami kita mereka dia ia nya the a an oleh sebagai
karena agar bahwa namun tetapi jika maka saat ketika telah masih bisa dapat
""".split())


def find_csv() -> "Path":
    # Prioritaskan file 600; fallback ke csv pertama
    prefer = list(DATA_RAW.glob("*600*.csv"))
    if prefer:
        return prefer[0]
    csvs = sorted(DATA_RAW.glob("*.csv"))
    if not csvs:
        raise FileNotFoundError(
            "Tidak ada CSV di Raw_Dataset/. Unduh dari Mendeley "
            "(lihat Dataset_Source.txt) dan letakkan di sana."
        )
    return csvs[0]


def pick_col(cols, candidates):
    low = {c.lower().strip(): c for c in cols}
    for cand in candidates:
        if cand.lower() in low:
            return low[cand.lower()]
    return None


def load_raw() -> pd.DataFrame:
    path = find_csv()
    # Dataset Mendeley ini: separator ';', encoding cp1252. Coba beberapa kombinasi.
    attempts = [
        dict(sep=";", encoding="cp1252"),
        dict(sep=";", encoding="latin-1"),
        dict(sep=",", encoding="utf-8"),
        dict(sep=";", encoding="utf-8-sig"),
    ]
    df = None
    for opt in attempts:
        try:
            tmp = pd.read_csv(path, engine="python", **opt)
            if tmp.shape[1] >= 2:
                df = tmp
                break
        except Exception:
            continue
    if df is None:
        df = pd.read_csv(path, sep=";", encoding="latin-1", engine="python")
    print(f"Dataset dimuat: {path.name}  shape={df.shape}")
    print("Kolom:", list(df.columns))
    return df


def to_label_binary(series: pd.Series) -> pd.Series:
    """Ubah label hoax/valid (teks atau angka) ke 1=hoax, 0=valid."""
    def m(v):
        s = str(v).strip().lower()
        if s in {"1", "hoax", "hoaks", "fake", "palsu"}:
            return 1
        if s in {"0", "valid", "real", "asli", "benar", "non-hoax", "nonhoax"}:
            return 0
        # angka >0 dianggap hoax
        try:
            return 1 if float(s) > 0 else 0
        except ValueError:
            return None
    return series.map(m)


def clean_text(t: str) -> str:
    t = str(t).lower()
    t = re.sub(r"http\S+|www\.\S+", " ", t)        # URL
    t = re.sub(r"[^a-z\s]", " ", t)                # simbol & angka
    t = re.sub(r"\s+", " ", t).strip()
    tokens = [w for w in t.split() if w not in STOPWORDS_ID and len(w) > 2]
    return " ".join(tokens)


def main():
    set_seed(SEED)
    ensure_dirs()
    df = load_raw()

    tcol = pick_col(df.columns, TEXT_CANDIDATES)
    lcol = pick_col(df.columns, LABEL_CANDIDATES)
    if tcol is None or lcol is None:
        # fallback: kolom pertama = teks, terakhir = label
        tcol = tcol or df.columns[0]
        lcol = lcol or df.columns[-1]
    print(f"Kolom teks  : '{tcol}'")
    print(f"Kolom label : '{lcol}'")

    out = pd.DataFrame()
    out["text_clean"] = df[tcol].map(clean_text)
    out["label"] = to_label_binary(df[lcol])

    before = len(out)
    out = out.dropna(subset=["label"])
    out = out[out["text_clean"].str.len() > 0]
    out["label"] = out["label"].astype(int)
    print(f"Baris valid: {len(out)}/{before}")
    print("Distribusi label:", dict(out["label"].value_counts()))

    out.to_csv(DATA_PROCESSED / "clean.csv", index=False)

    info = {
        "n_rows": int(len(out)),
        "n_hoax": int((out.label == 1).sum()),
        "n_valid": int((out.label == 0).sum()),
        "text_col_source": tcol,
        "label_col_source": lcol,
    }
    with open(DATA_PROCESSED / "clean_info.json", "w") as f:
        json.dump(info, f, indent=2)
    print("Tersimpan: clean.csv +", info)


if __name__ == "__main__":
    main()

"""
predict.py — CLI sederhana untuk mendeteksi hoaks dari teks atau file.

Contoh:
  python predict.py --text "Ini adalah berita uji coba."
  python predict.py --file ../sample.txt
"""

import argparse
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from preprocessing import clean_text
from config import MODEL_DIR, set_seed, SEED

MODEL_PATH = MODEL_DIR / "best_model_nb.pkl"
LABEL_MAP = {0: "Valid", 1: "Hoax"}


def load_model() -> object:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model tidak ditemukan di {MODEL_PATH}. Jalankan train_eval.py terlebih dahulu."
        )
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict_text(text: str, model: object) -> dict:
    clean = clean_text(text)
    if not clean:
        return {"error": "Teks tidak valid setelah preprocessing."}

    pred = model.predict([clean])[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        try:
            prob = model.predict_proba([clean])[0]
            confidence = float(prob[pred])
        except Exception:
            confidence = None

    return {
        "clean_text": clean,
        "prediction": LABEL_MAP.get(pred, str(pred)),
        "confidence": confidence,
        "raw_label": int(pred),
    }


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")
    return path.read_text(encoding="utf-8").strip()


def cli() -> None:
    parser = argparse.ArgumentParser(
        description="Prediksi berita hoaks bahasa Indonesia menggunakan model TF-IDF + NB"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", "-t", help="Teks berita untuk diprediksi.")
    group.add_argument("--file", "-f", type=Path, help="File teks (.txt) yang akan diprediksi.")
    args = parser.parse_args()

    set_seed(SEED)
    model = load_model()

    if args.file:
        text = read_text_file(args.file)
    else:
        text = args.text

    result = predict_text(text, model)
    if "error" in result:
        print("ERROR:", result["error"])
        sys.exit(1)

    print("=== Hasil Prediksi ===")
    print("Prediksi        :", result["prediction"])
    if result["confidence"] is not None:
        print(f"Kepercayaan     : {result['confidence']:.2%}")
    print("Teks preprocessing:")
    print(result["clean_text"])


if __name__ == "__main__":
    cli()

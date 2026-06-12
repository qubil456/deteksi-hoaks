"""
Streamlit app — Improved UI for Indonesian hoax news detection.

Run:
  cd 05_Source_Code
  .venv\Scripts\Activate.ps1  (or activate venv)
  python -m streamlit run Script/app.py --server.headless true
"""

import json
import pickle
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent
from config import MODEL_DIR, VIZ_DIR, DATA_PROCESSED, set_seed, SEED
from preprocessing import clean_text

MODEL_PATH = MODEL_DIR / "best_model_nb.pkl"
LABEL_MAP = {0: "Valid", 1: "Hoax"}


def load_model():
    if not MODEL_PATH.exists():
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict_text(text: str, model) -> dict:
    clean = clean_text(text)
    if not clean:
        return {"error": "Teks tidak valid setelah preprocessing. Masukkan teks yang lebih panjang."}
    pred = model.predict([clean])[0]
    confidence = None
    if hasattr(model, "predict_proba"):
        try:
            prob = model.predict_proba([clean])[0]
            confidence = float(prob[pred])
        except Exception:
            confidence = None
    return {"clean_text": clean, "prediction": LABEL_MAP.get(pred, str(pred)), "confidence": confidence}


def load_stats():
    info_path = DATA_PROCESSED / "clean_info.json"
    if info_path.exists():
        with open(info_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def main():
    set_seed(SEED)
    st.set_page_config(page_title="Deteksi Hoaks — Indonesia", page_icon="📰", layout="wide")

    # Sidebar
    with st.sidebar:
        st.header("Deteksi Hoaks")
        st.write("TF-IDF + Multinomial NB — replikasi penelitian")
        st.markdown("---")
        stats = load_stats()
        if stats:
            st.metric("Baris data", stats.get("n_rows"))
            st.metric("Hoax", stats.get("n_hoax"))
            st.metric("Valid", stats.get("n_valid"))
        else:
            st.info("Dataset belum diproses. Jalankan `preprocessing.py` jika perlu.")
        st.markdown("---")
        st.write("**Petunjuk singkat:**")
        st.write("Masukkan teks berita di kotak utama lalu tekan *Prediksi*. Hasil menunjukkan label dan (jika tersedia) confidence.")
        st.write("Model tersimpan di `06_Model/best_model_nb.pkl`.")

    # Main layout
    st.title("Deteksi Berita Hoaks — Bahasa Indonesia")
    st.subheader("Masukkan teks berita untuk dianalisis")

    model = load_model()
    col1, col2 = st.columns([2, 1])

    with col1:
        text = st.text_area("Teks berita", height=300, placeholder="Tempel berita atau paragraf di sini...")
        btn = st.button("Prediksi", use_container_width=True)

    with col2:
        st.markdown("**Contoh singkat:**")
        st.write("- Pemerintah mengumumkan...\n- Penelitian terbaru menunjukkan...\n- Berita viral mengatakan...")
        st.markdown("---")
        st.write("**Preview dataset (processed)**")
        csv_path = DATA_PROCESSED / "clean.csv"
        if csv_path.exists():
            try:
                import pandas as pd

                df = pd.read_csv(csv_path)
                st.dataframe(df.sample(min(5, len(df))).reset_index(drop=True))
            except Exception:
                st.write("Preview tidak tersedia")
        else:
            st.write("Tidak ada `clean.csv`")

    if btn:
        if not text or not text.strip():
            st.warning("Masukkan beberapa kalimat berita terlebih dahulu.")
        elif model is None:
            st.error("Model tidak ditemukan. Jalankan `train_eval.py` untuk membuat model.")
        else:
            with st.spinner("Sedang memprediksi..."):
                res = predict_text(text, model)
            if "error" in res:
                st.error(res["error"])
            else:
                st.success(f"Prediksi: {res['prediction']}")
                if res["confidence"] is not None:
                    st.info(f"Kepercayaan model: {res['confidence']:.2%}")
                st.markdown("---")
                st.write("**Teks setelah preprocessing:**")
                st.write(res["clean_text"]) 

    st.markdown("---")
    st.caption("Aplikasi ini adalah replikasi penelitian — gunakan hasil dengan kehati-hatian akademis.")


if __name__ == "__main__":
    main()

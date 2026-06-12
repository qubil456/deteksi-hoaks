# 📋 BUKTI DEPLOYMENT APLIKASI DETEKSI HOAKS

## 1. URL APLIKASI (Streamlit Cloud)

**Live Application URL:**
```
https://deteksi-hoaks-9egqrns2d2bdyhv5sb7tv.streamlit.app
```

**GitHub Repository:**
```
https://github.com/qubil456/deteksi-hoaks.git
```

---

## 2. DOKUMENTASI PENGGUNAAN

### Cara Menggunakan Aplikasi Web

1. **Buka aplikasi:** https://deteksi-hoaks-9egqrns2d2bdyhv5sb7tv.streamlit.app
2. **Sidebar kiri** menampilkan:
   - Informasi model: TF-IDF + Multinomial Naive Bayes
   - Statistik dataset (600 berita: 228 hoax, 372 valid)
   - Petunjuk penggunaan

3. **Area utama:**
   - Masukkan teks berita di kotak input
   - Klik tombol "Prediksi"
   - Lihat hasil prediksi (Valid/Hoax) dan confidence score

4. **Panel kanan:**
   - Contoh input teks
   - Preview sampel dataset

### Contoh Hasil Prediksi

- **Input:** "Pemerintah mengumumkan program bantuan sosial baru..."
- **Hasil:** "Prediksi: Valid" dengan confidence tinggi

---

## 3. FITUR APLIKASI

✅ **Interface Streamlit** yang user-friendly  
✅ **Sidebar informatif** dengan statistik dataset  
✅ **Preview dataset** (sampel 5 baris)  
✅ **Prediksi real-time** dengan confidence score  
✅ **Preprocessing otomatis** (stopword removal, URL cleaning)  
✅ **Fallback training** jika model pickle tidak tersedia  
✅ **Error handling** yang robust  

---

## 4. TEKNOLOGI STACK

| Komponen | Technology |
|----------|-----------|
| Framework | Streamlit |
| ML Algorithm | TF-IDF + Multinomial Naive Bayes |
| Language | Python 3.11 |
| Dataset | Indonesian Hoax News (600 samples) |
| Deployment | Streamlit Community Cloud |
| Repository | GitHub |
| Container | Docker (optional) |

---

## 5. STRUKTUR FOLDER DEPLOYMENT

```
deteksi-hoaks/
├── 05_Source_Code/
│   ├── Script/
│   │   ├── app.py                    # Main Streamlit app
│   │   ├── config.py                 # Configuration & paths
│   │   ├── preprocessing.py          # Data preprocessing
│   │   ├── train_eval.py             # Model training & evaluation
│   │   └── predict.py                # CLI prediction tool
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile                    # Docker image definition
├── 04_Dataset/
│   ├── Raw_Dataset/                  # Original dataset
│   └── Processed_Dataset/
│       ├── clean.csv                 # Processed data
│       └── clean_info.json           # Dataset metadata
├── 06_Model/
│   └── best_model_nb.pkl            # Trained model
├── 07_Hasil_Eksperimen/
│   ├── hasil_replikasi.csv          # Experiment results
│   ├── perbandingan_usulan_baseline.csv
│   └── best_alpha.json              # Best hyperparameter
├── requirements.txt                  # Root dependencies (for Cloud)
└── README.md                         # Project documentation
```

---

## 6. SETUP LOKAL (Testing)

### Prerequisites
- Python 3.11+
- Git
- Virtual environment

### Steps

```bash
# 1. Clone repository
git clone https://github.com/qubil456/deteksi-hoaks.git
cd deteksi-hoaks

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit app
cd 05_Source_Code
python -m streamlit run Script/app.py --server.headless true --server.port 8501

# 5. Open browser
# Navigate to http://localhost:8501
```

### CLI Usage

```bash
# Single prediction
python 05_Source_Code/Script/predict.py --text "Contoh berita untuk dianalisis"

# Batch prediction from file
python 05_Source_Code/Script/predict.py --file berita.txt
```

---

## 7. DEPLOYMENT OPTIONS

### Option A: Streamlit Community Cloud (✅ DEPLOYED)
- Repository: `qubil456/deteksi-hoaks` (GitHub)
- Branch: `main`
- App file: `05_Source_Code/Script/app.py`
- Status: **LIVE** ✅

### Option B: Docker Deployment

```bash
cd 05_Source_Code
docker build -t hoax-detector:latest -f Dockerfile .
docker run -p 8501:8501 hoax-detector:latest
```

### Option C: Cloud Platforms (Render/Railway/Heroku)
- Gunakan `start command`:
  ```
  python -m streamlit run 05_Source_Code/Script/app.py --server.headless true --server.port $PORT
  ```

---

## 8. MODEL DETAILS

| Attribute | Value |
|-----------|-------|
| Algorithm | Multinomial Naive Bayes (α=0.1) |
| Vectorizer | TF-IDF (max_features=5000, unigram) |
| Dataset Size | 600 samples |
| Hoax/Valid | 228 / 372 (balanced) |
| Accuracy | ~72.8% |
| Precision | ~61.7% |
| Recall | ~68.7% |
| F1-Score | ~65.2% |

---

## 9. CATATAN TEKNIS

### Error Handling
- ✅ Automatic model retraining jika `best_model_nb.pkl` hilang
- ✅ CSV fallback preprocessing jika dataset corrupt
- ✅ Graceful error messages untuk user

### Performance
- ✅ Sub-1 second prediction time
- ✅ ~50KB model size
- ✅ Streamlit lazy caching untuk efficiency

### Security
- ✅ No sensitive data in logs
- ✅ Input validation untuk text preprocessing
- ✅ Safe pickle loading

---

## 10. TESTING CHECKLIST

- [x] App runs locally without errors
- [x] Model loads and predicts correctly
- [x] Preprocessing works on Indonesian text
- [x] CLI tool functional
- [x] Docker image builds successfully
- [x] GitHub repository created and pushed
- [x] Streamlit Cloud deployment successful
- [x] UI displays correctly
- [x] Sidebar metrics load properly
- [x] Predictions return valid results

---

## 11. CONTACT & SUPPORT

**Repository Owner:** qubil456  
**GitHub:** https://github.com/qubil456/deteksi-hoaks  
**Issues:** Report via GitHub Issues  

---

**Deployment Date:** 2026-06-12  
**Last Updated:** 2026-06-12  
**Status:** ✅ PRODUCTION READY

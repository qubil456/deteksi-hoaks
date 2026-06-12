# 05_Source_Code — Replikasi Deteksi Hoaks (Naive Bayes + TF-IDF)

Penyusun: **Abiansyah**

Replikasi paper Pratiwi, Asmara & Rahutomo (2017), "Study of hoax news detection using naive bayes classifier in Indonesian language" (ICTS 2017, DOI 10.1109/ICTS.2017.8265649), dengan dataset Mendeley CC BY 4.0 (DOI 10.17632/p3hfgr5j3m.1).

## Yang direplikasi
- **Metode usulan**: TF-IDF + Multinomial Naive Bayes, tuning alpha, diuji pada 3 skema split (60-40, 70-30, 80-20) seperti paper.
- **Baseline pembanding**: TF-IDF + Linear SVM, TF-IDF + Logistic Regression.
- **Metrik**: Accuracy, Precision, Recall, F1 + confusion matrix.

## Struktur
```
Script/
  config.py          # pusat seed, path, skema split, parameter
  preprocessing.py   # load Mendeley CSV -> bersihkan teks ID -> clean.csv
  train_eval.py      # latih usulan + baseline, evaluasi, simpan hasil
Notebook/
  (opsional, bisa dibuat memanggil script di atas)
```

## Library
```bash
pip install pandas numpy scikit-learn matplotlib
# opsional (stemming/stopword lebih baik): pip install Sastrawi
```

## Cara jalan (urut)
1. Unduh dataset sesuai `04_Dataset/Dataset_Source.txt`, taruh CSV di `Raw_Dataset/`.
2. `cd Script && python preprocessing.py`  → menghasilkan `clean.csv`.
3. `python train_eval.py`  → hasil di `07_Hasil_Eksperimen/`, confusion di `08_Visualisasi/`, model di `06_Model/`.

## Catatan kejujuran (penting untuk laporan)
1. **Hasil tidak akan identik dengan paper.** Paper 2017 tidak merinci semua parameter preprocessing & TF-IDF. Skrip ini memakai pilihan wajar (stopword ringkas, max_features=5000, unigram) + seed tetap. Angka Anda akan *mendekati*, bukan sama persis — wajar dalam replikasi, dan bisa jadi bahan diskusi.
2. **Stopword/stemming disederhanakan** (tanpa dependensi). Untuk lebih dekat ke standar NLP Indonesia, ganti dengan Sastrawi (stemming + stopword resmi). Ini bisa Anda sebut sebagai potensi pengembangan.
3. **Baseline (SVM, LogReg) adalah tambahan** untuk memenuhi syarat metode pembanding tugas — paper aslinya fokus Naive Bayes.
4. **Verifikasi status SINTA paper acuan** sebelum submit (ICTS 2017 = conference IEEE; bila dosen wajib *jurnal* SINTA, pasangkan dengan paper jurnal SINTA yang juga memakai dataset Mendeley ini).

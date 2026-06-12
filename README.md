# UAS Kecerdasan Buatan — Replikasi Deteksi Berita Hoaks Bahasa Indonesia

| | |
|---|---|
| **Nama** | Abiansyah |
| **NIM** | _(isi)_ |
| **Topik** | Deteksi berita hoaks bahasa Indonesia (NLP, ML klasik) |
| **Metode usulan** | TF-IDF + Multinomial Naive Bayes |
| **Baseline** | TF-IDF + Linear SVM, TF-IDF + Logistic Regression |
| **Dataset** | Indonesian Hoax News Detection (Mendeley, CC BY 4.0, DOI 10.17632/p3hfgr5j3m.1) |
| **Paper acuan** | Pratiwi, Asmara, Rahutomo (2017), ICTS, DOI 10.1109/ICTS.2017.8265649 |

## Research Gap (ringkas — kembangkan di 03_Gap_Analysis)
Paper acuan berfokus pada Naive Bayes tanpa pembanding model modern, tanpa tuning sistematis, dan dengan preprocessing terbatas. Replikasi ini menambah baseline pembanding dan tuning alpha.

## Novelty (ringkas)
Membandingkan metode usulan (NB) dengan baseline (SVM, Logistic Regression) pada skema split yang sama, untuk menguji apakah NB tetap kompetitif.

## Ringkasan Hasil
Dijalankan pada dataset asli (600 berita: 372 valid, 228 hoax).

Rata-rata antar 3 skema split (60-40, 70-30, 80-20):

| Model | Accuracy | Precision | Recall | F1 |
|---|---|---|---|---|
| SVM (baseline) | 0.743 | 0.669 | 0.639 | 0.654 |
| Naive Bayes (usulan) | 0.722 | 0.621 | 0.687 | 0.652 |
| Logistic Regression (baseline) | 0.728 | 0.765 | 0.411 | 0.533 |

Model NB terbaik: split 80-20, alpha=0.01 → accuracy 0.733, F1 0.667.
Detail lengkap: `07_Hasil_Eksperimen/hasil_replikasi.csv`.

## Struktur Folder
```
Abiansyah_UAS_AI/
  01_Paper/             paper acuan + referensi pendukung (≥10 PDF)
  02_Literature_Mapping/ literature mapping + comparison matrix
  03_Gap_Analysis/      gap, novelty, research method, framework
  04_Dataset/           Raw / Processed + Dataset_Source.txt
  05_Source_Code/       Script + Notebook + README
  06_Model/             model terlatih (best_model_nb.pkl)
  07_Hasil_Eksperimen/  hasil_replikasi.csv, perbandingan, best_alpha.json
  08_Visualisasi/       confusion matrix, grafik
  09_Draft_IEEE/        draft artikel IEEE (.docx/.pdf)
  10_Presentasi/        slide
  11_Turnitin/          laporan similarity
```

## Status pengerjaan
- [x] Struktur folder
- [x] Kode replikasi (teruji jalan di CPU)
- [x] Dataset source (link Mendeley publik)
- [ ] Unduh dataset & jalankan (hasil nyata)
- [ ] Isi 01–03 (paper, literature mapping, gap analysis)
- [ ] Draft IEEE, presentasi, Turnitin
- [ ] Verifikasi status SINTA paper acuan

## Catatan
Kode sudah diuji berjalan end-to-end dengan data sintetis (lalu dihapus). Hasil nyata muncul setelah dataset Mendeley diunduh dan dijalankan. Lihat `05_Source_Code/README.md` untuk catatan kejujuran soal keterbatasan replikasi.

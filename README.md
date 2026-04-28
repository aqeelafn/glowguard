# 🧪 GlowGuard: Advanced Skincare Chemical Interaction Analyzer

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red.svg)
![Data_Science](https://img.shields.io/badge/Expert_System-Data_Architecture-green.svg)

**Live Demo:** [KLIK DI SINI UNTUK MENCOBA APLIKASI] *(Isi dengan link Streamlit Share-mu nanti)*

## 📖 Ringkasan Eksekutif
Banyak konsumen mengalami iritasi kulit (*chemical burns*, kerusakan *skin barrier*) akibat ketidaktahuan dalam menggabungkan bahan aktif *skincare*. **GlowGuard** adalah sebuah purwarupa *Expert System* (Sistem Pakar) berbasis data yang menstrukturkan aturan dermatologis ke dalam bentuk *Feature Matrix* untuk menganalisis risiko interaksi kimia secara instan.

## 🧠 Metodologi Data & Pendekatan Machine Learning
Proyek ini mengadopsi kerangka kerja **Knowledge-Based Expert System**. Dataset dibangun dengan prinsip *Feature Engineering* yang mengekstraksi variabel independen pembentuk risiko iritasi.

Variabel (*Features*) yang dianalisis dalam sistem ini meliputi:
1. **Ordinal Features:** * `Strength` (Tingkat konsentrasi/kekuatan: *Low, Medium, Strong*)
   * `pH Levels` (Kadar asam basa: *Low, Neutral, Variable*)
2. **Categorical Features:** * `Kategori/Role` (Fungsi bahan: *Retinoid, Exfoliant, Barrier, Antioxidant*, dll)
   * `Interaction Type` (Bentuk reaksi: *Over Exfoliation, pH Conflict, Barrier Repair*, dll)
3. **Target Variable / Labels:**
   * `Label_Status` & `Irritation_Risk` (Di- *mapping* dari 0 [JANGAN] hingga 3 [WAJIB]).

**Mengapa ini penting dalam Data Science?**
Dataset multidimensi ini (memiliki fitur pendukung `ph`, `strength`, dll) bertindak sebagai *Ground Truth*. Strukturnya sudah disiapkan (*Pre-processed*) sehingga di masa depan dapat langsung digunakan untuk melatih model **Classification Machine Learning** (seperti *Decision Trees* atau *Random Forest Classifier*) untuk memprediksi probabilitas iritasi pada formulasi *skincare* yang belum pernah ada di pasaran.

## ⚙️ Arsitektur Sistem (Streamlit)
Aplikasi ini menjalankan *Rule-Engine Logic* dengan kompleksitas waktu `O(1)` berkat metode *Bi-directional Lookup*. Sistem tidak hanya memberikan hasil *binary* (Aman/Tidak), tetapi mengembalikan metrik analitik seperti jenis benturan (*pH Conflict / Deactivation*) berdasarkan *Feature Matrix* yang dibangun.

## 🛠️ Instalasi Lokal

1. Clone repository:
   ```bash
   git clone [https://github.com/username-kamu/glowguard-advanced.git](https://github.com/username-kamu/glowguard-advanced.git)
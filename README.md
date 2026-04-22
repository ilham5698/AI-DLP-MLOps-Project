# 🛡️ AI-Based Data Loss Prevention (DLP) with MLOps

Proyek ini adalah sistem deteksi kebocoran data otomatis yang mengimplementasikan siklus hidup **MLOps (Machine Learning Operations)**.

## 🚀 Fitur Utama
* **End-to-End Pipeline:** Otomasi dari ekstraksi teks (PDF/Docx) hingga deteksi.
* **TF-IDF & Cosine Similarity:** Algoritma NLP untuk mendeteksi kemiripan data sensitif.
* **Model Registry:** Penyimpanan versi model (.pkl) untuk reproduksibilitas.
* **Real-time Monitoring:** Dashboard untuk memantau tren ancaman dan log aktivitas.

## 📁 Hubungan dengan Materi Perkuliahan
1. **Introduction to MLOps:** Implementasi lifecycle Deployment & Monitoring.
2. **Anotasi Data:** Pembuatan dataset sintetis berlabel secara otomatis.
3. **ML Pipeline:** Integrasi preprocessing dan inference dalam satu alur kerja.
4. **Experiment Tracking:** Manajemen model menggunakan folder Registry.
5. **Dataset Tracking:** Pelacakan versi data melalui CSV logging.

## 🛠️ Cara Menjalankan
1. Install requirements: `pip install streamlit pandas scikit-learn pypdf python-docx plotly`
2. Generate Database: `python generate_data.py`
3. Jalankan Aplikasi: `streamlit run app.py`
graph LR
    A[generate_data.py] -- Membuat --> B[(dataset_rahasia.csv)]
    B -- Input Ke --> C[dlp_otak.py]
    D[registry/model.pkl] -- Diambil --> C
    C -- Proses AI --> E[app.py / Scanner]
    E -- Catat Hasil --> F[(monitoring_log.csv)]
    F -- Visualisasi --> G[Dashboard Monitoring]

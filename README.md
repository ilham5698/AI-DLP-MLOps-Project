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
graph TD
    A[generate_data.py] --> B[(dataset_rahasia.csv)]
    B --> C[dlp_otak.py]
    D[registry/model.pkl] --> C
    C --> E[app.py / Scanner]
    E --> F[(monitoring_log.csv)]
    F --> G[Dashboard Monitoring]

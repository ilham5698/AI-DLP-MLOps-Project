import re
import pandas as pd
import os
import streamlit as st
import joblib
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import docx

# ==========================================
# 1. MODEL REGISTRY (Materi Experiment Tracking)
# ==========================================
REGISTRY_PATH = "registry"

def registrasi_model(vectorizer, tfidf_matrix, versi="v1"):
    """Menyimpan model ke dalam Registry agar bisa diproduksi kembali (Reproducible)"""
    if not os.path.exists(REGISTRY_PATH):
        os.makedirs(REGISTRY_PATH)
    
    joblib.dump(vectorizer, f"{REGISTRY_PATH}/vectorizer_{versi}.pkl")
    joblib.dump(tfidf_matrix, f"{REGISTRY_PATH}/matrix_{versi}.pkl")
    return f"✅ Model Versi {versi} Berhasil Diregistrasi di Registry"

def muat_model_terbaik(versi="v1"):
    """Mengambil model dari registry untuk digunakan saat scanning"""
    try:
        vectorizer = joblib.load(f"{REGISTRY_PATH}/vectorizer_{versi}.pkl")
        tfidf_matrix = joblib.load(f"{REGISTRY_PATH}/matrix_{versi}.pkl")
        return vectorizer, tfidf_matrix
    except:
        return None, None

# ==========================================
# 2. MONITORING LOG (Materi MLOps Monitoring)
# ==========================================
def log_monitoring(kategori, skor, status_bocor):
    """Mencatat aktivitas deteksi untuk memantau performa model (Monitoring)"""
    log_file = "monitoring_log.csv"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    new_data = {
        "Timestamp": [timestamp],
        "Kategori": [kategori],
        "Skor": [skor],
        "Status": [status_bocor]
    }
    df_new = pd.DataFrame(new_data)
    
    if not os.path.isfile(log_file):
        df_new.to_csv(log_file, index=False)
    else:
        df_new.to_csv(log_file, mode='a', header=False, index=False)

# ==========================================
# 3. DATA INGESTION (Materi Pipeline)
# ==========================================
@st.cache_data
def muat_database():
    """Memuat dataset rahasia (Dataset Tracking)"""
    file_path = "dataset_rahasia.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.to_dict('records'), f"Database Aktif: {len(df)} Records"
    return [], "⚠️ Database Tidak Ditemukan"

def baca_file(uploaded_file):
    """Mengekstrak teks dari berbagai format file (Preprocessing)"""
    teks = ""
    try:
        if uploaded_file.name.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            for page in reader.pages: teks += page.extract_text()
        elif uploaded_file.name.endswith('.docx'):
            doc = docx.Document(uploaded_file)
            for p in doc.paragraphs: teks += p.text + "\n"
        elif uploaded_file.name.endswith('.txt'):
            teks = uploaded_file.read().decode("utf-8")
    except Exception as e:
        return f"Error: {e}"
    return teks

# ==========================================
# 4. PATTERN MATCHING (Regex)
# ==========================================
def cek_pola_sensitif(teks):
    """Mendeteksi pola data pribadi seperti NIK dan Nomor Telepon"""
    laporan = []
    if re.search(r'\b\d{16}\b', teks):
        laporan.append("NIK/KTP (16 Digit)")
    if re.search(r'(\+62|62|0)8[1-9][0-9]{6,11}', teks):
        laporan.append("Nomor Telepon Indonesia")
    return laporan

# ==========================================
# 5. INFERENCE ENGINE (Materi Modeling)
# ==========================================
def cek_kebocoran(teks_input):
    """Pipeline utama untuk mendeteksi kemiripan data"""
    DATABASE, status_db = muat_database()
    if not DATABASE:
        return 0, "N/A", [], status_db

    list_rahasia = [str(item['Isi']).lower() for item in DATABASE]
    teks_input_clean = teks_input.lower()

    # Coba muat dari Registry dulu
    vectorizer, tfidf_matrix = muat_model_terbaik()

    # Jika registry kosong, buat pipeline baru (Fit Model)
    if vectorizer is None:
        vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
        tfidf_matrix = vectorizer.fit_transform(list_rahasia)
        # Langsung simpan ke registry setelah training pertama
        registrasi_model(vectorizer, tfidf_matrix)

    # Transformasi input user ke angka (Vektor)
    tfidf_input = vectorizer.transform([teks_input_clean])
    
    # Hitung kemiripan (Cosine Similarity)
    cosine_sim = cosine_similarity(tfidf_input, tfidf_matrix)
    
    skor_maks = cosine_sim.max()
    indeks_terdekat = cosine_sim.argmax()
    kategori_terdeteksi = DATABASE[indeks_terdekat]['Kategori']
    
    # Cek Pola Regex
    pola_ditemukan = cek_pola_sensitif(teks_input)
    
    # Simpan ke Monitoring Log
    status_hasil = "TERDETEKSI" if (skor_maks > 0.4 or pola_ditemukan) else "AMAN"
    log_monitoring(kategori_terdeteksi if status_hasil == "TERDETEKSI" else "Aman", skor_maks, status_hasil)

    return skor_maks, kategori_terdeteksi, pola_ditemukan, status_db
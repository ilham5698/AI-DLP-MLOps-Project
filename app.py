import streamlit as st
import pandas as pd
import os
import time
import plotly.express as px # Opsional: untuk grafik yang lebih bagus
from dlp_otak import muat_database, baca_file, cek_kebocoran

# ==========================================
# 1. KONFIGURASI TEMA (Cyber Security UI)
# ==========================================
st.set_page_config(page_title="Cyber DLP SOC Dashboard", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #050a0f; color: #00ff41; font-family: 'Courier New'; }
    .stTextArea textarea { background-color: #000 !important; color: #00ff41 !important; border: 1px solid #00ff41 !important; }
    h1, h2, h3 { color: #00ff41 !important; text-shadow: 0 0 10px #00ff41; }
    .stButton>button { background-color: #00ff41; color: black; font-weight: bold; border-radius: 0px; width: 100%; border: none; }
    .stButton>button:hover { background-color: #008f11; color: white; }
    .stTabs [data-baseweb="tab-list"] { background-color: #050a0f; }
    .stTabs [data-baseweb="tab"] { color: #00ff41; font-weight: bold; }
    .stMetric { background-color: #0c1621; padding: 10px; border-radius: 5px; border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. HEADER APLIKASI
# ==========================================
st.title("🛡️ SECURITY OPERATIONS CENTER (SOC)")
st.write("AI-Powered Data Loss Prevention System | MLOps Version")

# Tabs untuk memisahkan fitur Scanner dan Monitoring
tab_scanner, tab_monitoring = st.tabs(["🔍 NETWORK SCANNER", "📊 MONITORING DASHBOARD"])

# ==========================================
# 3. HALAMAN SCANNER (Inference / Deployment)
# ==========================================
with tab_scanner:
    st.subheader("System Input")
    
    col_in1, col_in2 = st.columns([2, 1])
    with col_in1:
        input_teks = st.text_area("RAW PACKET DATA (INPUT TEKS):", height=200, placeholder="Masukkan teks atau log yang ingin diperiksa...")
    with col_in2:
        file_upload = st.file_uploader("UPLOAD DOCUMENT (PDF/DOCX/TXT):", type=["pdf", "docx", "txt"])

    if st.button("EXECUTE SECURITY SCAN"):
        # Data Ingestion
        konten = baca_file(file_upload) if file_upload else input_teks
        
        if konten:
            # Simulasi Pipeline Processing
            with st.status("Neural Scan in Progress...", expanded=True) as status:
                st.write("Preprocessing data...")
                time.sleep(0.5)
                st.write("Comparing with Model Registry (v1)...")
                
                # ML Inference (Memanggil otak AI)
                skor, kategori, pola, msg_db = cek_kebocoran(konten)
                
                time.sleep(0.5)
                status.update(label="SCAN COMPLETE!", state="complete", expanded=False)
            
            st.divider()

            # Logic Deteksi (Threshold 0.4 sesuai Experiment Tracking)
            if skor > 0.4 or pola:
                st.error("🚨 SECURITY BREACH DETECTED!")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("THREAT LEVEL", f"{skor:.2%}", delta="HIGH RISK", delta_color="inverse")
                with c2:
                    st.metric("IDENTIFIED CATEGORY", kategori)
                with c3:
                    st.metric("PATTERNS FOUND", len(pola))
                
                if pola:
                    st.warning(f"**Pola Sensitif Terdeteksi:** {', '.join(pola)}")
                
                st.info("Saran Tindakan: Segera hapus atau enkripsi data sebelum dikirim.")
            else:
                st.success("✅ NETWORK SECURE: NO SENSITIVE DATA DETECTED")
                st.metric("THREAT LEVEL", f"{skor:.2%}", delta="SAFE")
        else:
            st.warning("SYSTEM ERROR: Silakan masukkan data untuk dipindai.")

# ==========================================
# 4. HALAMAN MONITORING (MLOps Monitoring Stage)
# ==========================================
with tab_monitoring:
    st.subheader("Real-Time Security Analytics")
    
    log_file = "monitoring_log.csv"
    if os.path.exists(log_file):
        df_log = pd.read_csv(log_file)
        
        # Ringkasan Metrik
        total_scan = len(df_log)
        total_breach = len(df_log[df_log['Status'] == "TERDETEKSI"])
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Scans", total_scan)
        m2.metric("Breaches Detected", total_breach, delta=f"Risk: {(total_breach/total_scan):.1%}", delta_color="inverse")
        m3.metric("System Uptime", "99.9%", delta="Stable")

        st.divider()

        # Visualisasi (Materi Monitoring: Melihat tren ancaman)
        col_graph1, col_graph2 = st.columns(2)
        
        with col_graph1:
            st.write("📈 Tren Skor Ancaman (Threat Score Trend)")
            st.line_chart(df_log['Skor'])
        
        with col_graph2:
            st.write("📊 Distribusi Kategori Kebocoran")
            # Menghitung jumlah per kategori
            kat_counts = df_log[df_log['Kategori'] != "Aman"]['Kategori'].value_counts()
            if not kat_counts.empty:
                st.bar_chart(kat_counts)
            else:
                st.info("Belum ada kategori ancaman yang tercatat.")

        st.divider()
        
        # Histori Log Mentah (Materi Dataset Tracking)
        st.write("🗄️ Raw Security Logs (Dataset Tracking)")
        st.dataframe(df_log.sort_values(by="Timestamp", ascending=False), use_container_width=True)
        
        if st.button("Clear Monitoring Logs"):
            os.remove(log_file)
            st.rerun()
            
    else:
        st.info("Waiting for data... Jalankan scanner terlebih dahulu untuk melihat statistik monitoring.")
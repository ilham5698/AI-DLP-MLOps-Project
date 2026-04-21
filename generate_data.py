import pandas as pd
import random
import string

# Daftar kategori dan data sampel untuk simulasi rahasia
categories = ["IT Security", "Keuangan", "HRD", "Strategi"]
nama_sampel = ["Budi Santoso", "Siti Aminah", "Ahmad Hidayat", "Dewi Lestari", "Rizky Pratama"]
bank_sampel = ["Bank BCA", "Bank Mandiri", "Bank BNI", "Bank BRI"]

print("Memulai pembuatan 5000 data rahasia...")

data_rows = []
for i in range(5000):
    kategori = random.choice(categories)
    
    if kategori == "IT Security":
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        api = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        isi = f"Peringatan: Akses server via IP {ip} dengan API Key {api} terdeteksi."
              
    elif kategori == "Keuangan":
        rek = ''.join(random.choices(string.digits, k=10))
        nominal = random.randint(1, 100) * 1000000
        isi = f"Transfer Rp {nominal:,} ke {random.choice(bank_sampel)} rek {rek} a/n {random.choice(nama_sampel)}."
              
    elif kategori == "HRD":
        nik = ''.join(random.choices(string.digits, k=16))
        isi = f"Data Karyawan: {random.choice(nama_sampel)} (NIK: {nik}) Gaji Rp {random.randint(5, 50)}jt."
              
    else:
        isi = f"Proyek Strategis 2026: Rencana akuisisi {random.choice(['Garuda', 'Nusantara'])}."

    data_rows.append([kategori, isi])

df = pd.DataFrame(data_rows, columns=["Kategori", "Isi"])
df.to_csv("dataset_rahasia.csv", index=False, encoding='utf-8')
print("✅ Selesai! File 'dataset_rahasia.csv' siap digunakan.")
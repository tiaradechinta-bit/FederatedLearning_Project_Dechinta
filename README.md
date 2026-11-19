# 🧠 Federated Learning — Simulation & Dashboard

Proyek simulasi **Federated Learning** menggunakan Python dan Flower Framework dengan visualisasi hasil eksperimen melalui dashboard interaktif berbasis Streamlit.

Proyek ini mensimulasikan proses pelatihan model Machine Learning secara terdistribusi menggunakan **1 server dan 3 client**, dengan metode agregasi **Federated Averaging (FedAvg)**.

## 🎯 Tujuan Proyek

Proyek ini bertujuan untuk memahami proses Federated Learning, yaitu metode pelatihan Machine Learning yang memungkinkan beberapa client melatih model menggunakan data lokal masing-masing tanpa harus mengumpulkan seluruh data mentah ke server pusat.

Konsep utama:
- Data pelatihan tetap berada pada masing-masing client.
- Setiap client melakukan pelatihan model secara lokal.
- Client mengirimkan pembaruan parameter model kepada server.
- Server menggabungkan pembaruan model menggunakan algoritma FedAvg.
- Proses pelatihan dilakukan dalam beberapa ronde.

## 🏗️ Arsitektur Sistem

Sistem menggunakan arsitektur:
- **1 Flower Server:** mengoordinasikan proses pelatihan dan agregasi model.
- **3 Flower Client:** melakukan pelatihan menggunakan data lokal masing-masing.
- **Global Test Dataset:** digunakan untuk mengevaluasi performa model.
- **Streamlit Dashboard:** menampilkan hasil eksperimen dalam bentuk metrik, grafik, tabel, dan visualisasi jaringan.

## 📁 Struktur Proyek

```text
FederatedLearning_Project_Dechinta/
│
├── dashboard.py
├── dashboard_backup.py
├── test_html.py
├── results.json
├── requirements.txt
├── README.md
│
├── src/
│   ├── server/
│   ├── client/
│   └── utils/
│
├── data/
├── assets/
├── logs/
└── .gitignore
```

Folder `venv/` merupakan lingkungan Python lokal dan tidak perlu diunggah ke GitHub.

## 🚀 Teknologi yang Digunakan

| Teknologi | Versi | Fungsi |
|---|---|---|
| Python | 3.10.8 | Bahasa pemrograman |
| Flower | 1.24.0 | Framework Federated Learning |
| Streamlit | 1.40.1 | Dashboard web |
| Plotly | 5.18.0 | Visualisasi grafik |
| NumPy | Minimal 1.26.0 | Komputasi numerik |
| Scikit-learn | 1.3.2 | Machine Learning |
| Pandas | 2.0.3 | Pengolahan data |

## ⚙️ Cara Menjalankan Dashboard

### 1. Persiapkan proyek

Pastikan Python sudah terpasang dan buka terminal pada direktori proyek.

### 2. Aktifkan virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Jalankan dashboard

```powershell
python -m streamlit run dashboard.py
```

Dashboard dapat diakses melalui alamat lokal yang ditampilkan pada terminal, biasanya:

```text
http://localhost:8501
```

Jika port tersebut sedang digunakan, Streamlit dapat menggunakan port lain, misalnya 8502.

## 📊 Hasil Eksperimen

Simulasi Federated Learning telah berhasil dijalankan dengan konfigurasi berikut:

| Parameter | Hasil |
|---|---:|
| Status eksperimen | Completed |
| Jumlah server | 1 |
| Jumlah client | 3 |
| Jumlah ronde | 5 |
| Sampel per client | 40 |
| Akurasi akhir | 91,67% |
| Loss ronde terakhir | 0,32298 |

Hasil eksperimen disimpan dalam file `results.json` dan digunakan oleh dashboard untuk menampilkan informasi performa model.

## 🎮 Fitur Dashboard

Dashboard menyediakan beberapa fitur visualisasi:
1. Ringkasan hasil eksperimen.
2. Informasi jumlah ronde dan client.
3. Visualisasi arsitektur jaringan Federated Learning.
4. Penjelasan proses pelatihan terdistribusi.
5. Grafik perkembangan akurasi dan loss.
6. Tabel hasil setiap ronde.
7. Ringkasan hasil eksperimen.

**Catatan:** Dashboard membaca hasil eksperimen yang telah disimpan pada `results.json`. Visualisasi jaringan merupakan ilustrasi arsitektur sistem, bukan pemantauan komunikasi jaringan secara langsung.

## ☁️ Deployment

Dashboard dapat dipublikasikan menggunakan **Streamlit Community Cloud** dengan menghubungkan repository GitHub.

File utama aplikasi:

```text
dashboard.py
```

File hasil eksperimen:

```text
results.json
```

File dependensi:

```text
requirements.txt
```

## 👩‍💻 Pengembang

**Dechinta Mutiara Hazrina**

**NIM:** 24221022

**Proyek:** Federated Learning Simulation & Dashboard
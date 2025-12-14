# EDA_Kerawanan_Pangan_Indonesia
Aplikasi ini merupakan dashboard berbasis Streamlit yang dirancang untuk menganalisis kondisi kerawanan pangan di Indonesia selama periode 2020–2024. Dashboard ini mengintegrasikan berbagai aspek penting seperti produksi pertanian, kondisi sosial ekonomi, faktor lingkungan dan geospasial, gizi dan kesehatan keluarga, serta rantai pasok pangan.

# 📊 Dashboard Analisis Produksi dan Kerawanan Pangan di Indonesia (2020–2024)

Dashboard interaktif berbasis **Streamlit** untuk menganalisis kondisi **ketahanan dan kerawanan pangan di Indonesia** dari berbagai sudut pandang, meliputi:
- Produksi pangan utama (padi & jagung)
- Faktor sosial ekonomi rumah tangga
- Faktor lingkungan & geospasial
- Faktor gizi dan kesehatan keluarga
- Produksi, impor, dan supply chain pangan

Dashboard ini dirancang sebagai **alat eksplorasi data dan visualisasi** untuk mendukung analisis kebijakan dan pengambilan keputusan berbasis data.

---

## 🎯 Tujuan Proyek
1. Mengidentifikasi **pola produksi pangan nasional dan regional**
2. Menganalisis **hubungan produksi pangan dengan ketahanan pangan (IKP)**
3. Mengkaji pengaruh **faktor sosial, lingkungan, dan gizi** terhadap kerawanan pangan
4. Menyajikan analisis dalam bentuk **dashboard interaktif yang mudah dipahami**

---

## 🧩 Fitur Utama Dashboard

### 📘 Slide 1 — Produksi & Kerawanan Pangan Nasional
- KPI produksi padi & jagung nasional
- Tren produksi 5 tahun (2020–2024)
- Top 10 provinsi produksi terendah
- Peta choropleth produksi pangan Indonesia
- Bubble chart produksi vs estimasi IKP
- Tabel data mentah

---

### 📘 Slide 2 — Faktor Sosial Ekonomi Rumah Tangga
- KPI sosial ekonomi (IKP, kemiskinan, RLS, KPM, dll.)
- Pie chart:
  - Jenis pekerjaan
  - Jumlah anggota keluarga
  - Pengeluaran pangan vs nonpangan
- Scatterplot pengaruh faktor sosial terhadap IKP

---

### 📘 Slide 3 — Faktor Lingkungan & Geospasial
- Analisis bencana (banjir & kekeringan)
- Infrastruktur pasar dan distribusi
- Hubungan IKP dengan:
  - Intensitas bencana
  - Akses pasar & toko
- Visualisasi boxplot dan scatter interaktif
- Insight dan rekomendasi kebijakan

---

### 📘 Slide 4 — Gizi & Kesehatan Keluarga
- Hubungan IKP dengan prevalensi stunting
- Tren IKP vs stunting (dengan regresi)
- Top 10 provinsi stunting tertinggi
- Heatmap konsumsi energi, protein, dan kalori
- Top 10 provinsi dengan konsumsi protein terendah

---

### 📘 Slide 5 — Produksi & Supply Chain
- Produksi pangan vs IKP (log-scale)
- Produktivitas & luas panen per kategori kerawanan
- Hubungan impor non-migas dengan IKP
- Top 10 provinsi produksi & impor tertinggi

---

## 🛠️ Teknologi yang Digunakan
- **Python 3.12**
- **Streamlit** — dashboard interaktif
- **Pandas & NumPy** — data processing
- **Matplotlib & Seaborn** — visualisasi statis
- **Plotly** — visualisasi interaktif
- **Scikit-learn** — normalisasi data (MinMaxScaler)

---

## 📦 Menjalankan Aplikasi
- streamlit run app_eda.py

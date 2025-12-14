import plotly.express as px
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import json
from sklearn.preprocessing import MinMaxScaler

# ================================================================
# CONFIG
# ================================================================
st.set_page_config(
    page_title="Dashboard Produksi Pangan",
    layout="wide"
)

# ================================================================
# LOAD DATA
# ================================================================
@st.cache_data
def load_data():

    padi = pd.read_csv(r"Dataset/Produksi_Padi_2020_2024_Clean.csv")
    jagung = pd.read_csv(r"Dataset/Produksi_Jagung_2020_2024_Clean.csv")

    # samakan nama kolom
    padi = padi.rename(columns={"Provinsi": "provinsi"})
    jagung = jagung.rename(columns={"Provinsi": "provinsi"})

    tahun = ["2020", "2021", "2022", "2023", "2024"]

    # ================= PRODUKSI PADI =================
    padi_melt = padi.melt(
        id_vars="provinsi",
        value_vars=tahun,
        var_name="tahun",
        value_name="produksi_padi"
    )
    padi_melt["tahun"] = padi_melt["tahun"].astype(int)

    # ================= PRODUKSI JAGUNG =================
    jagung_melt = jagung.melt(
        id_vars="provinsi",
        value_vars=tahun,
        var_name="tahun",
        value_name="produksi_jagung"
    )
    jagung_melt["tahun"] = jagung_melt["tahun"].astype(int)

    # ================= GABUNG =================
    df = pd.merge(padi_melt, jagung_melt, on=["provinsi", "tahun"], how="outer")

    return df


df = load_data()

# ================================================================
# SIDEBAR SLIDE NAVIGATION
# ================================================================
st.sidebar.title("📚 Navigasi Dashboard")

if "slide" not in st.session_state:
    st.session_state.slide = 1

slides = {
    1: "📘 Dashboard Produksi dan Kerawananan Pangan di Indonesia",
    2: "📘 Analisis Kerawanan Pangan Berdasarkan Sosial Ekonomi Rumah Tangga",
    3: "📘 Analisis Kerawanan Pangan Berdasarkan Faktor Lingkungan dan Geospasial",
    4: "📘 Analisis Kerawanan Pangan Berdasarkan Karakteristik Gizi dan Kesehatan Keluarga",
    5: "📘 Analisis Kerawanan Pangan Berdasarkan Produksi dan Supply Chain",
}

for key, label in slides.items():
    if st.sidebar.button(label):
        st.session_state.slide = key

slide = st.session_state.slide

# ================================================================
# SLIDE 1 — FULL DASHBOARD 
# ================================================================
if slide == 1:

    st.title("Dashboard Analisis Produksi dan Kerawanan Pangan di Indonesia Tahun 2020–2024")
    # ================= KPI OVERVIEW =================
    st.subheader("Overview KPI Produksi Pangan Nasional (2020–2024)")

    total_padi = df["produksi_padi"].sum()
    total_jagung = df["produksi_jagung"].sum()
    avg_padi_prov = df.groupby("provinsi")["produksi_padi"].mean().mean()
    avg_jagung_prov = df.groupby("provinsi")["produksi_jagung"].mean().mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total Produksi Padi", f"{total_padi:,.0f} ton")
    col2.metric("Total Produksi Jagung", f"{total_jagung:,.0f} ton")
    col3.metric("Rata-rata Produksi Padi per Provinsi", f"{avg_padi_prov:,.0f} ton")
    col4.metric("Rata-rata Produksi Jagung per Provinsi", f"{avg_jagung_prov:,.0f} ton")
    col5.metric("Jumlah Provinsi Terdata", f"{df['provinsi'].nunique()}")
    st.markdown("---")

    # ------------------------------------------------------------
    # TREN 5 TAHUN NASIONAL
    # ------------------------------------------------------------
    st.header("Tren Produksi Nasional (5 Tahun Terakhir)")

    nat_padi = df.groupby("tahun")["produksi_padi"].sum()
    nat_jagung = df.groupby("tahun")["produksi_jagung"].sum()

    tahun_list = sorted(df["tahun"].unique())

    colA, colB = st.columns(2)

    with colA:
        st.subheader("🌾 Produksi Padi Nasional")
        figA, axA = plt.subplots()
        axA.plot(tahun_list, nat_padi.values, marker="o", color="#F39C12")
        axA.set_xlabel("Tahun")
        axA.set_ylabel("Produksi (ton)")
        axA.set_xticks(tahun_list)
        axA.set_xticklabels(tahun_list)
        st.pyplot(figA)

    with colB:
        st.subheader("🌽 Produksi Jagung Nasional")
        figB, axB = plt.subplots()
        axB.plot(tahun_list, nat_jagung.values, marker="o", color="#F39C12")
        axB.set_xlabel("Tahun")
        axB.set_ylabel("Produksi (ton)")
        axB.set_xticks(tahun_list)
        axB.set_xticklabels(tahun_list)
        st.pyplot(figB)

    st.markdown("---")

    # ------------------------------------------------------------
    # FILTER TAHUN
    # ------------------------------------------------------------
    st.header("Analisis Provinsi Rawan Produksi Padi & Jagung per Tahun (Terendah)")

    tahun_pilih = st.selectbox("Pilih Tahun:", sorted(df["tahun"].unique()))

    df_th = df[df["tahun"] == tahun_pilih]

    col1, col2 = st.columns(2)

    # ================= TOP 10 PRODUKSI RENDAH PADI =================
    with col1:
        st.subheader(f"🌾 Top 10 Produksi Padi Terendah — {tahun_pilih}")
        df_low_padi = df_th.sort_values("produksi_padi", ascending=True).head(10)

        fig1, ax1 = plt.subplots()
        ax1.bar(df_low_padi["provinsi"], df_low_padi["produksi_padi"], color="#F39C12")
        ax1.tick_params(axis="x", rotation=45)
        st.pyplot(fig1)

    # ================= TOP 10 PRODUKSI RENDAH JAGUNG =================
    with col2:
        st.subheader(f"🌽 Top 10 Produksi Jagung Terendah — {tahun_pilih}")
        df_low_jagung = df_th.sort_values("produksi_jagung", ascending=True).head(10)

        fig2, ax2 = plt.subplots()
        ax2.bar(df_low_jagung["provinsi"], df_low_jagung["produksi_jagung"], color="#F39C12")
        ax2.tick_params(axis="x", rotation=45)
        st.pyplot(fig2)

    st.markdown("---")

    # ------------------------------------------------------------
    # PRODUKSI PER PROVINSI × TAHUN
    # ------------------------------------------------------------
    st.header("Peta Produksi Pangan Indonesia")

    tahun_pilih = st.selectbox(
        "Pilih Tahun",
        sorted(df["tahun"].unique())
    )

    komoditas = st.radio(
        "Pilih Komoditas",
        ["produksi_padi", "produksi_jagung"],
        horizontal=True
    )

    df_map = df[df["tahun"] == tahun_pilih].copy()
    df_map["provinsi"] = df_map["provinsi"].str.upper().str.strip()

    with open("indonesia-province.json", "r", encoding="utf-8") as f:
        indo_geojson = json.load(f)

    fig = px.choropleth(
        df_map,
        geojson=indo_geojson,
        locations="provinsi",
        featureidkey="properties.Propinsi",
        color=komoditas,
        color_continuous_scale="YlOrBr",
        hover_name="provinsi",
        hover_data={komoditas: ":,.0f"},
        title=f"Peta Produksi {komoditas.replace('_',' ').title()} Indonesia Tahun {tahun_pilih}"
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
        lataxis_range=[-12, 7],
        lonaxis_range=[94, 142],
        projection_scale=1.25
    )

    fig.update_layout(
        height=800,
        dragmode=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "scrollZoom": False,
            "doubleClick": False,
            "displayModeBar": False
        }
    )



    # ------------------------------------------------------------
    # BUBBLE CHART PRODUKSI vs ESTIMASI IKP
    # ------------------------------------------------------------
    st.header("Bubble Chart: Produksi vs Estimasi IKP per Provinsi")
    # Buat IKP estimasi sederhana = total produksi / max produksi × 100
    df_bubble = df.groupby("provinsi")[["produksi_padi", "produksi_jagung"]].sum().reset_index()
    df_bubble["IKP_estimasi"] = (df_bubble["produksi_padi"] + df_bubble["produksi_jagung"]) / \
                                (df_bubble["produksi_padi"].sum() + df_bubble["produksi_jagung"].sum()) * 100

    fig5 = px.scatter(df_bubble, x="produksi_padi", y="produksi_jagung",
                      size="IKP_estimasi", color="provinsi",
                      hover_data=["IKP_estimasi"], 
                      title="Produksi Padi vs Jagung (Ukuran Bubble = IKP Estimasi)",
                      size_max=60)
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")

    # ------------------------------------------------------------
    # SHOW RAW DATA
    # ------------------------------------------------------------
    st.subheader("📄 Lihat Data Asli")

    # --- Perbaikan format tahun ---
    df_display = df.copy()
    df_display["tahun"] = df_display["tahun"].astype(str)
    df_display["produksi_padi"] = df_display["produksi_padi"].astype(int).astype(str)
    df_display["produksi_jagung"] = df_display["produksi_jagung"].astype(int).astype(str)

    st.dataframe(df_display)

# ================================================================
# SLIDE 2 — ANALISIS SOSIAL EKONOMI / SOSIAL BUDAYA
# ================================================================
elif slide == 2:
    st.title("Dashboard Analisis Kerawanan Pangan Berdasarkan Sosial Ekonomi Rumah Tangga")
    st.markdown("---")

    # ---------------------------------
    # LOAD DATASET LOKAL
    # ---------------------------------
    df_sosial = pd.read_csv(r"Dataset/Sosial Budaya - Dataset Utama.csv")

    # ---------------------------------
    # CLEANING
    # ---------------------------------
    def format_dataset(df):
        percent_cols = ["IKP", "P0", "RLS", "RTL", "1", "2-3", "4-5", "≥6"]

        for col in percent_cols:
            if col in df.columns:
                df[col] = (
                    df[col].astype(str)
                    .str.replace(",", ".", regex=False)
                    .astype(float)
                )

        int_cols = [
            "KPM", "Wirausaha", "Usaha Kecil", "Usaha Besar",
            "Karyawan/Formal", "Lepas Pertanian", "Lepas Non-Pertanian",
            "Pekerja Keluarga",
            "Pengeluaran Pangan", "Pengeluaran Nonpangan"
        ]

        for col in int_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        return df

    df_sosial = format_dataset(df_sosial)

    # ---------------------------------
    # FILTER
    # ---------------------------------
    st.subheader("Filter Data")

    prov_list = ["Indonesia"] + sorted(df_sosial["PROVINSI"].unique())
    year_list = sorted(df_sosial["TAHUN"].unique(), reverse=True)

    selected_prov = st.selectbox("Pilih PROVINSI", prov_list, index=prov_list.index("Indonesia"))
    selected_year = st.selectbox("Pilih TAHUN", year_list, index=year_list.index(2024))

    # Apply filter
    filtered_df = df_sosial[df_sosial["TAHUN"] == selected_year]

    if selected_prov != "Indonesia":
        filtered_df = filtered_df[filtered_df["PROVINSI"] == selected_prov]

    # ---------------------------------
    # KPI SECTION
    # ---------------------------------
    st.subheader("Overview (KPI)")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Indeks Ketahanan Pangan", f"{filtered_df['IKP'].mean():.2f}")
    col2.metric("Rata-rata Kemiskinan", f"{filtered_df['P0'].mean():.2f}%")
    col3.metric("Total Keluarga Penerima Manfaat", f"{filtered_df['KPM'].sum():,.0f}")
    col4.metric("Rata-rata Lama Sekolah", f"{filtered_df['RLS'].mean():.2f}")
    col5.metric("Persentase Rumah Tangga Lansia", f"{filtered_df['RTL'].mean():.2f}%")

    # ---------------------------------
    # PIE CHART – JENIS PEKERJAAN
    # ---------------------------------
    st.subheader("Pie Chart: Jenis Pekerjaan")

    job_cols = [
        "Wirausaha", "Usaha Kecil", "Usaha Besar",
        "Karyawan/Formal", "Lepas Pertanian",
        "Lepas Non-Pertanian", "Pekerja Keluarga"
    ]

    job_data = filtered_df[job_cols].sum()

    fig_job = px.pie(
        names=job_data.index,
        values=job_data.values,
        title="Distribusi Jenis Pekerjaan"
    )
    st.plotly_chart(fig_job, use_container_width=True)

    # ---------------------------------
    # PIE CHART – JUMLAH ANGGOTA KELUARGA
    # ---------------------------------
    st.subheader("Pie Chart: Jumlah Anggota Keluarga")

    fam_cols = ["1", "2-3", "4-5", "≥6"]
    fam_data = filtered_df[fam_cols].mean()

    fig_fam = px.pie(
        names=fam_data.index,
        values=fam_data.values,
        title="Distribusi Jumlah Anggota Keluarga"
    )
    st.plotly_chart(fig_fam, use_container_width=True)

    # ---------------------------------
    # PIE CHART – PENGELUARAN PANGAN vs NONPANGAN
    # ---------------------------------
    st.subheader("Pie Chart: Pengeluaran Pangan vs Nonpangan")

    exp_cols = ["Pengeluaran Pangan", "Pengeluaran Nonpangan"]
    exp_data = filtered_df[exp_cols].sum()

    fig_exp = px.pie(
        names=exp_data.index,
        values=exp_data.values,
        title="Perbandingan Pengeluaran Pangan vs Nonpangan"
    )
    st.plotly_chart(fig_exp, use_container_width=True)

    # ---------------------------------
    # SCATTERPLOT PENGARUH FAKTOR TERHADAP IKP
    # ---------------------------------
    st.subheader("Scatterplot Pengaruh Faktor Sosial Budaya terhadap Ketahanan Pangan (IKP)")

    rename_cols = {
        "P0": "Persentase Kemiskinan",
        "RTL": "Persentase Rumah Tangga Lansia",
        "KPM": "Jumlah Keluarga Penerima Manfaat",
        "RLS": "Rata-rata Lama Sekolah",
        "1": "Jumlah Anggota Keluarga 1",
        "2-3": "Jumlah Anggota Keluarga 2-3",
        "4-5": "Jumlah Anggota Keluarga 4-5",
        "≥6": "Jumlah Anggota Keluarga ≥6"
    }

    df_renamed = filtered_df.rename(columns=rename_cols)

    exclude_cols = ["TAHUN", "PROVINSI", "IKP", "Kerentanan Area"]

    factor_candidates = [
        col for col in df_renamed.columns
        if col not in exclude_cols
    ]

    selected_factor = st.selectbox("Pilih Faktor", factor_candidates)

    fig_scatter = px.scatter(
        df_renamed,
        x=selected_factor,
        y="IKP",
        trendline="ols",
        title=f"Pengaruh {selected_factor} terhadap IKP"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

# ================================================================
# SLIDE 3 — ANALISIS KERAWANAN PANGAN BERDASARKAN FAKTOR LINGKUNGAN & GEOSPASIAL
# ================================================================
elif slide == 3:
    st.title("Analisis Kerawanan Pangan Berdasarkan Faktor Lingkungan dan Geospasial")
    st.markdown("---")

    @st.cache_data
    def load_geospatial_data():
        # GANTI PATH SESUAI KOMPUTER KAMU
        df_pasar = pd.read_csv(r"Dataset/Pasar_34_provinsi.csv")
        df_disaster = pd.read_csv(r"Dataset/merged_disaster_flood_drought.csv")
        df_ikp = pd.read_csv(r"Dataset/Indeks Ketahanan Pangan.csv")

        # === NORMALISASI NAMA PROVINSI ===
        df_pasar['Provinsi'] = df_pasar['Provinsi'].str.upper().str.strip()
        df_disaster['Province'] = df_disaster['Province'].str.upper().str.strip()
        df_ikp['PROVINSI'] = df_ikp['PROVINSI'].str.upper().str.strip()

        # Standarisasi nama yang sering beda
        replace_map = {
            'KEP. BANGKA BELITUNG': 'KEPULAUAN BANGKA BELITUNG',
            'KEP. RIAU': 'KEPULAUAN RIAU',
            'DI YOGYAKARTA': 'D.I. YOGYAKARTA',
            'DKI JAKARTA': 'DKI JAKARTA',
            'INDONESIA': None
        }
        df_pasar['Provinsi'] = df_pasar['Provinsi'].replace(replace_map)

        # === RENAME KOLOM KE "Province" SECARA BENAR ===
        df_pasar = df_pasar.rename(columns={'Provinsi': 'Province'})
        df_ikp = df_ikp.rename(columns={'PROVINSI': 'Province'})  # ini yang tadi salah!

        # Filter baris "INDONESIA" dan data rusak
        df_pasar = df_pasar[df_pasar['Province'] != 'INDONESIA']
        df_pasar = df_pasar[~df_pasar['Jumlah'].astype(str).str.contains('-')]

        # Konversi kolom jumlah pasar ke numerik
        for col in ['Pasar Tradisional', 'Pusat Perbelanjaan', 'Toko Swalayan', 'Jumlah']:
            df_pasar[col] = pd.to_numeric(df_pasar[col], errors='coerce')

        # Rata-rata IKP per provinsi (2019–2024)
        df_ikp_avg = df_ikp.groupby('Province')['IKP'].mean().reset_index()

        # Kerentanan Area tahun terbaru (2024)
        df_ikp_latest = df_ikp[df_ikp['TAHUN'] == 2024][['Province', 'Kerentanan Area']].copy()

        # === MERGE SEMUA DATA ===
        df = df_disaster.merge(df_pasar, on='Province', how='left')
        df = df.merge(df_ikp_avg, on='Province', how='left')
        df = df.merge(df_ikp_latest, on='Province', how='left')

        # Hapus provinsi yang tidak lengkap datanya
        df = df.dropna(subset=['IKP', 'Jumlah', 'Total_Disaster', 'Kerentanan Area'])

        return df

    try:
        df_geo = load_geospatial_data()
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        st.stop()

    # ================= OVERVIEW KPI =================
    st.subheader("Overview Ketahanan Pangan dari Aspek Lingkungan & Infrastruktur Pasar")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Rata-rata IKP Nasional", f"{df_geo['IKP'].mean():.2f}")
    col2.metric("Provinsi Sangat Tahan", len(df_geo[df_geo['Kerentanan Area'] == 'Sangat Tahan']))
    col3.metric("Provinsi Rentan/Sangat Rentan", len(df_geo[df_geo['Kerentanan Area'].isin(['Rentan', 'Sangat Rentan'])]))
    col4.metric("Total Bencana Nasional", f"{df_geo['Total_Disaster'].sum():,}")
    col5.metric("Rata-rata Pasar/Toko per Provinsi", f"{df_geo['Jumlah'].mean():.0f}")
    st.markdown("---")

    # ================= IKP VS BENCANA =================
    st.subheader("Distribusi IKP Berdasarkan Intensitas Bencana")

    # kategorisasi bencana
    df_geo["Kategori Bencana"] = pd.qcut(
        df_geo["Total_Disaster"],
        q=3,
        labels=["Rendah", "Sedang", "Tinggi"]
    )

    fig2 = px.box(
        df_geo,
        x="Kategori Bencana",
        y="IKP",
        color="Kategori Bencana",
        title="Distribusi IKP Berdasarkan Intensitas Bencana",
        labels={"IKP": "Indeks Ketahanan Pangan"}
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.warning(
        "Distribusi IKP antar kategori bencana menunjukkan bahwa provinsi dengan intensitas bencana tinggi "
        "tidak selalu memiliki IKP yang lebih rendah. Hal ini menandakan bahwa ketahanan pangan dipengaruhi "
        "oleh faktor lain seperti akses distribusi dan infrastruktur pasar."
    )

    # ================= 1. IKP vs BENCANA =================
    st.header("Apakah Wilayah Rawan Banjir/Kekeringan = Rawan Pangan?")
    fig1 = px.scatter(
        df_geo, x="Total_Disaster", y="IKP", size="Jumlah", color="Kerentanan Area",
        hover_name="Province", size_max=70,
        title="IKP vs Total Bencana (Ukuran = Jumlah Pasar/Toko)",
        labels={"Total_Disaster": "Total Banjir + Kekeringan", "IKP": "Rata-rata IKP 2019–2024"},
        color_discrete_map={"Sangat Tahan":"#006400","Tahan":"#228B22","Agak Tahan":"#90EE90",
                            "Agak Rentan":"#FFD700","Rentan":"#FFA500","Sangat Rentan":"#FF4500"}
    )
    fig1.add_hline(y=60, line_dash="dash", line_color="gray", annotation_text="Batas Agak Tahan")
    st.plotly_chart(fig1, use_container_width=True)

    st.warning("Provinsi Jawa (bencana tinggi) → IKP tinggi. Papua (bencana rendah) → IKP sangat rendah. "
               "Kerawanan pangan lebih ditentukan oleh akses distribusi daripada frekuensi bencana.")


    # ================= IKP VS PASAR =================
    st.subheader("Distribusi IKP Berdasarkan Akses Infrastruktur Pasar")

    # kategorisasi jumlah pasar
    df_geo["Kategori Pasar"] = pd.qcut(
        df_geo["Jumlah"],
        q=3,
        labels=["Akses Rendah", "Akses Sedang", "Akses Tinggi"]
    )

    kategori_order = ["Akses Rendah", "Akses Sedang", "Akses Tinggi"]

    fig_pasar_box = px.box(
        df_geo,
        x="Kategori Pasar",
        y="IKP",
        color="Kategori Pasar",
        category_orders={"Kategori Pasar": kategori_order},
        title="Distribusi IKP Berdasarkan Tingkat Akses Pasar",
        labels={"IKP": "Indeks Ketahanan Pangan"}
    )

    st.plotly_chart(fig_pasar_box, use_container_width=True)


    # ================= PENJELASAN =================
    st.warning(
        "Infrastruktur pasar berfungsi sebagai penyangga utama ketahanan pangan, terutama dalam menjamin kelancaran distribusi dan keterjangkauan pangan."
    )

    # ================= 2. IKP vs PASAR =================
    st.header("Pengaruh Infrastruktur Pasar terhadap Ketahanan Pangan")
    fig2 = px.scatter(
        df_geo, x="Jumlah", y="IKP", size="Total_Disaster", color="Kerentanan Area",
        hover_name="Province", size_max=70, log_x=True,
        title="IKP vs Jumlah Pasar & Toko (Ukuran = Total Bencana)",
        labels={"Jumlah": "Total Fasilitas Pasar", "IKP": "Rata-rata IKP"},
        color_discrete_map={"Sangat Tahan":"#006400","Tahan":"#228B22","Agak Tahan":"#90EE90",
                            "Agak Rentan":"#FFD700","Rentan":"#FFA500","Sangat Rentan":"#FF4500"}
    )
    fig2.add_vline(x=df_geo['Jumlah'].mean(), line_dash="dash", line_color="orange")
    st.plotly_chart(fig2, use_container_width=True)

    st.success("Semakin banyak pasar & toko → semakin tinggi IKP. "
               "Infrastruktur distribusi adalah faktor terkuat ketahanan pangan di Indonesia.")

    # ================= BAR CHART RATA-RATA PASAR PER KELOMPOK =================
    st.header("Rata-rata Jumlah Pasar berdasarkan Tingkat Kerentanan")
    avg_market = df_geo.groupby("Kerentanan Area")["Jumlah"].mean().round(0).sort_values(ascending=False)
    fig3 = px.bar(x=avg_market.index, y=avg_market.values, text=avg_market.values,
                  color=avg_market.index, title="Rata-rata Jumlah Pasar/Toko per Kelompok Kerentanan",
                  color_discrete_map={"Sangat Tahan":"#006400","Tahan":"#228B22","Agak Tahan":"#90EE90",
                                      "Agak Rentan":"#FFD700","Rentan":"#FFA500","Sangat Rentan":"#FF4500"})
    fig3.update_traces(textposition='outside')
    st.plotly_chart(fig3, use_container_width=True)

    # ================= KESIMPULAN =================
    st.markdown("---")
    st.subheader("Kesimpulan & Rekomendasi")
    st.markdown("""
    - **Kerawanan pangan TIDAK sebanding dengan tingkat bencana alam**  
    - **Akses ke pasar & toko adalah prediktor terkuat ketahanan pangan**  
    - **Indonesia Timur (Papua, Maluku, NTT) paling rentan karena minim infrastruktur distribusi**  
    **Rekomendasi**: Bangun lebih banyak pasar tradisional, minimarket, dan jalur logistik di Indonesia Timur.
    """)

    # ================= DATA TABLE =================
    with st.expander("Lihat Data Lengkap"):
        st.dataframe(
            df_geo[['Province', 'IKP', 'Kerentanan Area', 'Total_Disaster', 'Jumlah',
                    'Pasar Tradisional', 'Pusat Perbelanjaan', 'Toko Swalayan']]
            .sort_values('IKP', ascending=False)
            .round(2),
            use_container_width=True
        )
# ================================================================
# SLIDE 4 — ANALISIS KERAWANAN PANGAN
# ================================================================
elif slide == 4:
    st.title("Dashboard Analisis Kerawanan Pangan Berdasarkan Gizi dan Kesehatan Keluarga")
    st.markdown("---")
    st.header("Hubungan Stunting dengan Kerawanan Pangan")

    # ================= LOAD DATA =================
    data = pd.read_csv(
        r"Dataset/Analisis_gizi_dan_kesehata_keluarga.csv"
    )

    # ================= PILIH TAHUN =================
    tahun_list = sorted(data["TAHUN"].unique())
    tahun_pilih = st.selectbox("Pilih Tahun:", tahun_list)

    df_year = data[data["TAHUN"] == tahun_pilih]

    # ================= SCATTER PLOT 1 =================
    st.subheader("Hubungan IKP dan Prevalensi Stunting")
    fig1, ax1 = plt.subplots(figsize=(7, 4))
    sns.scatterplot(
        data=df_year,
        x="IKP",
        y="prevalensi_balita_stunting",
        hue="Kerentanan Area",
        palette="Greens",
        ax=ax1
    )
    ax1.set_title("Hubungan IKP dan Prevalensi Stunting")
    ax1.set_xlabel("Indeks Ketahanan Pangan (IKP)")
    ax1.set_ylabel("Prevalensi Stunting (%)")
    ax1.grid(True)
    st.pyplot(fig1)

    # ================= SCATTER PLOT 2 + REGRESSION =================
    st.subheader("Tren Hubungan Kerawanan Pangan (IKP) vs Stunting")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=df_year,
        x="IKP",
        y="prevalensi_balita_stunting",
        hue="Kerentanan Area",
        palette="YlOrBr",
        ax=ax2
    )
    sns.regplot(
        data=df_year,
        x="IKP",
        y="prevalensi_balita_stunting",
        scatter=False,
        color="green",
        ax=ax2
    )
    ax2.set_title("Tren Hubungan Kerawanan Pangan (IKP) vs Stunting")
    st.pyplot(fig2)

    # ================= TOP 10 PROVINSI STUNTING =================
    st.subheader(f"Top 10 Provinsi dengan Stunting Tertinggi (Tahun {tahun_pilih})")

    df_prov = (
        df_year.groupby("PROVINSI")["prevalensi_balita_stunting"]
        .max()
        .reset_index()
    )

    top10_stunting = df_prov.nlargest(10, "prevalensi_balita_stunting")

    top10_stunting = top10_stunting.merge(
        df_year[["PROVINSI", "Kerentanan Area"]].drop_duplicates(),
        on="PROVINSI",
        how="left"
    )

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=top10_stunting,
        x="PROVINSI",
        y="prevalensi_balita_stunting",
        hue="Kerentanan Area",
        palette="YlGn",
        ax=ax3
    )
    ax3.set_title(f"Top 10 Provinsi dengan Stunting Tertinggi (Tahun {tahun_pilih})")
    ax3.set_xlabel("Provinsi")
    ax3.set_ylabel("Prevalensi Stunting (%)")
    plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig3)

    # ============================================================
    # ANALISIS TAMBAHAN — KONSUMSI GIZI
    # ============================================================
    st.markdown("---")
    st.header("Analisis Konsumsi Nutrisi Berdasarkan Kelompok IKP")

    # ================= DATA RADAR / HEATMAP =================
    df_radar = data.groupby("Kelompok IKP")[
        [
            "Konsumsi Energi (kkal/kap/hari)",
            "Konsumsi Protein (gram/kap/hari)",
            "Konsumsi Kalori"
        ]
    ].mean().reset_index()

    df_radar = df_radar.rename(columns={
        "Konsumsi Energi (kkal/kap/hari)": "Energi",
        "Konsumsi Protein (gram/kap/hari)": "Protein",
        "Konsumsi Kalori": "Kalori"
    })

    scaler = MinMaxScaler()
    df_norm = df_radar.copy()
    df_norm[["Energi", "Protein", "Kalori"]] = (
        scaler.fit_transform(df_norm[["Energi", "Protein", "Kalori"]]) * 10
    )
    df_norm = df_norm.round(2)

    # ================= HEATMAP =================
    st.subheader("Heatmap Konsumsi Nutrisi per Kelompok IKP")

    fig4, ax4 = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        df_norm.set_index("Kelompok IKP")[["Energi", "Protein", "Kalori"]],
        annot=True,
        cmap="Greens",
        vmin=0,
        vmax=10,
        ax=ax4
    )
    ax4.set_title("Konsumsi Nutrisi per Kelompok IKP")
    st.pyplot(fig4)

    # ================= TOP 10 PROVINSI PROTEIN TERENDAH =================
    st.subheader(f"Top 10 Provinsi dengan Konsumsi Protein Terendah (Tahun {tahun_pilih})")

    df_protein = (
        df_year.groupby("PROVINSI")["Konsumsi Protein (gram/kap/hari)"]
        .mean()
        .reset_index()
    )

    top10_low_protein = df_protein.nsmallest(
        10, "Konsumsi Protein (gram/kap/hari)"
    )

    top10_low_protein = top10_low_protein.merge(
        df_year[["PROVINSI", "Kerentanan Area"]].drop_duplicates(),
        on="PROVINSI",
        how="left"
    )

    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top10_low_protein,
        x="Konsumsi Protein (gram/kap/hari)",
        y="PROVINSI",
        hue="Kerentanan Area",
        palette="Greens_r",
        ax=ax5
    )
    ax5.set_title(
        f"Top 10 Provinsi dengan Konsumsi Protein Terendah (Tahun {tahun_pilih})"
    )
    ax5.set_xlabel("Protein (gram/kap/hari)")
    ax5.set_ylabel("Provinsi")
    plt.tight_layout()
    st.pyplot(fig5)


# ================================================================
# SLIDE 5 — ANALISIS KERAWANAN PANGAN TERHADAP PRODUKSI DAN SUPPLY CHAIN
# ================================================================
elif slide == 5:
    st.title("Dashboard Analisis Kerawanan Pangan Berdasarkan Produksi dan Supply Chain")
    st.markdown("---")
    st.header("Pengaruh Produksi Rendah terhadap Kerawanan Pangan")

    # ================= LOAD DATA =================
    data = pd.read_csv(r"Dataset/Analisis_gizi_dan_kesehata_keluarga.csv")

    # ================= PILIH TAHUN =================
    tahun_list = sorted(data["TAHUN"].unique())
    tahun_pilih = st.selectbox("Pilih Tahun:", tahun_list)

    df_year = data[data["TAHUN"] == tahun_pilih]

    # ================= SCATTER PRODUKSI vs IKP =================
    st.subheader("Hubungan Produksi Pangan dengan Ketahanan Pangan (IKP)")
    fig1, ax1 = plt.subplots(figsize=(10,6))
    sns.scatterplot(
        data=data,
        x="Produksi (ton)",
        y="IKP",
        hue="Kerentanan Area",
        palette="Greens",
        ax=ax1
    )
    ax1.set_xscale("log")
    ax1.set_xlabel("Produksi (ton) [log scale]")
    ax1.set_ylabel("IKP")
    ax1.grid(True)
    st.pyplot(fig1)

    # ================= BOX PLOT PRODUKTIVITAS & LUAS PANEN =================
    st.subheader("Perbandingan Produktivitas dan Luas Panen Berdasarkan Kerawanan Pangan")
    fig2, ax2 = plt.subplots(1, 2, figsize=(14,6))
    sns.boxplot(
        data=data,
        x="Kerentanan Area",
        y="Produktivitas (ku/ha)",
        palette="Greens",
        ax=ax2[0]
    )
    ax2[0].set_title("Produktivitas vs Kerawanan Pangan")
    sns.boxplot(
        data=data,
        x="Kerentanan Area",
        y="Luas Panen (ha)",
        palette="Greens",
        ax=ax2[1]
    )
    ax2[1].set_title("Luas Panen vs Kerawanan Pangan")
    plt.tight_layout()
    st.pyplot(fig2)

    # ================= TOP 10 PRODUKSI RENDAH =================
    st.subheader(f"Top 10 Provinsi dengan Produksi Padi Terendah ({tahun_pilih})")
    df_prod = df_year.groupby("PROVINSI")["Produksi (ton)"].max().reset_index()
    top10_low_production = df_prod.nsmallest(10, "Produksi (ton)")
    top10_low_production = top10_low_production.merge(
        df_year[["PROVINSI","Kerentanan Area"]].drop_duplicates(),
        on="PROVINSI",
        how="left"
    )

    fig3, ax3 = plt.subplots(figsize=(10,5))
    sns.barplot(
        data=top10_low_production,
        x="Produksi (ton)",
        y="PROVINSI",
        hue="Kerentanan Area",
        palette="YlGn",
        ax=ax3
    )
    plt.tight_layout()
    st.pyplot(fig3)

    # ================= SCATTER IMPORT vs IKP =================
    st.subheader("Pengaruh Ketergantungan Impor Non-Migas terhadap IKP")
    fig4, ax4 = plt.subplots(figsize=(10,6))
    sns.scatterplot(
        data=data,
        x="Import_Non_Migas",
        y="IKP",
        hue="Kerentanan Area",
        palette="Greens",
        ax=ax4
    )
    ax4.set_xlabel("Nilai Impor Non-Migas")
    ax4.set_ylabel("IKP")
    st.pyplot(fig4)

    # ================= SCATTER + REGRESSION IMPORT vs IKP =================
    st.subheader("Hubungan Impor Non-Migas vs IKP (dengan Trendline)")
    fig5, ax5 = plt.subplots(figsize=(9,6))
    sns.scatterplot(
        data=data,
        x="Import_Non_Migas",
        y="IKP",
        hue="Kerentanan Area",
        palette="Greens",
        ax=ax5
    )
    sns.regplot(
        data=data,
        x="Import_Non_Migas",
        y="IKP",
        scatter=False,
        color="darkgreen",
        ax=ax5
    )
    st.pyplot(fig5)

    # ================= TOP 10 IMPOR TERTINGGI =================
    st.subheader(f"Top 10 Provinsi dengan Nilai Import Non-Migas Tertinggi ({tahun_pilih})")
    df_imp = df_year.groupby("PROVINSI")["Import_Non_Migas"].max().reset_index()
    top10_import = df_imp.nlargest(10, "Import_Non_Migas")
    top10_import = top10_import.merge(
        df_year[["PROVINSI","Kerentanan Area"]].drop_duplicates(),
        on="PROVINSI",
        how="left"
    )

    fig6, ax6 = plt.subplots(figsize=(10,6))
    sns.barplot(
        data=top10_import,
        x="Import_Non_Migas",
        y="PROVINSI",
        hue="Kerentanan Area",
        palette="Greens",
        ax=ax6
    )
    plt.tight_layout()
    st.pyplot(fig6)

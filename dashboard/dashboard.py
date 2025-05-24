import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi awal
st.set_page_config(page_title="Dashboard Bike Sharing", layout="wide")
sns.set(style="whitegrid")

# Load data
day_df = pd.read_csv("dashboard/day.csv")

# Preprocessing
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['season'] = day_df['season'].astype('category').cat.rename_categories({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weathersit'] = day_df['weathersit'].map({
    1: 'Clear/Few Clouds', 
    2: 'Mist/Cloudy', 
    3: 'Light Rain/Snow', 
    4: 'Heavy Rain/Snow'
})
day_df['year'] = day_df['dteday'].dt.year
day_df['day_type'] = day_df['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

# Sidebar
st.sidebar.header("Filter")
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(day_df['year'].unique()))
df_filtered = day_df[day_df['year'] == selected_year]

# 1. Tren penggunaan per musim
st.header("1. Tren Penggunaan Bike Sharing Setiap Musim")
fig1, ax1 = plt.subplots()
sns.barplot(data=df_filtered, x="season", y="cnt", estimator="mean", ci=None, palette="viridis", ax=ax1)
ax1.set_title("Rata-rata Penyewaan per Musim")
ax1.set_xlabel("Musim")
ax1.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig1)

# 2. Perbedaan Hari Kerja vs Akhir Pekan
st.header("2. Perbedaan Penyewaan antara Hari Kerja dan Akhir Pekan")
fig2, ax2 = plt.subplots()
sns.barplot(data=df_filtered, x="season", y="cnt", hue="day_type", estimator="mean", ci=None, palette="coolwarm", ax=ax2)
ax2.set_title("Penyewaan berdasarkan Musim dan Kategori Hari")
ax2.set_xlabel("Musim")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.legend(title="Hari")
st.pyplot(fig2)

# 3. Pengaruh Musim dan Cuaca
st.header("3. Pengaruh Musim dan Cuaca terhadap Peminjaman")

# Hitung total dan rata-rata peminjaman berdasarkan musim dan cuaca
total_by_weather = day_df.groupby(["season", "weathersit"], observed=False)["cnt"].sum().reset_index()
avg_by_weather = day_df.groupby(["season", "weathersit"], observed=False)["cnt"].mean().reset_index()
combined_weather = total_by_weather.merge(avg_by_weather, on=["season", "weathersit"], suffixes=("_total", "_avg"))

st.subheader("Tabel Ringkasan Peminjaman per Musim dan Cuaca")
st.dataframe(combined_weather)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Total Peminjaman**")
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=combined_weather, x="season", y="cnt_total", hue="weathersit", ax=ax3)
    ax3.set_ylabel("Total Penyewaan")
    st.pyplot(fig3)

with col2:
    st.markdown("**Rata-rata Harian Peminjaman**")
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=combined_weather, x="season", y="cnt_avg", hue="weathersit", ax=ax4)
    ax4.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig4)

# 4. Tren pengguna per tahun
st.header("4. Tren Pengguna Sepeda per Tahun")

yearly = day_df.groupby('year')[['casual', 'registered', 'cnt']].sum()
yearly.index = yearly.index.astype(str)

change = yearly.pct_change().iloc[1] * 100
summary = yearly.astype(str)
summary.loc['% Change'] = change.apply(lambda v: f"{v:.2f}%" if pd.notna(v) else "-")
summary.iloc[:-1] = summary.iloc[:-1].applymap(lambda x: f"{int(x):,}")

st.subheader("Tabel Total Pengguna Tahunan")
st.dataframe(summary)

fig5, ax5 = plt.subplots()
yearly.T.plot(kind="bar", ax=ax5)
ax5.set_title("Total Pengguna Sepeda: per Tahun")
ax5.set_ylabel("Jumlah")
ax5.set_xlabel("Tipe Pengguna")
st.pyplot(fig5)

# Insight Ringkasan
st.markdown("""
---
### Insight Singkat:
- **Penyewaan tertinggi terjadi saat musim gugur dan musim panas.**
- **Hari kerja lebih sibuk di musim panas dan gugur, tapi akhir pekan ramai saat musim semi.**
- **Cuaca cerah mendukung penyewaan tinggi, sedangkan hujan salju berat membuat penyewaan nol.**
- **Tahun 2012 menunjukkan lonjakan signifikan pengguna, terutama pengguna terdaftar.**
""")

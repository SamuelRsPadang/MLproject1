import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Data
day_df = pd.read_csv("dashboard/day.csv")

# Preprocessing
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
day_df['season'] = day_df['season'].astype('category').cat.rename_categories({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['year'] = day_df['dteday'].dt.year
day_df['day_type'] = day_df['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})

# Streamlit Sidebar
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(day_df['year'].unique()))

df_filtered = day_df[day_df['year'] == selected_year]

# Tren penggunaan bike sharing setiap musim
st.header("Tren Penggunaan Bike Sharing Setiap Musim")
fig, ax = plt.subplots()
sns.barplot(data=df_filtered, x="season", y="cnt", estimator="mean", ci=None, palette="viridis", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)

# Ide Kreatif: Heatmap hubungan antara faktor cuaca dan penyewaan
st.header("Heatmap Hubungan Faktor Cuaca dan Penyewaan")
fig, ax = plt.subplots(figsize=(10, 5))
corr = day_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)
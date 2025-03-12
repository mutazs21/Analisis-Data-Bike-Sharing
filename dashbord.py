import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
day_data = pd.read_csv("day.csv")
hour_data = pd.read_csv("hour.csv")

# Konversi tanggal
day_data["dteday"] = pd.to_datetime(day_data["dteday"])
hour_data["dteday"] = pd.to_datetime(hour_data["dteday"])

# Judul Dashboard
st.title("Analisis Data Bike Sharing 📊")

# Sidebar untuk memilih visualisasi
st.sidebar.header("Pilih Analisis")
option = st.sidebar.selectbox(
    "Pilih Analisis yang Ingin Ditampilkan",
    ["Tren Penyewaan Mingguan", "Tren Penyewaan Bulanan", "Distribusi Penyewaan Berdasarkan Musim", "Waktu Paling Sibuk",]
)

# Fitur Filter Tanggal
st.sidebar.subheader("Filter Data Berdasarkan Tanggal")
start_date = st.sidebar.date_input("Mulai dari:", day_data["dteday"].min())
end_date = st.sidebar.date_input("Sampai:", day_data["dteday"].max())

# rentang tanggal
if start_date > end_date:
    st.sidebar.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir!")

# Filter data berdasarkan tanggal yang dipilih
filtered_day_data = day_data[(day_data["dteday"] >= pd.to_datetime(start_date)) & (day_data["dteday"] <= pd.to_datetime(end_date))]

# Analisis Tren Penyewaan Mingguan
if option == "Tren Penyewaan Mingguan":
    st.subheader("📅 Tren Penyewaan Sepeda per Hari dalam Seminggu")

    # Agregasi rata-rata jumlah penyewaan per hari dalam seminggu
    weekly_trend = filtered_day_data.groupby(filtered_day_data["dteday"].dt.day_name())["cnt"].mean().reset_index()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekly_trend["dteday"] = pd.Categorical(weekly_trend["dteday"], categories=order, ordered=True)
    weekly_trend = weekly_trend.sort_values("dteday")

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=weekly_trend, x="dteday", y="cnt", ax=ax, color="royalblue")
    ax.set_title("Rata-rata Penyewaan Sepeda per Hari dalam Seminggu")
    ax.set_xlabel("Hari dalam Seminggu")
    ax.set_ylabel("Rata-rata Penyewaan")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Tren Penyewaan Sepeda Bulanan
elif option == "Tren Penyewaan Bulanan":
    st.subheader("📆 Tren Penyewaan Sepeda Bulanan")

    # Agregasi jumlah penyewaan per bulan
    monthly_trend = filtered_day_data.groupby("mnth")["cnt"].sum().reset_index()

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=monthly_trend, x="mnth", y="cnt", marker="o", color="b", ax=ax)
    ax.set_title("Tren Penyewaan Sepeda Bulanan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
    ax.grid()
    st.pyplot(fig)

# Distribusi Penyewaan Berdasarkan Musim
elif option == "Distribusi Penyewaan Berdasarkan Musim":
    st.subheader("🌤️ Distribusi Penyewaan Sepeda Berdasarkan Musim")

    # Mapping nama musim
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    filtered_day_data["season"] = filtered_day_data["season"].map(season_labels)

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=filtered_day_data, x="season", y="cnt", ax=ax, palette="viridis")
    ax.set_title("Frekuensi Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

# Waktu Paling Sibuk
elif option == "Waktu Paling Sibuk":
    st.subheader("⏰ Waktu Paling Sibuk dalam Penyewaan Sepeda")

    # Filter juga hour_data agar sesuai dengan tanggal yang dipilih
    filtered_hour_data = hour_data[(hour_data["dteday"] >= pd.to_datetime(start_date)) & (hour_data["dteday"] <= pd.to_datetime(end_date))]

    # Agregasi jumlah penyewaan per jam
    busy_hours = filtered_hour_data.groupby("hr")["cnt"].mean().reset_index()

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=busy_hours, x="hr", y="cnt", ax=ax, marker="o", color="red")
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(0, 24))
    st.pyplot(fig)

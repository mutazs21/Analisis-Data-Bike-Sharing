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
st.title("Analisis Data Bike Sharing")

# Sidebar untuk memilih visualisasi
st.sidebar.header("Pilih Analisis")
option = st.sidebar.selectbox(
    "Pilih Analisis yang Ingin Ditampilkan",
    ["Tren Penyewaan Mingguan", "Tren Penyewaan Bulanan", "Distribusi Penyewaan Berdasarkan Musim", "Waktu Paling Sibuk",]
)

# Analisis Tren Penyewaan Mingguan
if option == "Tren Penyewaan Mingguan":
    st.subheader("📅 Tren Penyewaan Sepeda per Hari dalam Seminggu")
    
    # Agregasi rata-rata jumlah penyewaan per hari dalam seminggu
    weekly_trend = day_data.groupby(day_data["dteday"].dt.day_name())["cnt"].mean().reset_index()
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
    
    # Insight
    st.markdown("""
    ### Insight:
    - Jumlah penyewaan sepeda lebih tinggi pada Sabtu dan Minggu, menunjukkan bahwa sepeda lebih banyak digunakan untuk aktivitas rekreasi.
    - Rata-rata penyewaan sepeda paling rendah terjadi pada hari Senin, kemungkinan karena orang masih beradaptasi setelah akhir pekan.
    """)
    
# Tren Penyewaan Sepeda Bulanan
elif option == "Tren Penyewaan Bulanan":
    st.subheader("📆 Tren Penyewaan Sepeda Bulanan")

    # Agregasi jumlah penyewaan per bulan
    monthly_trend = day_data.groupby("mnth")["cnt"].sum().reset_index()

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
    
    # Insight
    st.markdown("""
    ### Insight:
    - Penyewaan sepeda cenderung meningkat pada bulan-bulan musim panas (Juni Agustus).
    - Penurunan terlihat di musim dingin (Desember - Februari).
    """)


# Distribusi Penyewaan Berdasarkan Musim
elif option == "Distribusi Penyewaan Berdasarkan Musim":
    st.subheader("🌤️ Distribusi Penyewaan Sepeda Berdasarkan Musim")

    # Mapping nama musim
    season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    day_data["season"] = day_data["season"].map(season_labels)

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=day_data, x="season", y="cnt", ax=ax, palette="viridis")
    ax.set_title("Frekuensi Penyewaan Sepeda Berdasarkan Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)
    
    # Insight
    st.markdown("""
    ### Insight:
    - Penyewaan paling tinggi terjadi pada musim panas, kemungkinan karena cuaca lebih nyaman untuk bersepeda.
    - Penyewaan terendah pada musim dingin, mungkin karena kondisi cuaca yang lebih sulit.
    """)

# Waktu Paling Sibuk
elif option == "Waktu Paling Sibuk":
    st.subheader("⏰ Waktu Paling Sibuk dalam Penyewaan Sepeda")

    # Agregasi jumlah penyewaan per jam
    busy_hours = hour_data.groupby("hr")["cnt"].mean().reset_index()

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10,5))
    sns.lineplot(data=busy_hours, x="hr", y="cnt", ax=ax, marker="o", color="red")
    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.set_xticks(range(0, 24))
    st.pyplot(fig)
    
    #Insight
    st.markdown("""
    ### Insight:
    - Waktu penyewaan paling sibuk terjadi pada jam **07:00 - 09:00** dan **17:00 - 19:00** (jam berangkat & pulang kerja).
    - Waktu paling sepi adalah setelah tengah malam hingga subuh.
    """)
    

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Header
st.title("Dashboard Analisis Data Penyewaan Sepeda")
st.write(
    "Dashboard ini menampilkan hasil analisis data penyewaan sepeda dari dataset day.csv dan hour.csv."
)

tab1, tab2 = st.tabs(["Day.csv", "Hour.csv"])

# Load data
day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Ringkasan Data Day.csv tab1
with tab1:
    st.header("Ringkasan Data day.csv")
    st.write("Jumlah baris dan kolom:", day_df.shape)
    st.dataframe(day_df.head())  # Menampilkan 5 data teratas

    # Rata-rata Penyewaan Sepeda per Bulan
    st.header("Rata-rata Penyewaan Sepeda per Bulan")
    df_month = day_df.groupby("mnth", as_index=False)["cnt"].mean()
    df_month["mnth"] = df_month["mnth"].map(
        {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df_month, x="mnth", y="cnt", ax=ax, palette="viridis")
    ax.set_title("Rata-rata Penyewaan Sepeda per Bulan")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Filter Data Interaktif
    st.header("Filter Data Penyewaan")
    selected_month = st.selectbox("Pilih Bulan:", df_month["mnth"])
    filtered_data = day_df[
        day_df["mnth"] == df_month[df_month["mnth"] == selected_month].index[0] + 1
    ]

    st.write(f"Data Penyewaan Sepeda untuk Bulan {selected_month}:")
    st.dataframe(filtered_data)

    # Unduh Data
    csv_data = day_df.to_csv(index=False)
    st.download_button(
        "Unduh Data Penyewaan Sepeda",
        data=csv_data,
        file_name="data_sewa_sepeda_hari.csv",
        mime="text/csv",
    )

    # Header
    st.header("Analisis Penggunaan Sepeda pada Tahun 2012")
    st.write(
        "Hasil analisis ini menunjukkan pola penggunaan sepeda berdasarkan bulan pada tahun 2012"
    )
    # Filter data untuk tahun 2012
    data_2012 = day_df[day_df["yr"] == 1]
    monthly_avg_2012 = data_2012.groupby("mnth", as_index=False)["cnt"].mean()
    monthly_avg_2012["mnth"] = monthly_avg_2012["mnth"].map(
        {
            1: "Jan",
            2: "Feb",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }
    )

    # Header
    st.header("Penggunaan Sepeda pada Tahun 2012")
    st.write(
        "Figure di bawah ini menunjukkan rata-rata penggunaan sepeda per bulan pada tahun 2012."
    )

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    # Line
    sns.lineplot(data=monthly_avg_2012, x="mnth", y="cnt", marker="o", ax=ax)
    ax.set_title("Rata-rata Penggunaan Sepeda per Bulan pada Tahun 2012")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.grid(axis="y", linestyle="--", alpha=0.6)
    st.pyplot(fig)

    st.write(
        "Pada analisis ini, terlihat bahwa rata-rata penggunaan sepeda tertinggi terjadi pada bulan September."
    )

    # Header
    st.header("Penggunaan Sepeda berdasarkan Tipe Hari")
    st.write(
        "Figure di bawah ini menunjukkan rata-rata penggunaan sepeda berdasarkan tipe hari pada tahun 2012."
    )

    year_day_copy = data_2012.copy()
    year_day_copy["day_type"] = data_2012.apply(
        lambda row: (
            "Holiday"
            if row["holiday"] == 1
            else ("Weekend" if row["weekday"] in [0, 6] else "Working Day")
        ),
        axis=1,
    )
    day_type_avg = year_day_copy.groupby("day_type")["cnt"].mean()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=day_type_avg.index, y=day_type_avg, ax=ax, palette="viridis")
    ax.set_title("Rata-rata Penggunaan Sepeda berdasarkan Hari")
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    st.write(
        "Pada analisis ini, terlihat bahwa rata-rata penggunaan sepeda lebih tinggi pada hari kerja dibandingkan dengan hari libur dan akhir pekan."
    )

    # Header
    st.header("Analisis Penggunaan Sepeda pada Tahun 2012 per Hari")
    st.write(
        "Figure di bawah ini menunjukkan rata-rata penggunaan sepeda per hari dalam seminggu pada tahun 2012."
    )

    weekday_avg = data_2012.groupby("weekday")["cnt"].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    weekday_avg.plot(kind="line", marker="o", color="lightgreen")
    ax.set_title("Rata-rata Penggunaan Sepeda per Hari dalam Seminggu", fontsize=14)
    ax.set_xlabel("Hari dalam Seminggu (0 = Minggu, 6 = Sabtu)", fontsize=12)
    ax.set_ylabel("Rata-rata Pengguna Sepeda", fontsize=12)
    ax.set_xticks(ticks=range(7))
    ax.set_xticklabels(["Ming", "Sen", "Sel", "Rab", "Kam", "Jum", "Sab"])
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig)

    st.write(
        "Pada analisis ini, terlihat bahwa rata-rata penggunaan sepeda lebih tinggi pada hari kerja dibandingkan dengan akhir pekan."
    )

with tab2:
    st.header("Ringkasan Data hour.csv")
    st.write("Jumlah baris dan kolom:", hour_df.shape)
    st.dataframe(hour_df.head())  # Menampilkan 5 data teratas

    # Rata-rata Penyewaan Sepeda per Jam
    st.header("Rata-rata Penyewaan Sepeda per Jam")
    df_hour = hour_df.groupby("hr", as_index=False)["cnt"].mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df_hour, x="hr", y="cnt", marker="o", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    # Unduh Data
    csv_data = hour_df.to_csv(index=False)
    st.download_button(
        "Unduh Data Penyewaan Sepeda",
        data=csv_data,
        file_name="data_sewa_sepeda_jam.csv",
        mime="text/csv",
    )

    # Header
    st.header("Analisis Penyewaan Sepeda Berdasarkan Jam")
    st.write(
        """
        Visualisasi ini menunjukkan pola penyewaan sepeda berdasarkan jam. Anda dapat 
        memfilter data berdasarkan kategori: Hari Kerja (Working Day), Akhir Pekan (Weekend), 
        dan Hari Libur (Holiday). Defaultnya adalah Hari Kerja (Working Day).
        """
    )

    # Tambahkan filter kategori
    filter_option = st.selectbox(
        "Pilih Kategori:",
        options=["Working Day", "Weekend", "Holiday"],
        index=0,  # Default ke "Working Day"
    )

    # Filter data berdasarkan kategori
    if filter_option == "Working Day":
        filtered_data = hour_df[hour_df["workingday"] == 1]
    elif filter_option == "Weekend":
        filtered_data = hour_df[
            (hour_df["workingday"] == 0) & (hour_df["holiday"] == 0)
        ]
    elif filter_option == "Holiday":
        filtered_data = hour_df[hour_df["holiday"] == 1]

    workingday_peak_avg = (
        filtered_data[
            (filtered_data["hr"].between(7, 9)) | (filtered_data["hr"].between(17, 20))
        ]
        .groupby("hr")["cnt"]
        .mean()
    )

    workingday_non_peak_avg = (
        filtered_data[
            ~(
                (filtered_data["hr"].between(7, 9))
                | (filtered_data["hr"].between(17, 20))
            )
        ]
        .groupby("hr")["cnt"]
        .mean()
    )

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(
        workingday_peak_avg.index,
        workingday_peak_avg,
        color="lightblue",
        label="Jam Kerja (7-9 & 17-20)",
        edgecolor="black",
    )

    # Bar chart untuk jam non-kerja
    ax.bar(
        workingday_non_peak_avg.index,
        workingday_non_peak_avg,
        color="lightcoral",
        alpha=0.6,
        label="Jam Non-Kerja",
        edgecolor="black",
    )

    # Menambahkan judul dan label
    ax.set_title(
        "Perbandingan Penyewaan Sepeda: Jam Kerja vs Non-Kerja (Hari Kerja)",
        fontsize=14,
    )
    ax.set_xlabel("Jam", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewa Sepeda", fontsize=12)

    # Mengatur ticks pada sumbu x
    ax.set_xticks(range(24))
    ax.set_xticklabels([f"{i}:00" for i in range(24)], rotation=45)

    # Menambahkan grid pada sumbu y
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    # Menambahkan legend
    ax.legend()

    # Menampilkan plot
    st.pyplot(fig)

    st.write(
        "Dari analisis data hour.csv, jam sibuk (pagi pukul 7-9 dan sore pukul 17-20) memiliki jumlah penyewaan sepeda yang jauh lebih tinggi dibandingkan dengan jam non-sibuk pada hari kerja. Hal ini mengindikasikan bahwa sepeda sering digunakan sebagai alat transportasi utama selama jam-jam perjalanan kerja. Pola ini jelas terlihat pada hari kerja, sedangkan pada hari libur penggunaan sepeda lebih merata sepanjang hari. Dan untuk pada hari libur penggunaan sepeda lebih merata sepanjang hari."
    )

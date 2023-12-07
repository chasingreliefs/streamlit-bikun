import streamlit as st
import pandas as pd
import json
from google.cloud import firestore
from google.oauth2 import service_account
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time

# Fungsi untuk mendapatkan data Firestore
def get_firestore_data():
    key_dict = json.loads(st.secrets["textkey"])
    creds = service_account.Credentials.from_service_account_info(key_dict)
    db = firestore.Client(credentials=creds, project="desprobikun")
    doc_ref = db.collection("data").document("1")
    doc = doc_ref.get()
    return doc.to_dict()

# Fungsi untuk menampilkan grafik jumlah orang di halte
def show_people_graph(data):
    timestamps = [pd.to_datetime(ts) for ts in data["timestamp"]]
    jumlah_orang = data["Orang"]

    fig, ax = plt.subplots()
    ax.plot(timestamps, jumlah_orang, label='Jumlah Orang')
    ax.xaxis.set_major_locator(mdates.HourLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.set_xlabel('Waktu')
    ax.set_ylabel('Jumlah Orang')
    ax.set_title('Grafik Jumlah Orang di Halte')
    
    st.pyplot(fig)

# Fungsi untuk menampilkan jumlah orang dan skala parameter
def show_people_count_and_scale(data):
    jumlah_orang = data["Orang"]
    
    st.write(f"Jumlah Orang di Halte: {jumlah_orang[0] if jumlah_orang else 0}")
    
    if jumlah_orang and jumlah_orang[0] <= 3:
        skala = "Sangat Sepi"
    elif jumlah_orang and 5 < jumlah_orang[0] <= 6:
        skala = "Sepi"
    elif jumlah_orang and 10 < jumlah_orang[0] <= 10:
        skala = "Normal"
    elif jumlah_orang and 20 < jumlah_orang[0] <= 15:
        skala = "Rame"
    else:
        skala = "Sangat Rame"
    
    st.write(f"Skala Parameter: {skala}")

# Fungsi untuk menampilkan status kedatangan Bis Kuning
def show_bikun_status(data):
    bikun_status = data["Bikun"]
    if bikun_status:
        st.write("Bis Kuning ada di halte.")
    else:
        st.write("Bis Kuning tidak ada di halte.")

# Fungsi untuk menampilkan foto keadaan halte terkini
def show_current_halte_photo(data):
    foto_halte_url = data["FotoHalte"]
    if foto_halte_url:
        st.image(foto_halte_url, caption='Keadaan Halte Terkini', use_column_width=True)
    else:
        st.write("Foto keadaan halte tidak tersedia.")

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Desain Proyek Teknik Elektro : Kelompok 3.5"
)
st.title('Crowd Monitoring dan Kedatangan Bikun di Halte FT UI :bus:💨')

while True:
    # Mendapatkan data Firestore
    data_firestore = get_firestore_data()

    # Membersihkan area sebelumnya
    st.text("")  

    # Menampilkan grafik jumlah orang di halte
    st.header('Grafik Jumlah Orang di Halte')
    previous_chart = st.empty()
    show_people_graph(data_firestore)
    previous_chart.text("")  # Membersihkan area sebelumnya

    # Menampilkan jumlah orang dan skala parameter
    st.header('Informasi Jumlah Orang dan Skala Parameter')
    previous_info = st.empty()
    show_people_count_and_scale(data_firestore)
    previous_info.text("")  # Membersihkan area sebelumnya

    # Menampilkan status kedatangan Bis Kuning
    st.header('Status Kedatangan Bis Kuning')
    previous_status = st.empty()
    show_bikun_status(data_firestore)
    previous_status.text("")  # Membersihkan area sebelumnya

    # Menampilkan foto keadaan halte terkini
    st.header('Foto Keadaan Halte Terkini')
    previous_photo = st.empty()
    show_current_halte_photo(data_firestore)
    previous_photo.text("")  # Membersihkan area sebelumnya

    # Menunggu 10 detik sebelum memperbarui data kembali
    time.sleep(10)

import os
import tempfile
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

# Optional import untuk unduh model dari Google Drive
try:
    import gdown
except ImportError:
    gdown = None

st.set_page_config(page_title="Prediksi Stunting", page_icon="🍼", layout="wide")

# === Konfigurasi Model & Dataset ===
GOOGLE_DRIVE_FILE_ID = "1pyjGOgXPauxs5eisE_plXbqU1vbWTINr"
DRIVE_URL = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
LOCAL_MODEL_PATH = "stunting_model.pkl"
DATA_CSV = "stunting_data.csv"

@st.cache_data(show_spinner=False)
def load_data(path=DATA_CSV):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

@st.cache_resource(show_spinner=True)
def load_model():
    # Unduh model jika belum ada
    if not os.path.exists(LOCAL_MODEL_PATH):
        if gdown is None:
            raise RuntimeError("gdown belum terpasang. Tambahkan ke requirements.txt.")
        tmp = os.path.join(tempfile.gettempdir(), "tmp_model.pkl")
        gdown.download(DRIVE_URL, tmp, quiet=False)
        os.replace(tmp, LOCAL_MODEL_PATH)
    return joblib.load(LOCAL_MODEL_PATH)

# Sidebar Menu
st.sidebar.title("Menu")
mode = st.sidebar.radio("Pilih Mode:", ["Dashboard", "Predict"])

# === DASHBOARD ===
if mode == "Dashboard":
    st.title("Dashboard Prediksi Stunting")
    df = load_data()

    if df.empty:
        st.warning("`stunting_data.csv` tidak ditemukan. Upload dataset ke proyek.")
    else:
        st.subheader("Visualisasi Stunting per Daerah (KBTEKS)")
        if "KBTEKS" in df.columns and "stunting" in df.columns:
            agg = df.groupby("KBTEKS")["stunting"].sum().reset_index()
            fig = px.bar(agg, x="KBTEKS", y="stunting", labels={"stunting":"Jumlah Stunting","KBTEKS":"Daerah"})
            st.plotly_chart(fig, use_container_width=True)
           
            st.subheader("Persentase Stunting")
            vc = df["stunting"].value_counts().rename({0:"Tidak", 1:"Ya"})
            fig2 = px.pie(values=vc.values, names=vc.index, title="Persentase Stunting")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Kolom `KBTEKS` atau `stunting` tidak ada di dataset.")

# === PREDICT ===
else:
    st.title("Prediksi Risiko Stunting")
    try:
        model = load_model()
    except Exception as err:
        st.error(f"Gagal load model: {err}")
        st.stop()

    st.markdown("Isi data dibawah untuk memprediksi stunting.")

    overweight = st.selectbox("Overweight", ["0", "1"])
    tinggi_balita = st.number_input("Tinggi Badan Balita (cm)", min_value=30.0, max_value=140.0, value=75.0)
    pendidikan_ibu = st.selectbox("Pendidikan Ibu", list(range(1,8)))
    berat_balita = st.number_input("Berat Badan Balita (kg)", min_value=1.0, max_value=30.0, value=8.5)
    panjang_lahir = st.number_input("Panjang Badan Saat Lahir (cm)", min_value=25.0, max_value=65.0, value=49.0)
    pekerjaan_ibu = st.selectbox("Pekerjaan Ibu", list(range(1,10)))
    berat_lahir = st.number_input("Berat Badan Saat Lahir (kg)", min_value=0.8, max_value=6.0, value=3.0)
    usia_hamil = st.number_input("Usia Kehamilan Saat Lahir (minggu)", min_value=20, max_value=45, value=38)
    lingkar_kepala = st.number_input("Lingkar Kepala Saat Lahir (cm)", min_value=20.0, max_value=45.0, value=33.0)

    if st.button("Prediksi"):
        X = pd.DataFrame([[
            int(overweight), tinggi_balita, pendidikan_ibu,
            berat_balita, panjang_lahir, pekerjaan_ibu,
            berat_lahir, usia_hamil, lingkar_kepala
        ]], columns=[
            "overweight", "tinggi_badan_balita", "pendidikan_ibu",
            "berat_badan_balita", "panjang_badan_saat_lahir", "pekerjaan_ibu",
            "berat_badan_saat_lahir", "usia_kehamilan_saat_lahiran", "lingkar_kepala_saat_lahir"
        ])

        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0][1] if hasattr(model, "predict_proba") else None
        label = "Stunting" if pred == 1 else "Tidak Stunting"
        if proba is not None:
            st.success(f"**{label}** (Confidence: {proba:.2%})")
        else:
            st.success(f"**{label}**")

        with st.expander("Lihat input yang digunakan"):
            st.write(X)

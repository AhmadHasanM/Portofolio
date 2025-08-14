import os
import tempfile
import shutil
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
DATA_CSV = "stunting_data.xlsx"

# Mapping kolom user-friendly → kolom asli dataset/model
column_mapping = {
    'Jenis Kelamin': 'B4K4',
    'Usia Kehamilan saat lahir (bulan)': 'I04',
    'Berat Badan saat lahir (kg)': 'I05A',
    'Tinggi Badan (cm)': 'I07',
    'Lingkar Kepala': 'I10',
    'Kondisi Kesehatan Balita': 'J01B',
    'Berat Badan': 'J01C',
    'Tinggi Badan': 'J02B',
    'Kondisi saat diukur': 'J02C',
    'Status Kawin Ibu': 'B4K5_ibu',
    'Pendidikan Ibu': 'B4K8_ibu',
    'Pekerjaan Ibu': 'B4K9_ibu',
    'Status kehamilan Ibu Saat Ini': 'B4K10_ibu',
    'Kepemilikan Jaminan Kesehatan Ibu': 'B4K11_ibu',
    'Pendidikan Kepala Keluarga': 'B4K8_KK',
    'Pekerjaan Kepala Keluarga': 'B4K9_KK'
}

@st.cache_data(show_spinner=False)
def load_data(path=DATA_CSV):
    return pd.read_csv(path) if os.path.exists(path) else pd.DataFrame()

@st.cache_resource(show_spinner=True)
def load_model():
    if not os.path.exists(LOCAL_MODEL_PATH):
        if gdown is None:
            raise RuntimeError("gdown belum terpasang. Tambahkan ke requirements.txt.")
        tmp = os.path.join(tempfile.gettempdir(), "tmp_model.pkl")
        gdown.download(DRIVE_URL, tmp, quiet=False)
        shutil.move(tmp, LOCAL_MODEL_PATH)  # Ganti os.replace → shutil.move
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

    # Input form berdasarkan mapping
    user_inputs = {}
    for label in column_mapping.keys():
        if "kg" in label.lower():
            user_inputs[label] = st.number_input(label, min_value=0.0, max_value=100.0, value=0.0)
        elif "cm" in label.lower():
            user_inputs[label] = st.number_input(label, min_value=0.0, max_value=200.0, value=0.0)
        elif "(1=ya" in label.lower() or "(1=ya," in label.lower():
            user_inputs[label] = st.selectbox(label, [0, 1])
        elif "umur" in label.lower() and "bulan" in label.lower():
            user_inputs[label] = st.number_input(label, min_value=0, max_value=60, value=0)
        elif "umur" in label.lower():
            user_inputs[label] = st.number_input(label, min_value=0, max_value=100, value=0)
        elif "pendidikan" in label.lower() or "pekerjaan" in label.lower() or "status" in label.lower():
            user_inputs[label] = st.number_input(label, min_value=0, max_value=10, value=0)
        else:
            user_inputs[label] = st.number_input(label, value=0.0)

    if st.button("Prediksi"):
        X = pd.DataFrame([[user_inputs[label] for label in column_mapping.keys()]],
                         columns=column_mapping.values())

        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0][1] if hasattr(model, "predict_proba") else None
        label_pred = "Stunting" if pred == 1 else "Tidak Stunting"

        if proba is not None:
            st.success(f"**{label_pred}** (Confidence: {proba:.2%})")
        else:
            st.success(f"**{label_pred}**")

        with st.expander("Lihat input yang digunakan"):
            st.write(X)


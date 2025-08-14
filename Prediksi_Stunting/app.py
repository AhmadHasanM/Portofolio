import os
import tempfile
import shutil
import joblib
import pandas as pd
import streamlit as st
import plotly.express as px

try:
    import gdown
except ImportError:
    gdown = None

st.set_page_config(page_title="Prediksi Stunting", page_icon="🍼", layout="wide")

# === Path & Konfigurasi ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GOOGLE_DRIVE_FILE_ID = "1pyjGOgXPauxs5eisE_plXbqU1vbWTINr"
DRIVE_URL = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
LOCAL_MODEL_PATH = os.path.join(BASE_DIR, "stunting_model.pkl")
DATA_CSV = os.path.join(BASE_DIR, "stunting_data.csv")

# === Fungsi Load Data ===
@st.cache_data(show_spinner=False)
def load_data(path=DATA_CSV):
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

# === Fungsi Load Model ===
@st.cache_resource(show_spinner=True)
def load_model():
    if not os.path.exists(LOCAL_MODEL_PATH):
        if gdown is None:
            raise RuntimeError("gdown belum terpasang. Tambahkan ke requirements.txt.")
        tmp = os.path.join(tempfile.gettempdir(), "tmp_model.pkl")
        gdown.download(DRIVE_URL, tmp, quiet=False)
        shutil.move(tmp, LOCAL_MODEL_PATH)
    return joblib.load(LOCAL_MODEL_PATH)

# === Sidebar ===
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
            fig = px.bar(
                agg, 
                x="KBTEKS", 
                y="stunting", 
                labels={"stunting": "Jumlah Stunting", "KBTEKS": "Daerah"}
            )
            st.plotly_chart(fig, use_container_width=True)
           
            st.subheader("Persentase Stunting")
            vc = df["stunting"].value_counts().rename({0: "Tidak", 1: "Ya"})
            fig2 = px.pie(
                values=vc.values, 
                names=vc.index, 
                title="Persentase Stunting"
            )
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

    # Ambil fitur yang diharapkan model
    try:
        expected_features = list(model.feature_names_in_)
    except AttributeError:
        st.error("Model tidak menyimpan nama fitur. Pastikan model dilatih dengan pandas DataFrame.")
        st.stop()

    # Form input dinamis sesuai kolom model
    user_input_dict = {}
    for feature in expected_features:
        if feature.lower() in ["overweight", "underweight", "wasting", "stunting"]:
            user_input_dict[feature] = int(st.selectbox(feature, ["0", "1"]))
        else:
            user_input_dict[feature] = st.number_input(
                feature,
                value=0.0,
                format="%.2f"
            )

    if st.button("Prediksi"):
        # Pastikan semua kolom ada dan urutannya sama
        for col in expected_features:
            if col not in user_input_dict:
                user_input_dict[col] = 0
        X = pd.DataFrame([[user_input_dict[col] for col in expected_features]], columns=expected_features)

        pred = model.predict(X)[0]
        proba = model.predict_proba(X)[0][1] if hasattr(model, "predict_proba") else None
        label = "Stunting" if pred == 1 else "Tidak Stunting"

        if proba is not None:
            st.success(f"**{label}** (Confidence: {proba:.2%})")
        else:
            st.success(f"**{label}**")

        with st.expander("Lihat input yang digunakan"):
            st.write(X)

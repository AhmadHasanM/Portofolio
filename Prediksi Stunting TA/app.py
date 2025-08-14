import os
import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

# --- optional: download model dari Google Drive ---
# FILE_ID dari link kamu: https://drive.google.com/file/d/13penaMLTZC1wDvJ_H0twhyVSwZA79_Bq/view
MODEL_FILE_ID = "13penaMLTZC1wDvJ_H0twhyVSwZA79_Bq"
MODEL_LOCAL_NAME = "stunting_model.pkl"

@st.cache_resource(show_spinner=False)
def load_model():
    # jika model belum ada secara lokal, download via gdown
    if not os.path.exists(MODEL_LOCAL_NAME):
        try:
            import gdown
        except Exception:
            # install ringan saat runtime (hanya jika benar-benar perlu)
            import subprocess, sys
            subprocess.check_call([sys.executable, "-m", "pip", "install", "gdown"])
            import gdown

        url = f"https://drive.google.com/uc?id={MODEL_FILE_ID}"
        st.info("Mengunduh model dari Google Drive… (sekali saja)")
        gdown.download(url, MODEL_LOCAL_NAME, quiet=False)

    # load model
    model = joblib.load(MODEL_LOCAL_NAME)
    return model

@st.cache_data(show_spinner=False)
def load_data(csv_path="stunting_data.csv"):
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()

# ================================
# UI
# ================================
st.set_page_config(page_title="Prediksi Stunting", page_icon="🍼", layout="wide")
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Pilih Menu:", ["📊 Dashboard", "🧠 Predict"])

# coba load dataset (opsional)
df = load_data()

# coba load model (hanya saat butuh prediksi, tapi kita trigger awal agar error cepat terdeteksi)
try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    model_error = str(e)

# ================================
# 📊 DASHBOARD
# ================================
if menu == "📊 Dashboard":
    st.title("📊 Dashboard Analisis Stunting")

    if df.empty:
        st.warning("Dataset `stunting_data.csv` tidak ditemukan di repo. "
                   "Letakkan file itu di folder yang sama dengan `app.py` untuk melihat grafik.")
    else:
        with st.expander("📂 Lihat Data (sample)"):
            st.dataframe(df.head(200))

        # --- Jumlah kasus stunting per daerah ---
        if {"Daerah", "Stunting"}.issubset(df.columns):
            st.subheader("📍 Jumlah Kasus Stunting per Daerah")
            agg = df.groupby("Daerah")["Stunting"].sum().reset_index()
            fig1 = px.bar(agg, x="Daerah", y="Stunting", title="Jumlah Kasus Stunting per Daerah")
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Kolom 'Daerah' dan/atau 'Stunting' tidak ada di dataset.")

        # --- Persentase penderita vs tidak ---
        if "Stunting" in df.columns:
            st.subheader("📈 Persentase Penderita vs Tidak")
            counts = df["Stunting"].value_counts().rename({0: "Tidak", 1: "Ya"})
            fig2 = px.pie(values=counts.values, names=counts.index, title="Persentase Stunting")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Kolom 'Stunting' tidak ada di dataset.")

# ================================
# 🧠 PREDICT
# ================================
else:
    st.title("🧠 Prediksi Stunting")

    if not model_loaded:
        st.error("Model belum bisa dimuat.\n\nDetail: " + model_error)
        st.stop()

    # Coba tebak feature yang dibutuhkan model
    expected_cols = None
    if hasattr(model, "feature_names_in_"):
        # untuk model scikit-learn yang menyimpan nama kolom
        expected_cols = list(model.feature_names_in_)

    st.caption("Isi form berikut. (Jika nama fitur model berbeda, aplikasi akan menyesuaikan otomatis.)")

    # Default schema (silakan sesuaikan dengan data latihmu)
    default_schema = ["Umur Ibu", "Tinggi Ibu", "Pendidikan Ibu", "Berat Bayi", "ASI Eksklusif"]

    used_cols = expected_cols if expected_cols else default_schema

    # Input builder dinamis sederhana
    inputs = {}
    colA, colB = st.columns(2)
    for i, colname in enumerate(used_cols):
        with (colA if i % 2 == 0 else colB):
            lower = colname.lower()
            if "asi" in lower:
                val = st.selectbox(colname, ["Tidak", "Ya"])
                inputs[colname] = 1 if val == "Ya" else 0
            elif "pendidikan" in lower:
                val = st.selectbox(colname, ["SD", "SMP", "SMA", "Perguruan Tinggi"])
                mapping = {"SD": 0, "SMP": 1, "SMA": 2, "Perguruan Tinggi": 3}
                inputs[colname] = mapping[val]
            else:
                # angka
                inputs[colname] = st.number_input(colname, value=0.0, step=1.0)

    if st.button("🔍 Prediksi"):
        try:
            X = pd.DataFrame([inputs], columns=used_cols)
            pred = model.predict(X)[0]
            proba = None
            if hasattr(model, "predict_proba"):
                try:
                    proba = float(model.predict_proba(X)[0][1])
                except Exception:
                    proba = None

            if int(pred) == 1:
                if proba is not None:
                    st.error(f"⚠️ Berisiko Stunting (Confidence: {proba:.2%})")
                else:
                    st.error("⚠️ Berisiko Stunting")
            else:
                if proba is not None:
                    st.success(f"✅ Tidak Berisiko Stunting (Confidence: {proba:.2%})")
                else:
                    st.success("✅ Tidak Berisiko Stunting")
        except Exception as e:
            st.exception(e)
            st.warning("Pastikan urutan/nama fitur sesuai dengan yang dipakai saat training.")

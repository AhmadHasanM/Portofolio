import streamlit as st
import pandas as pd
import joblib
import os
import requests

# ==== URL MODEL DARI GOOGLE DRIVE ====
MODEL_URL = "https://drive.google.com/uc?id=13penaMLTZC1wDvJ_H0twhyVSwZA79_Bq"  # ganti FILE_ID dengan ID model kamu
MODEL_PATH = "stunting_model.pkl"

# Download model jika belum ada
if not os.path.exists(MODEL_PATH):
    with st.spinner("📥 Mengunduh model dari Google Drive..."):
        r = requests.get(MODEL_URL)
        with open(MODEL_PATH, "wb") as f:
            f.write(r.content)
        st.success("✅ Model berhasil diunduh.")

# Load model
model = joblib.load(MODEL_PATH)

# ==== LOAD DATASET ====
DATA_PATH = "stunting_data.csv"
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    df = pd.DataFrame()

# ==== SIDEBAR MENU ====
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Pilih Menu:", ["📊 Dashboard", "🧠 Predict"])

# ==== DASHBOARD ====
if menu == "📊 Dashboard":
    st.title("📊 Dashboard Analisis Stunting")
    if df.empty:
        st.error("❌ Dataset tidak ditemukan.")
    else:
        st.dataframe(df)

# ==== PREDICT ====
elif menu == "🧠 Predict":
    st.title("🧠 Prediksi Stunting")
    umur_ibu = st.number_input("Umur Ibu", min_value=15, max_value=50, value=25)
    tinggi_ibu = st.number_input("Tinggi Ibu (cm)", min_value=120, max_value=200, value=155)
    pendidikan_map = {"SD": 0, "SMP": 1, "SMA": 2, "Perguruan Tinggi": 3}
    pendidikan_ibu = st.selectbox("Pendidikan Ibu", list(pendidikan_map.keys()))
    berat_bayi = st.number_input("Berat Bayi Lahir (kg)", min_value=1.0, max_value=6.0, value=3.0)
    asi_map = {"Tidak": 0, "Ya": 1}
    asi_eksklusif = st.selectbox("ASI Eksklusif", list(asi_map.keys()))

    if st.button("🔍 Prediksi"):
        input_data = pd.DataFrame([[
            umur_ibu,
            tinggi_ibu,
            pendidikan_map[pendidikan_ibu],
            berat_bayi,
            asi_map[asi_eksklusif]
        ]], columns=["Umur Ibu", "Tinggi Ibu", "Pendidikan Ibu", "Berat Bayi", "ASI Eksklusif"])

        pred = model.predict(input_data)[0]
        proba = model.predict_proba(input_data)[0][1]

        if pred == 1:
            st.error(f"⚠️ Berisiko Stunting (Confidence: {proba:.2%})")
        else:
            st.success(f"✅ Tidak Berisiko Stunting (Confidence: {proba:.2%})")

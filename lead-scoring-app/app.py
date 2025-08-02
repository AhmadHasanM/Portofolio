import streamlit as st
import pandas as pd
import joblib
import os

# Load model dengan path yang lebih aman
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "lead_scoring_model.pkl")
model = joblib.load(model_path)

# Judul
st.title("🧠 Lead Scoring Prediction")
st.markdown("Masukkan informasi perusahaan untuk mengetahui apakah lead ini bernilai tinggi atau tidak.")

# Input fitur
industry = st.number_input("Industri (kode numerik)", min_value=0)
revenue = st.number_input("Revenue (USD millions)", min_value=0)
revenue_growth = st.number_input("Revenue Growth (%)", format="%.2f")
employees = st.number_input("Jumlah Karyawan", min_value=0)
state = st.number_input("Lokasi (State - kode numerik)", min_value=0)

# Prediksi saat tombol ditekan
if st.button("Prediksi Lead"):
    data_input = pd.DataFrame([[industry, revenue, revenue_growth, employees, state]],
                              columns=['Industri', 'Revenue (USD millions)', 'Revenue growth', 'Employees', 'State'])

    pred = model.predict(data_input)[0]
    proba = model.predict_proba(data_input)[0][1]

    if pred == 1:
        st.success(f"✅ Lead ini bernilai tinggi (Confidence: {proba:.2%})")
    else:
        st.warning(f"⚠️ Lead ini bernilai rendah (Confidence: {proba:.2%})")

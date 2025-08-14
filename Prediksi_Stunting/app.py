import streamlit as st
import pandas as pd
import pickle

# ======================
# Load model & kolom training
# ======================
with open("stunting_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

# ======================
# Mapping input → kolom dataset
# ======================
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

# ======================
# Streamlit UI
# ======================
st.title("Prediksi Stunting")

input_data = {}
for label in column_mapping.keys():
    if label in ['Jenis Kelamin', 'Kondisi Kesehatan Balita', 'Kondisi saat diukur', 'Pendidikan Ibu', 'Pekerjaan Ibu', 'Status Kawin Ibu', 'Status kehamilan Ibu Saat Ini', 'Kepemilikan Jaminan Kesehatan Ibu', 'Pendidikan Kepala Keluarga', 'Pekerjaan Kepala Keluarga']:
        input_data[label] = st.selectbox(label, ["Pilihan 1", "Pilihan 2"])  # ganti sesuai kategori asli
    else:
        input_data[label] = st.number_input(label, value=0.0)

if st.button("Prediksi"):
    # Buat DataFrame dari input
    X = pd.DataFrame([input_data])

    # Rename kolom sesuai dataset training
    X = X.rename(columns=column_mapping)

    # Pastikan urutan & nama kolom sama persis seperti model training
    X = X[model_columns]

    # Prediksi
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1] if hasattr(model, "predict_proba") else None

    # Output hasil
    st.subheader("Hasil Prediksi")
    st.write("Stunting" if pred == 1 else "Tidak Stunting")
    if proba is not None:
        st.write(f"Probabilitas: {proba:.2%}")

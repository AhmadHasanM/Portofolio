import streamlit as st
import pandas as pd
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# ================================
# --- LOAD MODEL & DATA ---
# ================================
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "stunting_model.pkl")
data_path = os.path.join(current_dir, "stunting_data.csv")

# Load model
model = joblib.load(model_path)

# Load dataset
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame()

# ================================
# --- SIDEBAR MENU ---
# ================================
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio("Pilih Menu:", ["📊 Dashboard", "🧠 Predict"])

# ================================
# 📊 DASHBOARD
# ================================
if menu == "📊 Dashboard":
    st.title("📊 Dashboard Analisis Stunting")
    
    if df.empty:
        st.error("❌ Dataset tidak ditemukan.")
    else:
        # Tampilkan data mentah
        with st.expander("📂 Lihat Data"):
            st.dataframe(df)

        # --- Visualisasi Jumlah Stunting per Daerah ---
        st.subheader("📍 Jumlah Stunting per Daerah")
        fig1 = px.bar(df.groupby("Daerah")["Stunting"].sum().reset_index(),
                      x="Daerah", y="Stunting",
                      title="Jumlah Kasus Stunting per Daerah",
                      color="Stunting", color_continuous_scale="Reds")
        st.plotly_chart(fig1, use_container_width=True)

        # --- Persentase Penderita vs Tidak ---
        st.subheader("📈 Persentase Penderita vs Tidak")
        if "Stunting" in df.columns:
            stunting_counts = df["Stunting"].value_counts()
            fig2 = px.pie(values=stunting_counts.values,
                          names=["Tidak" if i == 0 else "Ya" for i in stunting_counts.index],
                          title="Persentase Stunting")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Kolom 'Stunting' tidak ditemukan di dataset.")

# ================================
# 🧠 PREDICT
# ================================
elif menu == "🧠 Predict":
    st.title("🧠 Prediksi Stunting")
    st.markdown("Isi data di bawah untuk memprediksi kemungkinan stunting.")

    # Sesuaikan input ini dengan fitur yang digunakan model
    col1, col2 = st.columns(2)

    with col1:
        umur_ibu = st.number_input("Umur Ibu (tahun)", min_value=15, max_value=50, value=25)
        tinggi_ibu = st.number_input("Tinggi Ibu (cm)", min_value=120, max_value=200, value=155)
        pendidikan_ibu = st.selectbox("Pendidikan Ibu", ["SD", "SMP", "SMA", "Perguruan Tinggi"])

    with col2:
        berat_bayi = st.number_input("Berat Bayi Lahir (kg)", min_value=1.0, max_value=6.0, value=3.0)
        asi_eksklusif = st.selectbox("ASI Eksklusif", ["Ya", "Tidak"])
        daerah = st.text_input("Daerah")

    # Mapping categorical ke numerik (contoh)
    pendidikan_map = {"SD": 0, "SMP": 1, "SMA": 2, "Perguruan Tinggi": 3}
    asi_map = {"Tidak": 0, "Ya": 1}

    if st.button("🔍 Prediksi"):
        try:
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
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

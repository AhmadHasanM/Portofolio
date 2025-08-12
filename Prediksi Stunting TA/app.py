import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Load model dan dataset
model = joblib.load("stunting_model.pkl")
df = pd.read_csv("stunting_data.csv")

# Sidebar menu
menu = st.sidebar.radio("Menu", ["Dashboard", "Predict"])

# ===============================
# Dashboard
# ===============================
if menu == "Dashboard":
    st.title("📊 Dashboard Analisis Stunting")

    # 1. Jumlah stunting per daerah
    st.subheader("Jumlah Stunting per Daerah")
    daerah_count = df.groupby("daerah")["stunting"].sum().reset_index()
    fig1 = px.bar(daerah_count, x="daerah", y="stunting", title="Jumlah Penderita Stunting per Daerah")
    st.plotly_chart(fig1)

    # 2. Presentase penderita stunting
    st.subheader("Persentase Penderita vs Tidak Penderita")
    pie_data = df["stunting"].value_counts().reset_index()
    pie_data.columns = ["status", "jumlah"]
    pie_data["status"] = pie_data["status"].map({1: "Stunting", 0: "Tidak"})
    fig2 = px.pie(pie_data, names="status", values="jumlah", title="Persentase Stunting")
    st.plotly_chart(fig2)

    # 3. Distribusi umur penderita stunting
    st.subheader("Distribusi Umur Penderita Stunting")
    fig3 = px.histogram(df[df["stunting"] == 1], x="umur", nbins=20, title="Distribusi Umur Penderita Stunting")
    st.plotly_chart(fig3)

# ===============================
# Predict
# ===============================
elif menu == "Predict":
    st.title("🔮 Prediksi Stunting")

    col1, col2 = st.columns(2)
    with col1:
        umur = st.number_input("Umur (bulan)", min_value=0, max_value=60)
        berat = st.number_input("Berat badan (kg)", min_value=0.0)
    with col2:
        tinggi = st.number_input("Tinggi badan (cm)", min_value=0.0)
        jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    # Encode jenis kelamin
    jk_encoded = 1 if jenis_kelamin == "Laki-laki" else 0

    if st.button("Prediksi"):
        input_data = pd.DataFrame([[umur, berat, tinggi, jk_encoded]],
                                  columns=["umur", "berat", "tinggi", "jenis_kelamin"])
        pred = model.predict(input_data)[0]

        if pred == 1:
            st.error("⚠️ Anak berisiko stunting")
        else:
            st.success("✅ Anak tidak berisiko stunting")

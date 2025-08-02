import streamlit as st
import pandas as pd
import joblib
import os

# --- PATH MODEL ---
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "lead_scoring_model.pkl")
model = joblib.load(model_path)

# --- LOAD DATA PERUSAHAAN ---
data_path = os.path.join(current_dir, "cleaned_leads_dataset.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
else:
    df = pd.DataFrame()  # jika file tidak ada, biarkan kosong

# --- SIDEBAR MENU ---
st.sidebar.title("📊 Menu Dashboard")
menu = st.sidebar.radio("Pilih Menu:", ["📁 Data Perusahaan", "🎯 Lead Scoring", "✉️ Generated AI Email"])

# ---------------------------
# 1️⃣ MENU DATA PERUSAHAAN
# ---------------------------
if menu == "📁 Data Perusahaan":
    st.title("🏢 Data Perusahaan")
    st.markdown("Menampilkan data perusahaan dari dataset.")
    
    if df.empty:
        st.error("❌ Dataset tidak ditemukan atau kosong.")
    else:
        st.dataframe(df)  # tampilkan tabel data perusahaan
        # Bisa juga tambahkan filter
        industri_list = df['Industri'].unique()
        filter_industri = st.selectbox("Filter Industri:", ["Semua"] + list(industri_list))

        if filter_industri != "Semua":
            filtered_df = df[df['Industri'] == filter_industri]
            st.dataframe(filtered_df)
        else:
            st.dataframe(df)

# ---------------------------
# 2️⃣ MENU LEAD SCORING
# ---------------------------
elif menu == "🎯 Lead Scoring":
    st.title("🧠 Lead Scoring Prediction")
    st.markdown("Masukkan informasi perusahaan untuk mengetahui apakah lead ini bernilai tinggi atau tidak.")

    # Input fitur
    industry = st.number_input("Industri (kode numerik)", min_value=0)
    revenue = st.number_input("Revenue (USD millions)", min_value=0)
    revenue_growth = st.number_input("Revenue Growth (%)", format="%.2f")
    employees = st.number_input("Jumlah Karyawan", min_value=0)
    state = st.number_input("Lokasi (State - kode numerik)", min_value=0)

    if st.button("Prediksi Lead"):
        # buat dataframe input
        data_input = pd.DataFrame([[industry, revenue, revenue_growth, employees, state]],
                                  columns=['Industri', 'Revenue (USD millions)', 'Revenue growth', 'Employees', 'State'])

        # Prediksi
        pred = model.predict(data_input)[0]
        proba = model.predict_proba(data_input)[0][1]

        if pred == 1:
            st.success(f"✅ Lead ini bernilai tinggi (Confidence: {proba:.2%})")
        else:
            st.warning(f"⚠️ Lead ini bernilai rendah (Confidence: {proba:.2%})")

# ---------------------------
# 3️⃣ MENU GENERATED AI EMAIL
# ---------------------------
elif menu == "✉️ Generated AI Email":
    st.title("📧 Generated AI Email")
    st.markdown("Masukkan informasi untuk membuat email penawaran otomatis.")

    nama_client = st.text_input("Nama Client")
    nama_perusahaan = st.text_input("Nama Perusahaan")
    produk = st.text_input("Produk yang Ditawarkan")
    promo = st.text_input("Promo / Diskon (opsional)", "")

    if st.button("Generate Email"):
        email_template = f"""
        Halo {nama_client},

        Kami dari {nama_perusahaan} ingin menawarkan produk **{produk}** yang dapat membantu bisnis Anda berkembang lebih pesat.
        {"Kami juga memberikan promo spesial: " + promo if promo else ""}

        Jika Anda tertarik, kami dengan senang hati akan mengatur pertemuan lebih lanjut.

        Salam hangat,  
        Tim Marketing {nama_perusahaan}
        """
        st.markdown(email_template)

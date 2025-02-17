import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengumpulkan data dari file CSV lokal
all_data = pd.read_csv('Data/all_merge_data.csv')

# Menampilkan judul aplikasi
st.title('Proyek Analisis Data')

# Menampilkan dataset
st.subheader('Proyek Analisis Data')
st.write(all_data)

category_performance = all_data.groupby('product_category_name_english').agg({
    'order_item_id': 'sum',    # Jumlah produk terjual
    'price': 'mean'             # Rata-rata harga
}).reset_index()

category_performance = category_performance.sort_values(by='order_item_id', ascending=False)

# Visualisasi total penjualan per kategori produk
plt.figure(figsize=(12, 6))
bars = sns.barplot(x='order_item_id', y='product_category_name_english', data=category_performance[:20], hue='product_category_name_english', palette='viridis')
plt.title('Total Penjualan per Kategori Produk (Top 20)')
plt.xlabel('Total Penjualan')
plt.ylabel('Kategori Produk')

# Menambahkan data di dalam setiap bar
for bar in bars.patches:
    # plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width()):,}', ha='left', va='center', color='black', fontsize=10)
    plt.text(bar.get_width() / 2, bar.get_y() + bar.get_height() / 2, f'{int(bar.get_width()):,}', ha='center', va='center', color='white')

plt.show()

#pembelian per negara bagian
purchase_by_state = all_data.groupby('customer_state')['order_id'].count().reset_index().sort_values(by='order_id', ascending=False)
# Analisis Pembelian Berdasarkan Lokasi
plt.figure(figsize=(12, 6))
bars = sns.barplot(x='customer_state', y='order_id', data=purchase_by_state, hue='customer_state', palette='viridis', dodge=False)
plt.title('Jumlah Pembelian per Negara Bagian')
plt.xlabel('Negara Bagian')
plt.ylabel('Jumlah Pembelian')
plt.xticks(rotation=45)

# Menampilkan nilai pada setiap bar
for bar in bars.patches:
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{int(bar.get_height())}', ha='center', va='bottom')

plt.show()
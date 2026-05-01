import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

# Configuration
st.set_page_config(
    page_title="Dashboard E-Commerce Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)


PALETTE = ["#2563eb", "#16a34a", "#ea580c", "#9333ea", "#0891b2", "#dc2626", "#ca8a04"]
 
def styled_fig(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f8fafc")
    ax.tick_params(colors="#374151", labelsize=9)
    ax.xaxis.label.set_color("#374151")
    ax.yaxis.label.set_color("#374151")
    ax.title.set_color("#111827")
    for spine in ax.spines.values():
        spine.set_edgecolor("#e5e7eb")
    return fig, ax

# style css
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
 
/* Background */
.stApp {
    background: #f8fafc;
    color: #1e293b;
}
 
/* Sidebar */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0;
    box-shadow: 2px 0 8px rgba(0,0,0,0.04);
}
[data-testid="stSidebar"] * {
    color: #334155 !important;
}
 
/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.metric-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 8px;
}
.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
    font-family: 'JetBrains Mono', monospace;
}
.metric-delta {
    font-size: 12px;
    color: #16a34a;
    margin-top: 4px;
}
 
/* Section headers */
.section-header {
    font-size: 20px;
    font-weight: 700;
    color: #0f172a;
    margin: 8px 0 4px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #e2e8f0;
}
.section-sub {
    font-size: 13px;
    color: #64748b;
    margin-bottom: 18px;
}
 
/* Insight box */
.insight-box {
    background: #f0fdf4;
    border-left: 4px solid #16a34a;
    border-radius: 0 10px 10px 0;
    padding: 14px 18px;
    margin-top: 12px;
    font-size: 13.5px;
    color: #166534;
    line-height: 1.7;
}
 
/* Chart container */
.chart-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px;
}
 
/* Tab styles */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-radius: 45px;
    padding: cd 
    gap: 100px;
    border: 1px solid #e2e8f0;
            
}
.stTabs [data-baseweb="tab"] {
    border-radius: 45px;
    color: #64748b;
    font-weight: 700;
    font-size: 10px;
}
.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    width: 150px;
    color: #ffffff !important;
}
 
/* Divider */
hr {
    border-color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)
 

# ======================================================================= 

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df
 
try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("⚠️ File `main_data.csv` tidak ditemukan. Pastikan file ada di folder yang sama dengan `dashboard.py`.")
    st.stop()
 
# Sidebar filters
with st.sidebar:
    st.markdown("## 🛒 E-Commerce\n**Analytics Dashboard**")
    st.markdown("---")
 
    st.markdown("### 📅 Filter Periode")
    year_options = sorted(df_raw['order_purchase_timestamp'].dt.year.unique().tolist())
    selected_years = st.multiselect("Tahun", year_options, default=year_options)
 
    st.markdown("### 🏙️ Filter Kota (Top N)")
    top_n = st.slider("Tampilkan Top N Kota/Kategori", 5, 20, 10)
 
    st.markdown("---")
    st.markdown("""
    <div style='font-size:12px; color:#64748b; line-height:1.8'>
    📊 <b>Dataset:</b> Brazilian E-Commerce<br>
    📆 <b>Periode:</b> Jan 2017 – Agt 2018<br>
    👩‍💻 <b>Dibuat oleh:</b><br>Auliya Az Zahrah Salsabilah<br>
    <span style='color:#2563eb'>Dicoding 2026 [CDC-31]</span>
    </div>
    """, unsafe_allow_html=True)
 
# filtering data
if selected_years:
    df = df_raw[df_raw['order_purchase_timestamp'].dt.year.isin(selected_years)].copy()
else:
    df = df_raw.copy()
 
# header
st.markdown("""
<div style='padding: 24px 0 8px 0'>
    <h1 style='font-size:32px; font-weight:800; color:#0f172a; margin:0'>
        📦 E-Commerce Analytics Dashboard
    </h1>
    <p style='color:#64748b; font-size:14px; margin-top:6px'>
        Analisis performa penjualan · Januari 2017 – Agustus 2018 · Brazilian E-Commerce Public Dataset
    </p>
</div>
""", unsafe_allow_html=True)
 
# KPI Metrics
total_orders = df['order_id'].nunique()
total_revenue = df['payment_value'].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
total_customers = df['customer_id'].nunique() if 'customer_id' in df.columns else 0
 
col1, col2, col3, col4 = st.columns(4)
for col, label, value, delta in [
    (col1, "Total Order",      f"{total_orders:,}",          "📦 Delivered"),
    (col2, "Total Revenue",    f"R$ {total_revenue/1e6:.2f}M", "💰 BRL"),
    (col3, "Total Pelanggan",  f"{total_customers:,}",        "👤 Unik"),
    (col4, "Avg Order Value",  f"R$ {avg_order_value:,.0f}",   "🧾 per transaksi"),
]:
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)
 
st.markdown("<br>", unsafe_allow_html=True)
 
# tab navigasi 
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tren Penjualan",
    "🏙️ Kota & Geografis",
    "📦 Kategori Produk",
    "💳 Metode Pembayaran",
    "👥 RFM & Segmentasi"
])
 
# tren penjualan 
with tab1:
    st.markdown('<div class="section-header">Tren Jumlah Order & Revenue per Bulan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Bagaimana tren penjualan dan revenue berkembang sepanjang periode 2017–2018?</div>', unsafe_allow_html=True)
 
    monthly_df = df.resample(rule='ME', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "total_price": "sum"
    }).reset_index()
    monthly_df.columns = ['bulan', 'order_count', 'revenue']
 
    col1, col2 = st.columns(2)
 
    with col1:
        fig, ax = styled_fig((8, 4))
        ax.plot(monthly_df['bulan'], monthly_df['order_count'],
                color=PALETTE[0], linewidth=2.5, marker='o', markersize=4,
                markerfacecolor='white', markeredgewidth=2, markeredgecolor=PALETTE[0])
        ax.fill_between(monthly_df['bulan'], monthly_df['order_count'], alpha=0.15, color=PALETTE[0])
 
        if not monthly_df.empty:
            max_idx = monthly_df['order_count'].idxmax()
            ax.annotate(
                f"Puncak\n{int(monthly_df.loc[max_idx,'order_count']):,} orders",
                xy=(monthly_df.loc[max_idx,'bulan'], monthly_df.loc[max_idx,'order_count']),
                xytext=(15, -40), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color=PALETTE[2], lw=1.5),
                fontsize=9, color=PALETTE[2], fontweight='bold'
            )
 
        ax.set_title("Jumlah Order per Bulan", fontsize=13, fontweight='bold', pad=10)
        ax.set_xlabel("Bulan", fontsize=10)
        ax.set_ylabel("Jumlah Order", fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.grid(True, color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    with col2:
        fig, ax = styled_fig((8, 4))
        ax.plot(monthly_df['bulan'], monthly_df['revenue'],
                color=PALETTE[1], linewidth=2.5, marker='s', markersize=4,
                markerfacecolor='white', markeredgewidth=2, markeredgecolor=PALETTE[1])
        ax.fill_between(monthly_df['bulan'], monthly_df['revenue'], alpha=0.15, color=PALETTE[1])
 
        if not monthly_df.empty:
            max_idx = monthly_df['revenue'].idxmax()
            ax.annotate(
                f"Puncak\nR$ {monthly_df.loc[max_idx,'revenue']/1e6:.1f}M",
                xy=(monthly_df.loc[max_idx,'bulan'], monthly_df.loc[max_idx,'revenue']),
                xytext=(15, -45), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', color=PALETTE[2], lw=1.5),
                fontsize=9, color=PALETTE[2], fontweight='bold'
            )
 
        ax.set_title("Total Revenue per Bulan", fontsize=13, fontweight='bold', pad=10)
        ax.set_xlabel("Bulan", fontsize=10)
        ax.set_ylabel("Revenue (BRL)", fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x/1e6:.1f}M'))
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.grid(True, color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    st.markdown("""
    <div class="insight-box">
    📌 <b>Insight:</b> Tren jumlah order dan revenue menunjukkan pertumbuhan yang konsisten dari awal 2017 hingga akhir tahun, 
    dengan puncak tertinggi terjadi pada <b>November–Desember 2017</b> yang mengindikasikan adanya pengaruh 
    faktor musiman (kampanye akhir tahun). Revenue kemudian cenderung stabil pada semester pertama 2018.
    </div>
    """, unsafe_allow_html=True)
 
# Kota dan geografis
with tab2:
    st.markdown('<div class="section-header">Analisis Geografis — Distribusi Transaksi & Revenue per Kota</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Kota mana yang memiliki jumlah transaksi dan revenue tertinggi selama 2017–2018?</div>', unsafe_allow_html=True)
 
    city_df = df.groupby("customer_city").agg(
        total_orders=("order_id", "nunique"),
        revenue=("total_price", "sum")
    ).reset_index()
 
    top_city_orders = city_df.sort_values("total_orders", ascending=False).head(top_n)
    top_city_rev    = city_df.sort_values("revenue", ascending=False).head(top_n)
 
    col1, col2 = st.columns(2)
 
    with col1:
        fig, ax = styled_fig((7, top_n * 0.42 + 1))
        colors_c = [PALETTE[0] if i == 0 else '#bfdbfe' for i in range(len(top_city_orders))]
        bars = ax.barh(top_city_orders['customer_city'][::-1],
                       top_city_orders['total_orders'][::-1],
                       color=colors_c[::-1], edgecolor='none', height=0.7)
        for bar, val in zip(bars, top_city_orders['total_orders'][::-1]):
            ax.text(bar.get_width() + max(top_city_orders['total_orders']) * 0.01,
                    bar.get_y() + bar.get_height()/2,
                    f'{int(val):,}', va='center', fontsize=8, color='#374151')
        ax.set_title(f"Top {top_n} Kota — Jumlah Transaksi", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Jumlah Order", fontsize=9)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax.grid(axis='x', color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    with col2:
        fig, ax = styled_fig((7, top_n * 0.42 + 1))
        colors_c2 = [PALETTE[1] if i == 0 else '#bbf7d0' for i in range(len(top_city_rev))]
        bars = ax.barh(top_city_rev['customer_city'][::-1],
                       top_city_rev['revenue'][::-1],
                       color=colors_c2[::-1], edgecolor='none', height=0.7)
        for bar, val in zip(bars, top_city_rev['revenue'][::-1]):
            ax.text(bar.get_width() + max(top_city_rev['revenue']) * 0.01,
                    bar.get_y() + bar.get_height()/2,
                    f'R$ {val/1e6:.1f}M', va='center', fontsize=8, color='#374151')
        ax.set_title(f"Top {top_n} Kota — Total Revenue", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Revenue (BRL)", fontsize=9)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x/1e6:.0f}M'))
        ax.grid(axis='x', color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    # State-level analysis
    st.markdown("---")
    st.markdown("#### Distribusi Revenue per State (Level Provinsi)")
 
    if 'customer_state' in df.columns:
        state_df = df.groupby("customer_state").agg(
            total_revenue=("total_price", "sum"),
            total_orders=("order_id", "nunique")
        ).reset_index().sort_values("total_revenue", ascending=False)
 
        fig, ax = styled_fig((12, 4))
        colors_s = [PALETTE[0] if i < 3 else '#bfdbfe' for i in range(len(state_df))]
        ax.bar(state_df['customer_state'], state_df['total_revenue'],
               color=colors_s, edgecolor='none')
        ax.set_title("Total Revenue per State (2017–2018)", fontsize=13, fontweight='bold', pad=10)
        ax.set_xlabel("State", fontsize=10)
        ax.set_ylabel("Revenue (BRL)", fontsize=10)
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x/1e6:.0f}M'))
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.grid(axis='y', color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    st.markdown("""
    <div class="insight-box">
    📌 <b>Insight:</b> <b>São Paulo</b> mendominasi secara signifikan — baik dari jumlah transaksi maupun total revenue — 
    jauh melampaui kota-kota lain. Ini mencerminkan konsentrasi aktivitas e-commerce di pusat ekonomi utama Brazil. 
    Kota-kota di wilayah tenggara (SP, RJ, MG) menjadi prioritas utama untuk strategi pemasaran, 
    sementara kota-kota kecil menyimpan potensi ekspansi pasar yang besar.
    </div>
    """, unsafe_allow_html=True)
 
# Kategori produk
with tab3:
    st.markdown('<div class="section-header">Analisis Kategori Produk</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Kategori produk apa yang paling laris dan menghasilkan revenue terbesar?</div>', unsafe_allow_html=True)
 
    cat_df = df.groupby("product_category_name").agg(
        total_sold=("order_id", "count"),
        revenue=("total_price", "sum")
    ).reset_index()
 
    top_cat_sold = cat_df.sort_values("total_sold", ascending=False).head(top_n)
    top_cat_rev  = cat_df.sort_values("revenue", ascending=False).head(top_n)
 
    col1, col2 = st.columns(2)
 
    with col1:
        fig, ax = styled_fig((7, top_n * 0.42 + 1))
        cmap_sold = plt.cm.Blues(np.linspace(0.4, 0.9, len(top_cat_sold)))
        bars = ax.barh(top_cat_sold['product_category_name'][::-1],
                       top_cat_sold['total_sold'][::-1],
                       color=cmap_sold, edgecolor='none', height=0.7)
        for bar, val in zip(bars, top_cat_sold['total_sold'][::-1]):
            ax.text(bar.get_width() + max(top_cat_sold['total_sold']) * 0.01,
                    bar.get_y() + bar.get_height()/2,
                    f'{int(val):,}', va='center', fontsize=8, color='#374151')
        ax.set_title(f"Top {top_n} Kategori — Volume Penjualan", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Jumlah Item Terjual", fontsize=9)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
        ax.grid(axis='x', color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    with col2:
        fig, ax = styled_fig((7, top_n * 0.42 + 1))
        cmap_rev = plt.cm.Purples(np.linspace(0.4, 0.9, len(top_cat_rev)))
        bars = ax.barh(top_cat_rev['product_category_name'][::-1],
                       top_cat_rev['revenue'][::-1],
                       color=cmap_rev, edgecolor='none', height=0.7)
        for bar, val in zip(bars, top_cat_rev['revenue'][::-1]):
            ax.text(bar.get_width() + max(top_cat_rev['revenue']) * 0.01,
                    bar.get_y() + bar.get_height()/2,
                    f'R$ {val/1e6:.1f}M', va='center', fontsize=8, color='#374151')
        ax.set_title(f"Top {top_n} Kategori — Total Revenue", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel("Revenue (BRL)", fontsize=9)
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x/1e6:.1f}M'))
        ax.grid(axis='x', color='#e5e7eb', linestyle='--', linewidth=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
 
    st.markdown("""
    <div class="insight-box">
    📌 <b>Insight:</b> Kategori <b>bed_bath_table</b> dan <b>health_beauty</b> mendominasi volume penjualan, 
    mencerminkan tingginya permintaan terhadap produk kebutuhan rumah tangga dan perawatan diri. 
    Sementara itu dari sisi revenue, kategori-kategori dengan harga produk lebih tinggi (seperti elektronik) 
    bisa menghasilkan revenue signifikan meski volumenya lebih rendah. 
    Ini menjadi sinyal penting untuk strategi pengelolaan stok dan promosi.
    </div>
    """, unsafe_allow_html=True)
 
# Metode pembayaran
with tab4:
    st.markdown('<div class="section-header">Analisis Metode Pembayaran</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Metode pembayaran apa yang paling sering digunakan dan berkontribusi terbesar terhadap revenue?</div>', unsafe_allow_html=True)
 
    pay_col = 'payment_type' if 'payment_type' in df.columns else None
    val_col = 'payment_value' if 'payment_value' in df.columns else 'total_price'
 
    if pay_col:
        pay_df = df.groupby(pay_col).agg(
            total_orders=("order_id", "nunique"),
            revenue=(val_col, "sum")
        ).reset_index().sort_values("total_orders", ascending=False)
 
        col1, col2, col3 = st.columns([2, 2, 1.5])
 
        with col1:
            fig, ax = styled_fig((7, 4))
            colors_p = PALETTE[:len(pay_df)]
            bars = ax.bar(pay_df[pay_col], pay_df['total_orders'],
                          color=colors_p, edgecolor='none', width=0.6)
            for bar, val in zip(bars, pay_df['total_orders']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(pay_df['total_orders'])*0.01,
                        f'{int(val):,}', ha='center', fontsize=9, fontweight='bold', color='#374151')
            ax.set_title("Frekuensi Penggunaan", fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel("Metode Pembayaran", fontsize=9)
            ax.set_ylabel("Jumlah Transaksi", fontsize=9)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
            ax.grid(axis='y', color='#e5e7eb', linestyle='--', linewidth=0.7)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
 
        with col2:
            fig, ax = styled_fig((7, 4))
            pay_rev = pay_df.sort_values("revenue", ascending=False)
            bars = ax.bar(pay_rev[pay_col], pay_rev['revenue'],
                          color=colors_p[:len(pay_rev)], edgecolor='none', width=0.6)
            for bar, val in zip(bars, pay_rev['revenue']):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(pay_rev['revenue'])*0.01,
                        f'R$ {val/1e6:.1f}M', ha='center', fontsize=9, fontweight='bold', color='#374151')
            ax.set_title("Kontribusi Revenue", fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel("Metode Pembayaran", fontsize=9)
            ax.set_ylabel("Revenue (BRL)", fontsize=9)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x/1e6:.0f}M'))
            ax.grid(axis='y', color='#e5e7eb', linestyle='--', linewidth=0.7)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
 
        with col3:
            st.markdown("**Proporsi Transaksi**")
            fig, ax = plt.subplots(figsize=(3.5, 3.5))
            fig.patch.set_facecolor('#ffffff')
            wedges, texts, autotexts = ax.pie(
                pay_df['total_orders'],
                labels=pay_df[pay_col],
                colors=PALETTE[:len(pay_df)],
                autopct='%1.1f%%',
                startangle=90,
                wedgeprops=dict(edgecolor='#ffffff', linewidth=2),
                textprops=dict(color='#374151', fontsize=8)
            )
            for at in autotexts:
                at.set_fontsize(8)
                at.set_color('#0f172a')
                at.set_fontweight('bold')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
 
    st.markdown("""
    <div class="insight-box">
    📌 <b>Insight:</b> <b>Credit card</b> mendominasi lebih dari 73% transaksi dan menjadi kontributor terbesar 
    terhadap total revenue. <b>Boleto</b> (slip pembayaran tunai khas Brazil) menempati posisi kedua, 
    mencerminkan bahwa sebagian pelanggan masih memilih metode non-digital. 
    Voucher dan debit card memiliki pangsa sangat kecil — peluang untuk meningkatkan adopsinya melalui program insentif.
    </div>
    """, unsafe_allow_html=True)
 
# RFM dan segmentasi pelanggan
with tab5:
    st.markdown('<div class="section-header">RFM Analysis & Segmentasi Pelanggan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Segmentasi pelanggan berdasarkan Recency, Frequency, dan Monetary untuk memahami perilaku pembelian.</div>', unsafe_allow_html=True)
 
    if 'customer_id' in df.columns:
        # Hitung RFM
        rfm_df = df.groupby('customer_id').agg(
            last_order=('order_purchase_timestamp', 'max'),
            frequency=('order_id', 'nunique'),
            monetary=('total_price', 'sum')
        ).reset_index()
 
        latest_date = df['order_purchase_timestamp'].max()
        rfm_df['recency'] = (latest_date - rfm_df['last_order']).dt.days
 
        # Buat segmen
        rfm_df['segment'] = pd.qcut(rfm_df['monetary'], 3, labels=['Low', 'Medium', 'High'])
 
        # Ringkasan per segmen
        rfm_summary = rfm_df.groupby('segment', observed=True).agg(
            jumlah_pelanggan=('customer_id', 'count'),
            avg_recency=('recency', 'mean'),
            avg_frequency=('frequency', 'mean'),
            avg_monetary=('monetary', 'mean')
        ).round(1).reset_index()
 
        # Metric cards per segmen
        col1, col2, col3 = st.columns(3)
        seg_colors  = {'Low': '#ef4444', 'Medium': '#f59e0b', 'High': '#16a34a'}
        seg_emojis  = {'Low': '🔴', 'Medium': '🟡', 'High': '🟢'}
 
        for col, row in zip([col1, col2, col3], rfm_summary.itertuples()):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="border-color:{seg_colors[row.segment]}44">
                    <div class="metric-label">{seg_emojis[row.segment]} Segmen {row.segment}</div>
                    <div class="metric-value">{int(row.jumlah_pelanggan):,}</div>
                    <div style="font-size:12px; color:#64748b; margin-top:8px">
                        Avg Recency: <b style="color:#374151">{row.avg_recency:.0f} hari</b><br>
                        Avg Frequency: <b style="color:#374151">{row.avg_frequency:.1f}x</b><br>
                        Avg Monetary: <b style="color:#374151">R$ {row.avg_monetary:,.0f}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
 
        col1, col2 = st.columns(2)
 
        with col1:
            # Bar chart distribusi segmen
            fig, ax = styled_fig((7, 4))
            seg_counts = rfm_df['segment'].value_counts().reindex(['Low', 'Medium', 'High'])
            seg_clrs   = [seg_colors[s] for s in seg_counts.index]
            bars = ax.bar(seg_counts.index, seg_counts.values,
                          color=seg_clrs, edgecolor='none', width=0.5)
            for bar, val in zip(bars, seg_counts.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(seg_counts)*0.01,
                        f'{int(val):,}', ha='center', fontsize=10, fontweight='bold', color='#0f172a')
            ax.set_title("Distribusi Segmen Pelanggan (RFM)", fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel("Segmen", fontsize=10)
            ax.set_ylabel("Jumlah Pelanggan", fontsize=10)
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
            ax.grid(axis='y', color='#e5e7eb', linestyle='--', linewidth=0.7)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
 
        with col2:
            # Histogram monetary per segmen
            fig, ax = styled_fig((7, 4))
            for seg, clr in seg_colors.items():
                data = rfm_df[rfm_df['segment'] == seg]['monetary']
                ax.hist(data, bins=40, alpha=0.65, label=seg, color=clr, edgecolor='none')
            ax.set_title("Distribusi Nilai Transaksi per Segmen", fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel("Total Nilai Transaksi (BRL)", fontsize=10)
            ax.set_ylabel("Jumlah Pelanggan", fontsize=10)
            ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x:,.0f}'))
            ax.legend(title='Segmen', fontsize=9)
            ax.grid(axis='y', color='#e5e7eb', linestyle='--', linewidth=0.7)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
 
        col3, col4 = st.columns(2)
 
        with col3:
            # Histogram recency per segmen
            fig, ax = styled_fig((7, 4))
            for seg, clr in seg_colors.items():
                data = rfm_df[rfm_df['segment'] == seg]['recency']
                ax.hist(data, bins=40, alpha=0.65, label=seg, color=clr, edgecolor='none')
            ax.set_title("Distribusi Recency per Segmen", fontsize=12, fontweight='bold', pad=10)
            ax.set_xlabel("Hari sejak transaksi terakhir", fontsize=10)
            ax.set_ylabel("Jumlah Pelanggan", fontsize=10)
            ax.legend(title='Segmen', fontsize=9)
            ax.grid(axis='y', color='#e5e7eb', linestyle='--', linewidth=0.7)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
 
        with col4:
            # Tabel ringkasan RFM
            st.markdown("**Ringkasan Statistik RFM per Segmen**")
            rfm_display = rfm_summary.copy()
            rfm_display.columns = ['Segmen','Jml Pelanggan','Avg Recency (hari)','Avg Frequency','Avg Monetary (BRL)']
            rfm_display['Avg Monetary (BRL)'] = rfm_display['Avg Monetary (BRL)'].apply(lambda x: f'R$ {x:,.1f}')
            rfm_display['Jml Pelanggan'] = rfm_display['Jml Pelanggan'].apply(lambda x: f'{int(x):,}')
            st.dataframe(rfm_display, use_container_width=True, hide_index=True)
 
            # Clustering penjelasan
            st.markdown("""
            <div style='background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:14px; margin-top:12px; font-size:12.5px; line-height:1.8; color:#374151'>
            <b>🔴 Low:</b> Pelanggan baru atau jarang belanja, nilai transaksi kecil<br>
            <b>🟡 Medium:</b> Pelanggan potensial, perlu didorong agar lebih aktif<br>
            <b>🟢 High:</b> Pelanggan paling berharga — prioritas program loyalitas
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown("""
        <div class="insight-box">
        📌 <b>Insight:</b> Mayoritas pelanggan berada di segmen <b>Low</b>, mengindikasikan tingginya jumlah pembeli sekali atau jarang. 
        Segmen <b>High</b> adalah kelompok pelanggan paling berharga yang harus diprioritaskan untuk program loyalitas dan retensi. 
        Segmen <b>Medium</b> merupakan kelompok potensial yang bisa didorong naik ke segmen High melalui kampanye re-engagement 
        seperti email promosi atau program poin reward.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Kolom `customer_id` tidak ditemukan di `main_data.csv`. Pastikan data sudah di-merge dengan benar dari notebook.")
 
# footer
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#94a3b8; font-size:12px; padding: 8px 0'>
    © 2026 · Dashboard E-Commerce Analytics · 
    <b style='color:#2563eb'>Auliya Az Zahrah Salsabilah</b> · Dicoding [CDC-31]
</div>
""", unsafe_allow_html=True)
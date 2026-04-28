import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="GlowGuard: Advanced SkinChem Analyzer", page_icon="🧪", layout="centered")

# --- FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("skincare_rules.csv")
    
    # 1. Rapikan nama KOLOM (bahan_1 menjadi Bahan 1, ph_1 menjadi Ph 1, dst)
    df.columns = df.columns.str.replace('_', ' ').str.title()
    
    # 2. Rapikan ISI DATA-nya
    df = df.apply(lambda x: x.map(lambda y: str(y).replace('_', ' ').title() if isinstance(y, str) else y))
    
    return df

df = load_data()

# Mendapatkan daftar unik bahan (membersihkan data dari kedua kolom bahan)
semua_bahan = pd.concat([df['Bahan 1'], df['Bahan 2']]).unique()
# Mengecualikan 'All Active' agar tidak muncul di dropdown utama
semua_bahan = [bahan for bahan in semua_bahan if bahan.lower() != 'all active']
semua_bahan.sort()

# --- HEADER APLIKASI ---
st.title("🧪 GlowGuard")
st.markdown("**Advanced Skincare Interaction Matrix**")
st.write("Sistem pakar (Expert System) berbasis data untuk menganalisis risiko iritasi, benturan pH, dan efikasi kombinasi bahan kimia *skincare*.")

# --- UI INPUT ---
st.write("---")
col1, col2 = st.columns(2)

with col1:
    bahan_a = st.selectbox("🧪 Bahan Aktif 1:", semua_bahan, key="bahan_a")

with col2:
    bahan_b = st.selectbox("🧪 Bahan Aktif 2:", semua_bahan, key="bahan_b")

# --- LOGIC & HASIL ---
st.write("---")
if st.button("📊 Analisis Interaksi Kimia", use_container_width=True, type="primary"):
    if bahan_a == bahan_b:
        st.info("💡 Anda memilih bahan yang sama. Pastikan konsentrasi total tidak menyebabkan *over-exfoliation*.")
    else:
        # Mencari match dengan mempertimbangkan 2 arah (A-B atau B-A) dan aturan 'All Active' (seperti Sunscreen)
        match = df[
            ((df['Bahan 1'] == bahan_a) & ((df['Bahan 2'] == bahan_b) | (df['Bahan 2'] == 'All Active'))) | 
            ((df['Bahan 1'] == bahan_b) & ((df['Bahan 2'] == bahan_a) | (df['Bahan 2'] == 'All Active'))) |
            (((df['Bahan 1'] == 'All Active') | (df['Bahan 2'] == 'All Active')) & ((df['Bahan 1'] == bahan_a) | (df['Bahan 2'] == bahan_b) | (df['Bahan 1'] == bahan_b) | (df['Bahan 2'] == bahan_a)))
        ]
        
        if not match.empty:
            # Mengambil baris pertama dari hasil pencarian
            data = match.iloc[0]
            
            # --- VISUALISASI STATUS UTAMA ---
            status = data['Status'].upper()
            
            if status == "AMAN":
                st.success(f"✅ STATUS: {status}")
            elif status == "WAJIB":
                st.info(f"🛡️ STATUS: {status} (Highly Recommended)")
            elif status == "HATI-HATI":
                st.warning(f"⚠️ STATUS: {status}")
            elif status == "JANGAN":
                st.error(f"🚨 STATUS: {status} (High Risk!)")

            # --- ANALISIS MENDALAM (METRICS) ---
            st.markdown("### 🔬 Deep Chemical Analysis")
            
            col_met1, col_met2, col_met3 = st.columns(3)
            with col_met1:
                st.metric(label="Irritation Risk", value=data['Irritation Risk'].upper())
            with col_met2:
                st.metric(label="Interaction Type", value=data['Interaction Type'].replace(' ', '\n'))
            with col_met3:
                # Menampilkan bentrokan kategori
                st.metric(label="Category Mix", value=f"{data['Kategori 1']} + {data['Kategori 2']}")

            # --- PENJELASAN DETAIL ---
            with st.expander("📝 Baca Penjelasan Dermatologis", expanded=True):
                st.write(f"**Kesimpulan:** {data['Explanation']}")
                st.write("---")
                st.markdown("**Profil Bahan:**")
                st.write(f"- **{data['Bahan 1']}:** pH Level ({data['Ph 1']}) | Kekuatan ({data['Strength 1']})")
                st.write(f"- **{data['Bahan 2']}:** pH Level ({data['Ph 2']}) | Kekuatan ({data['Strength 2']})")
                
                # Tambahan logika peringatan pH
                if data['Ph 1'] != data['Ph 2'] and data['Ph 1'] != 'Neutral' and data['Ph 2'] != 'Neutral':
                    st.caption("⚠️ *Peringatan AI:* Terdapat perbedaan tingkat asam-basa (pH) yang signifikan. Kombinasi ini dapat mendestabilisasi salah satu bahan aktif.")

        else:
            st.warning("🤷‍♀️ Kombinasi ini belum dipetakan dalam database kami.")
            st.write("Saran: Selalu lakukan *patch test* di area rahang sebelum mencoba kombinasi baru.")

# --- FOOTER ---
st.write("---")
st.caption("Data Architecture by Aqeela | Methodology: Knowledge-Based Expert System")
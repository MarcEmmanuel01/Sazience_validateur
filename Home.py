import streamlit as st

# Configuration de la page principale
st.set_page_config(
    page_title="Validateur Excel - Accueil",
    page_icon="✅",
    layout="centered"
)

# --- HEADER ---
st.markdown("""
<div style='text-align:center; padding:40px 0 20px 0;'>
    <h1 style='color:#EC4400; margin-bottom:10px;'>🛠️ Validateur de Données Excel</h1>
    <p style='font-size:18px; color:#666;'>
        Validez vos fichiers Excel avec des références locales
    </p>
</div>
""", unsafe_allow_html=True)

# --- Description des étapes ---
st.markdown("""
<div style='display:flex; justify-content:space-between; gap:15px; margin:40px 0;'>
    <div style='flex:1; text-align:center; padding:25px 15px; border-radius:12px; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white;'>
        <div style='font-size:40px; margin-bottom:8px;'>📤</div>
        <div style='font-weight:600; font-size:16px;'>Upload</div>
        <div style='font-size:13px; opacity:0.9; margin-top:5px;'>Étape 1</div>
    </div>
    <div style='flex:1; text-align:center; padding:25px 15px; border-radius:12px; background:linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color:white;'>
        <div style='font-size:40px; margin-bottom:8px;'>🔍</div>
        <div style='font-weight:600; font-size:16px;'>Validation</div>
        <div style='font-size:13px; opacity:0.9; margin-top:5px;'>Étape 2</div>
    </div>
    <div style='flex:1; text-align:center; padding:25px 15px; border-radius:12px; background:linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color:white;'>
        <div style='font-size:40px; margin-bottom:8px;'>📊</div>
        <div style='font-weight:600; font-size:16px;'>Résultats</div>
        <div style='font-size:13px; opacity:0.9; margin-top:5px;'>Étape 3</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Bouton pour commencer ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Commencer la validation", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📤_Upload.py")

st.markdown("""
<div style='text-align:center; margin-top:30px; padding:15px; background:#f8f9fa; border-radius:8px; border-left:4px solid #EC4400;'>
    💡 <strong>Conseil :</strong> Importez votre fichier Excel, puis validez-le avec nos références prédéfinies
</div>
""", unsafe_allow_html=True)
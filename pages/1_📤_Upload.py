import streamlit as st
import pandas as pd

# Configuration
st.set_page_config(page_title="Étape 1 - Upload Excel", page_icon="📤", layout="centered")

# Header avec progression
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <div style='color:#999; font-size:14px; margin-bottom:5px;'>Étape 1 / 4</div>
    <h2 style='color:#EC4400; margin:0;'>📤 Import du fichier Excel</h2>
</div>
""", unsafe_allow_html=True)

# Barre de progression
st.markdown("""
<div style='width:100%; height:6px; background:#e0e0e0; border-radius:3px; margin:20px 0;'>
    <div style='width:25%; height:100%; background:#EC4400; border-radius:3px;'></div>
</div>
""", unsafe_allow_html=True)

# Upload du fichier
st.markdown("<div style='margin:40px 0;'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Déposez votre fichier Excel ici",
    type=["xlsx", "xls"],
    help="Formats acceptés : .xlsx, .xls"
)
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.session_state.uploaded_data = df
        st.session_state.filename = uploaded_file.name

        # Success message avec style
        st.markdown(f"""
        <div style='padding:15px; background:#d4edda; border-left:4px solid #28a745; border-radius:4px; margin:20px 0;'>
            ✅ <strong>Fichier importé avec succès :</strong> {uploaded_file.name}
        </div>
        """, unsafe_allow_html=True)

        # Statistiques du fichier
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div style='text-align:center; padding:20px; background:#f8f9fa; border-radius:8px;'>
                <div style='font-size:32px; color:#EC4400; font-weight:bold;'>{len(df)}</div>
                <div style='color:#666; font-size:14px;'>Lignes</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style='text-align:center; padding:20px; background:#f8f9fa; border-radius:8px;'>
                <div style='font-size:32px; color:#EC4400; font-weight:bold;'>{len(df.columns)}</div>
                <div style='color:#666; font-size:14px;'>Colonnes</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            taille = round(uploaded_file.size / 1024, 1)
            st.markdown(f"""
            <div style='text-align:center; padding:20px; background:#f8f9fa; border-radius:8px;'>
                <div style='font-size:32px; color:#EC4400; font-weight:bold;'>{taille}</div>
                <div style='color:#666; font-size:14px;'>Ko</div>
            </div>
            """, unsafe_allow_html=True)

        # Aperçu des données
        st.markdown("<h4 style='margin-top:30px;'>Aperçu des données</h4>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True, height=300)

        # Colonnes détectées - version compacte
        with st.expander(f"📋 Voir les {len(df.columns)} colonnes détectées"):
            cols_html = ""
            for col in df.columns:
                cols_html += f"""
                <span style='display:inline-block; background:#f0f2f6; color:#31333f; 
                             padding:6px 14px; margin:4px; border-radius:20px; 
                             font-size:13px; border:1px solid #d0d0d0;'>
                    {col}
                </span>
                """
            st.markdown(cols_html, unsafe_allow_html=True)

    except Exception as e:
        st.markdown(f"""
        <div style='padding:15px; background:#f8d7da; border-left:4px solid #dc3545; border-radius:4px;'>
            ❌ <strong>Erreur :</strong> {str(e)}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align:center; padding:40px; background:#e7f3ff; border-radius:8px; border:2px dashed #2196F3;'>
        <div style='font-size:48px; margin-bottom:10px;'>📁</div>
        <div style='color:#666;'>Aucun fichier importé pour le moment</div>
    </div>
    """, unsafe_allow_html=True)

# Navigation
st.markdown("<div style='margin-top:50px;'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Retour à l'accueil", use_container_width=True):
        st.switch_page("Home.py")

with col2:
    is_disabled = "uploaded_data" not in st.session_state
    if st.button("Suivant : Connexion SQL ➡️", use_container_width=True, 
                 type="primary", disabled=is_disabled):
        st.switch_page("pages/2_🔌_Connexion.py")
st.markdown("</div>", unsafe_allow_html=True)
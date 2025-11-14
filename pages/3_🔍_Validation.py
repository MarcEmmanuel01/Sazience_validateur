import streamlit as st
import pandas as pd
import os

# Configuration
st.set_page_config(page_title="Étape 2 - Validation", page_icon="🔍", layout="centered")

# Vérifier les prérequis
if "uploaded_data" not in st.session_state:
    st.warning("⚠️ Vous devez d'abord importer un fichier Excel.")
    if st.button("⬅️ Retour à l'étape 1"):
        st.switch_page("pages/1_📤_Upload.py")
    st.stop()

# Header avec progression
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <div style='color:#999; font-size:14px; margin-bottom:5px;'>Étape 2 / 3</div>
    <h2 style='color:#EC4400; margin:0;'>🔍 Validation par Fichier de Référence</h2>
</div>
""", unsafe_allow_html=True)

# Barre de progression
st.markdown("""
<div style='width:100%; height:6px; background:#e0e0e0; border-radius:3px; margin:20px 0;'>
    <div style='width:66%; height:100%; background:#EC4400; border-radius:3px;'></div>
</div>
""", unsafe_allow_html=True)

# Récupérer les données uploadées
df = st.session_state.uploaded_data

# Section 1 : Sélection du fichier de référence
st.markdown("<h4 style='margin-top:30px;'>1️⃣ Sélection du fichier de référence</h4>", unsafe_allow_html=True)

# Chemin vers le dossier de référence
REFERENCE_FOLDER = "LES_TABLES"

# Lister les fichiers Excel disponibles
try:
    excel_files = [f for f in os.listdir(REFERENCE_FOLDER) if f.endswith('.xlsx')]
    
    if not excel_files:
        st.error("❌ Aucun fichier Excel trouvé dans le dossier de référence")
        st.stop()
    
    selected_file = st.selectbox(
        "📊 Fichier de référence",
        options=excel_files,
        key="sel_file"
    )
    
    if selected_file:
        # Charger le fichier de référence
        file_path = os.path.join(REFERENCE_FOLDER, selected_file)
        df_reference = pd.read_excel(file_path)
        st.session_state.df_reference = df_reference
        st.session_state.selected_file = selected_file
        
        # Aperçu du fichier de référence
        with st.expander("👁️ Aperçu du fichier de référence"):
            st.dataframe(df_reference.head(10))
            st.write(f"**Dimensions :** {df_reference.shape[0]} lignes × {df_reference.shape[1]} colonnes")
            
except Exception as e:
    st.error(f"❌ Erreur lors du chargement des fichiers : {str(e)}")

# Section 2 : Mapping des colonnes
if 'df_reference' in st.session_state:
    st.markdown("<h4 style='margin-top:30px;'>2️⃣ Mapping des colonnes</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 Colonne Excel (à valider)**")
        colonne_excel = st.selectbox(
            "Sélectionnez la colonne à valider dans votre fichier",
            options=df.columns.tolist(),
            key="col_excel"
        )
    
    with col2:
        st.markdown("**🗃️ Colonne de Référence**")
        colonne_reference = st.selectbox(
            "Sélectionnez la colonne de référence",
            options=st.session_state.df_reference.columns.tolist(),
            key="col_ref"
        )

# Section 3 : Lancer la validation
if 'col_excel' in st.session_state and 'col_ref' in st.session_state:
    st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
    
    if st.button("🚀 Lancer la validation", use_container_width=True, type="primary"):
        with st.spinner("Validation en cours..."):
            try:
                # Récupérer les données
                df_ref = st.session_state.df_reference
                colonne_excel = st.session_state.col_excel
                colonne_reference = st.session_state.col_ref
                
                # Récupérer les valeurs de référence
                valeurs_reference = set(df_ref[colonne_reference].dropna().astype(str).unique())
                
                # Récupérer les valeurs du fichier uploadé
                valeurs_excel = df[colonne_excel].dropna().astype(str).unique()
                
                # Comparer
                valeurs_valides = [v for v in valeurs_excel if v in valeurs_reference]
                valeurs_invalides = [v for v in valeurs_excel if v not in valeurs_reference]
                
                # Sauvegarder les résultats
                st.session_state.resultats_validation = {
                    'valides': valeurs_valides,
                    'invalides': valeurs_invalides,
                    'colonne_excel': colonne_excel,
                    'colonne_reference': colonne_reference,
                    'fichier_reference': st.session_state.selected_file,
                    'total_reference': len(valeurs_reference)
                }
                
                # Afficher les résultats
                total = len(valeurs_valides) + len(valeurs_invalides)
                taux = (len(valeurs_valides) / total * 100) if total > 0 else 0
                
                st.markdown(f"""
                <div style='text-align:center; margin:30px 0;'>
                    <div style='font-size:48px; color:#EC4400; font-weight:bold; margin-bottom:10px;'>
                        {taux:.1f}%
                    </div>
                    <div style='font-size:18px; color:#666;'>Taux de validation</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div style='padding:20px; background:#d4edda; border-radius:8px; text-align:center;'>
                        <div style='font-size:32px; color:#28a745; font-weight:bold;'>{len(valeurs_valides)}</div>
                        <div style='color:#155724;'>✅ Valeurs valides</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style='padding:20px; background:#f8d7da; border-radius:8px; text-align:center;'>
                        <div style='font-size:32px; color:#dc3545; font-weight:bold;'>{len(valeurs_invalides)}</div>
                        <div style='color:#721c24;'>❌ Valeurs invalides</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div style='padding:20px; background:#e2e3e5; border-radius:8px; text-align:center;'>
                        <div style='font-size:32px; color:#6c757d; font-weight:bold;'>{st.session_state.resultats_validation['total_reference']}</div>
                        <div style='color:#383d41;'>📊 Références totales</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Afficher les détails
                with st.expander("📋 Détails des valeurs invalides"):
                    if valeurs_invalides:
                        st.write("**Valeurs non trouvées dans le fichier de référence :**")
                        for i, valeur in enumerate(valeurs_invalides[:50]):  # Limite à 50 premières
                            st.write(f"- {valeur}")
                        if len(valeurs_invalides) > 50:
                            st.write(f"... et {len(valeurs_invalides) - 50} autres")
                    else:
                        st.success("🎉 Toutes les valeurs sont valides !")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la validation : {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Navigation
st.markdown("<div style='margin-top:50px;'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Étape précédente", use_container_width=True):
        st.switch_page("pages/1_📤_Upload.py")

with col2:
    is_disabled = 'resultats_validation' not in st.session_state
    if st.button("Suivant : Résultats ➡️", use_container_width=True, 
                 type="primary", disabled=is_disabled):
        st.switch_page("pages/4_📊_Resultats.py")
st.markdown("</div>", unsafe_allow_html=True)
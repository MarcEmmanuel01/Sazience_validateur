import streamlit as st
import pandas as pd
from io import BytesIO

# Configuration
st.set_page_config(page_title="Étape 4 - Résultats", page_icon="📊", layout="wide")

# Vérifier les prérequis
if "uploaded_data" not in st.session_state:
    st.warning("⚠️ Vous devez d'abord importer un fichier Excel.")
    if st.button("⬅️ Retour à l'étape 1"):
        st.switch_page("pages/1_Upload.py")
    st.stop()

if "resultats_validation" not in st.session_state:
    st.warning("⚠️ Vous devez d'abord exécuter la validation.")
    if st.button("⬅️ Retour à l'étape 3"):
        st.switch_page("pages/3_Validation.py")
    st.stop()

# Header avec progression
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <div style='color:#999; font-size:14px; margin-bottom:5px;'>Étape 4 / 4</div>
    <h2 style='color:#EC4400; margin:0;'>📊 Résultats de la validation</h2>
</div>
""", unsafe_allow_html=True)

# Barre de progression
st.markdown("""
<div style='width:100%; height:6px; background:#e0e0e0; border-radius:3px; margin:20px 0 40px 0;'>
    <div style='width:100%; height:100%; background:#EC4400; border-radius:3px;'></div>
</div>
""", unsafe_allow_html=True)

# Récupérer les données
df = st.session_state.uploaded_data
resultats = st.session_state.resultats_validation

# Créer le DataFrame avec statuts
df_resultats = df.copy()
df_resultats['STATUT_VALIDATION'] = df_resultats[resultats['colonne_excel']].astype(str).apply(
    lambda x: '✅ VALIDE' if x in resultats['valides'] else '❌ INVALIDE'
)

# Statistiques globales
st.markdown("<h3>📈 Vue d'ensemble</h3>", unsafe_allow_html=True)

total_lignes = len(df_resultats)
lignes_valides = len(df_resultats[df_resultats['STATUT_VALIDATION'] == '✅ VALIDE'])
lignes_invalides = len(df_resultats[df_resultats['STATUT_VALIDATION'] == '❌ INVALIDE'])
taux = (lignes_valides / total_lignes * 100) if total_lignes > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style='padding:25px; background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius:12px; text-align:center; color:white;'>
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{total_lignes}</div>
        <div style='font-size:14px; opacity:0.9;'>Total lignes</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='padding:25px; background:linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                border-radius:12px; text-align:center; color:white;'>
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{lignes_valides}</div>
        <div style='font-size:14px; opacity:0.9;'>✅ Valides</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='padding:25px; background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                border-radius:12px; text-align:center; color:white;'>
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{lignes_invalides}</div>
        <div style='font-size:14px; opacity:0.9;'>❌ Invalides</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='padding:25px; background:linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                border-radius:12px; text-align:center; color:white;'>
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{taux:.1f}%</div>
        <div style='font-size:14px; opacity:0.9;'>Taux de réussite</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin:40px 0;'>", unsafe_allow_html=True)

# Onglets pour afficher les différentes vues
tab1, tab2, tab3 = st.tabs(["📋 Toutes les données", "✅ Valides uniquement", "❌ Invalides uniquement"])

with tab1:
    st.markdown(f"""
    <div style='margin-bottom:15px;'>
        <strong>Validation :</strong> {resultats['colonne_excel']} ➡️ {resultats['table_bd']}.{resultats['colonne_bd']}
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(df_resultats, use_container_width=True, height=400)

with tab2:
    donnees_valides = df_resultats[df_resultats['STATUT_VALIDATION'] == '✅ VALIDE']
    st.success(f"✅ {len(donnees_valides)} lignes valides")
    st.dataframe(donnees_valides, use_container_width=True, height=400)

with tab3:
    donnees_invalides = df_resultats[df_resultats['STATUT_VALIDATION'] == '❌ INVALIDE']
    
    if len(donnees_invalides) > 0:
        st.error(f"❌ {len(donnees_invalides)} lignes invalides")
        st.dataframe(donnees_invalides, use_container_width=True, height=400)
        
        # Détail des valeurs invalides
        st.markdown("<h4 style='margin-top:30px;'>🔍 Détail des valeurs invalides</h4>", unsafe_allow_html=True)
        valeurs_invalides_count = donnees_invalides[resultats['colonne_excel']].value_counts()
        
        df_invalides = pd.DataFrame({
            'Valeur': valeurs_invalides_count.index,
            'Occurrences': valeurs_invalides_count.values
        })
        st.dataframe(df_invalides, use_container_width=True, height=250)
    else:
        st.success("🎉 Aucune valeur invalide !")

st.markdown("</div>", unsafe_allow_html=True)

# Export des résultats
st.markdown("<h3 style='margin-top:40px;'>💾 Export des résultats</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Export Excel complet
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_resultats.to_excel(writer, sheet_name='Résultats_complets', index=False)
        if lignes_invalides > 0:
            donnees_invalides.to_excel(writer, sheet_name='Valeurs_invalides', index=False)
    
    st.download_button(
        label="📥 Rapport complet (Excel)",
        data=output.getvalue(),
        file_name=f"validation_complete_{resultats['colonne_excel']}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col2:
    # Export CSV
    csv = df_resultats.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Export CSV",
        data=csv,
        file_name=f"validation_{resultats['colonne_excel']}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col3:
    # Export invalides uniquement
    if lignes_invalides > 0:
        output_inv = BytesIO()
        with pd.ExcelWriter(output_inv, engine='openpyxl') as writer:
            donnees_invalides.to_excel(writer, sheet_name='Invalides', index=False)
        
        st.download_button(
            label="⚠️ Invalides uniquement",
            data=output_inv.getvalue(),
            file_name=f"invalides_{resultats['colonne_excel']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# Navigation
st.markdown("<div style='margin-top:50px;'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Étape précédente", use_container_width=True):
        st.switch_page("pages/3_🔍_Validation.py")

with col2:
    if st.button("🏁 Terminer et recommencer", use_container_width=True, type="primary"):
        # Nettoyer la session pour recommencer
        keys_to_keep = []
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                del st.session_state[key]
        st.switch_page("Home.py")

st.markdown("</div>", unsafe_allow_html=True)
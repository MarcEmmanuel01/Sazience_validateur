import streamlit as st
import pandas as pd

# Configuration
st.set_page_config(page_title="Étape 3 - Résultats", page_icon="📊", layout="wide")

# Vérifier les prérequis
if "uploaded_data" not in st.session_state:
    st.warning("⚠️ Vous devez d'abord importer un fichier Excel.")
    if st.button("⬅️ Retour à l'étape 1"):
        st.switch_page("pages/1_📤_Upload.py")
    st.stop()

if "resultats_validation" not in st.session_state:
    st.warning("⚠️ Vous devez d'abord exécuter la validation.")
    if st.button("⬅️ Retour à l'étape 2"):
        st.switch_page("pages/3_🔍_Validation.py")
    st.stop()

# Header avec progression
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <div style='color:#999; font-size:14px; margin-bottom:5px;'>Étape 3 / 3</div>
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
resultats_globaux = st.session_state.resultats_validation
validations = resultats_globaux['validations']

# Créer le DataFrame avec tous les statuts de validation
df_resultats = df.copy()

for validation in validations:
    colonne_excel = validation['colonne_excel']
    nom_colonne_statut = f"STATUT_{colonne_excel}"
    
    # Nettoyer et normaliser pour la comparaison
    valeurs_valides_set = set(validation['valeurs_valides_uniques'])
    
    df_resultats[nom_colonne_statut] = df_resultats[colonne_excel].astype(str).str.strip().str.upper().apply(
        lambda x: '✅ VALIDE' if x in valeurs_valides_set else '❌ INVALIDE'
    )

# Créer une colonne globale : VALIDE seulement si TOUTES les validations sont OK
colonnes_statut = [f"STATUT_{v['colonne_excel']}" for v in validations]
df_resultats['STATUT_GLOBAL'] = df_resultats[colonnes_statut].apply(
    lambda row: '✅ TOUTES VALIDES' if all(val == '✅ VALIDE' for val in row) else '❌ AU MOINS 1 INVALIDE',
    axis=1
)

# Statistiques globales
st.markdown("<h3>📈 Vue d'ensemble globale</h3>", unsafe_allow_html=True)

total_lignes = len(df_resultats)
lignes_toutes_valides = len(df_resultats[df_resultats['STATUT_GLOBAL'] == '✅ TOUTES VALIDES'])
lignes_avec_erreurs = len(df_resultats[df_resultats['STATUT_GLOBAL'] == '❌ AU MOINS 1 INVALIDE'])
taux_global = (lignes_toutes_valides / total_lignes * 100) if total_lignes > 0 else 0

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
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{lignes_toutes_valides}</div>
        <div style='font-size:14px; opacity:0.9;'>✅ 100% Valides</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='padding:25px; background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                border-radius:12px; text-align:center; color:white;'>
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{lignes_avec_erreurs}</div>
        <div style='font-size:14px; opacity:0.9;'>❌ Avec erreurs</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style='padding:25px; background:linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                border-radius:12px; text-align:center; color:white;'>
        <div style='font-size:36px; font-weight:bold; margin-bottom:8px;'>{taux_global:.1f}%</div>
        <div style='font-size:14px; opacity:0.9;'>Taux global</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin:40px 0;'>", unsafe_allow_html=True)

# Détail par validation
st.markdown("<h3>🔍 Détail par validation</h3>", unsafe_allow_html=True)

for idx, validation in enumerate(validations):
    colonne_excel = validation['colonne_excel']
    nom_colonne_statut = f"STATUT_{colonne_excel}"
    
    lignes_valides = validation['nb_lignes_valides']
    lignes_invalides = validation['nb_lignes_invalides']
    total_lignes_col = lignes_valides + lignes_invalides
    taux_lignes = (lignes_valides / total_lignes_col * 100) if total_lignes_col > 0 else 0
    
    # Statistiques sur valeurs uniques
    nb_valeurs_valides = len(validation['valeurs_valides_uniques'])
    nb_valeurs_invalides = len(validation['valeurs_invalides_uniques'])
    total_valeurs = nb_valeurs_valides + nb_valeurs_invalides
    taux_valeurs = (nb_valeurs_valides / total_valeurs * 100) if total_valeurs > 0 else 0
    
    with st.expander(f"**Validation #{idx+1} : {colonne_excel}** → {validation['colonne_reference']}", expanded=(idx==0)):
        
        # Afficher les 2 types de statistiques
        st.markdown("#### 📊 Statistiques sur les valeurs uniques")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Taux valeurs uniques", f"{taux_valeurs:.1f}%")
        with col2:
            st.metric("✅ Valeurs valides", nb_valeurs_valides)
        with col3:
            st.metric("❌ Valeurs invalides", nb_valeurs_invalides)
        with col4:
            st.metric("📊 Références", validation['total_reference'])
        
        st.markdown("#### 📄 Statistiques sur les lignes")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Taux lignes", f"{taux_lignes:.1f}%")
        with col2:
            st.metric("✅ Lignes valides", lignes_valides)
        with col3:
            st.metric("❌ Lignes invalides", lignes_invalides)
        
        if nb_valeurs_invalides > 0:
            st.markdown("---")
            st.markdown("**🔍 Liste des valeurs invalides uniques :**")
            
            # Créer un DataFrame avec les valeurs invalides et leur nombre d'occurrences
            valeurs_invalides = df_resultats[df_resultats[nom_colonne_statut] == '❌ INVALIDE'][colonne_excel]
            valeurs_invalides_nettoyees = valeurs_invalides.astype(str).str.strip().str.upper()
            compte = valeurs_invalides_nettoyees.value_counts()
            
            df_invalides = pd.DataFrame({
                'Valeur invalide': compte.index,
                'Nombre d\'occurrences': compte.values
            })
            
            st.dataframe(df_invalides, use_container_width=True, height=300)
            
            # Bouton de téléchargement des valeurs invalides
            csv_invalides = df_invalides.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"💾 Télécharger les {nb_valeurs_invalides} valeurs invalides",
                data=csv_invalides,
                file_name=f"valeurs_invalides_{colonne_excel}.csv",
                mime="text/csv",
                key=f"download_invalid_{idx}"
            )
        else:
            st.success("🎉 Toutes les valeurs sont valides pour cette colonne !")

st.markdown("</div>", unsafe_allow_html=True)

# Information sur la validation
st.markdown(f"""
<div style='padding:15px; background:#f0f2f6; border-radius:8px; margin:20px 0;'>
    <strong>Fichier de référence :</strong> {resultats_globaux['fichier_reference']}<br>
    <strong>Nombre de validations :</strong> {len(validations)}
</div>
""", unsafe_allow_html=True)

# Onglets pour afficher les différentes vues
tab1, tab2, tab3 = st.tabs(["📋 Toutes les données", "✅ 100% Valides", "❌ Avec erreurs"])

with tab1:
    st.info(f"📊 Affichage de {len(df_resultats)} lignes avec {len(validations)} validation(s)")
    st.dataframe(df_resultats, use_container_width=True, height=400)

with tab2:
    donnees_valides = df_resultats[df_resultats['STATUT_GLOBAL'] == '✅ TOUTES VALIDES']
    st.success(f"✅ {len(donnees_valides)} lignes avec toutes les validations OK")
    if len(donnees_valides) > 0:
        st.dataframe(donnees_valides, use_container_width=True, height=400)
    else:
        st.warning("Aucune ligne ne passe toutes les validations")

with tab3:
    donnees_invalides = df_resultats[df_resultats['STATUT_GLOBAL'] == '❌ AU MOINS 1 INVALIDE']
    
    if len(donnees_invalides) > 0:
        st.error(f"❌ {len(donnees_invalides)} lignes avec au moins une validation échouée")
        st.dataframe(donnees_invalides, use_container_width=True, height=400)
    else:
        st.success("🎉 Aucune erreur de validation !")

# Export des résultats
st.markdown("<h3 style='margin-top:40px;'>💾 Export des résultats</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    # Export toutes les données
    csv_all = df_resultats.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Toutes les données",
        data=csv_all,
        file_name="validation_complete.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    # Export uniquement les valides
    if len(donnees_valides) > 0:
        csv_valides = donnees_valides.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Données 100% valides",
            data=csv_valides,
            file_name="validation_valides.csv",
            mime="text/csv",
            use_container_width=True
        )

with col3:
    # Export uniquement les erreurs
    if len(donnees_invalides) > 0:
        csv_errors = donnees_invalides.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Données avec erreurs",
            data=csv_errors,
            file_name="validation_erreurs.csv",
            mime="text/csv",
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
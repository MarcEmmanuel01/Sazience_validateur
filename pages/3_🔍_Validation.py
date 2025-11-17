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
REFERENCE_FOLDER = "SOURCES"

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

# Section 2 : Mapping des colonnes (MULTI-SÉLECTION)
if 'df_reference' in st.session_state:
    st.markdown("<h4 style='margin-top:30px;'>2️⃣ Configuration des validations</h4>", unsafe_allow_html=True)
    
    # Initialiser le nombre de paires si pas déjà fait
    if 'nb_mappings' not in st.session_state:
        st.session_state.nb_mappings = 1
    
    # Boutons pour ajouter/retirer des mappings
    col_btn1, col_btn2, col_spacer = st.columns([1, 1, 2])
    with col_btn1:
        if st.button("➕ Ajouter une validation", use_container_width=True):
            st.session_state.nb_mappings += 1
            st.rerun()
    with col_btn2:
        if st.button("➖ Retirer la dernière", use_container_width=True, 
                     disabled=st.session_state.nb_mappings <= 1):
            st.session_state.nb_mappings -= 1
            st.rerun()
    
    st.markdown("<div style='margin:20px 0;'>", unsafe_allow_html=True)
    
    # Créer les paires de sélection
    mappings = []
    for i in range(st.session_state.nb_mappings):
        st.markdown(f"""
        <div style='background:#f8f9fa; padding:15px; border-radius:8px; margin:15px 0; border-left:4px solid #EC4400;'>
            <strong>Validation #{i+1}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📤 Colonne Excel (à valider)**")
            colonne_excel = st.selectbox(
                f"Colonne à valider",
                options=df.columns.tolist(),
                key=f"col_excel_{i}",
                label_visibility="collapsed"
            )
        
        with col2:
            st.markdown("**🗃️ Colonne de Référence**")
            colonne_reference = st.selectbox(
                f"Colonne de référence",
                options=st.session_state.df_reference.columns.tolist(),
                key=f"col_ref_{i}",
                label_visibility="collapsed"
            )
        
        mappings.append({
            'excel': colonne_excel,
            'reference': colonne_reference
        })
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Section 3 : Lancer la validation
    st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
    
    if st.button("🚀 Lancer toutes les validations", use_container_width=True, type="primary"):
        with st.spinner("Validation en cours..."):
            try:
                df_ref = st.session_state.df_reference
                tous_resultats = []
                
                # Valider chaque paire
                for idx, mapping in enumerate(mappings):
                    colonne_excel = mapping['excel']
                    colonne_reference = mapping['reference']
                    
                    # Récupérer les valeurs de référence (NETTOYÉES)
                    valeurs_reference = set(
                        str(v).strip().upper() 
                        for v in df_ref[colonne_reference].dropna().unique()
                    )
                    
                    # Récupérer les valeurs du fichier uploadé (NETTOYÉES)
                    valeurs_excel_brutes = df[colonne_excel].dropna()
                    valeurs_excel_uniques = valeurs_excel_brutes.astype(str).str.strip().str.upper().unique()
                    
                    # Comparer (valeurs uniques)
                    valeurs_valides_uniques = [v for v in valeurs_excel_uniques if v in valeurs_reference]
                    valeurs_invalides_uniques = [v for v in valeurs_excel_uniques if v not in valeurs_reference]
                    
                    # Calculer le nombre de LIGNES affectées
                    valeurs_excel_nettoyees = valeurs_excel_brutes.astype(str).str.strip().str.upper()
                    nb_lignes_valides = valeurs_excel_nettoyees.isin(valeurs_reference).sum()
                    nb_lignes_invalides = (~valeurs_excel_nettoyees.isin(valeurs_reference)).sum()
                    
                    tous_resultats.append({
                        'index': idx + 1,
                        'valeurs_valides_uniques': valeurs_valides_uniques,
                        'valeurs_invalides_uniques': valeurs_invalides_uniques,
                        'nb_lignes_valides': int(nb_lignes_valides),
                        'nb_lignes_invalides': int(nb_lignes_invalides),
                        'colonne_excel': colonne_excel,
                        'colonne_reference': colonne_reference,
                        'total_reference': len(valeurs_reference),
                        'total_valeurs_excel': len(valeurs_excel_uniques)
                    })
                
                # Sauvegarder tous les résultats
                st.session_state.resultats_validation = {
                    'validations': tous_resultats,
                    'fichier_reference': st.session_state.selected_file
                }
                
                # Afficher un résumé
                st.markdown("<h3 style='margin-top:30px;'>📊 Résumé des validations</h3>", unsafe_allow_html=True)
                
                for resultat in tous_resultats:
                    # Taux basé sur les VALEURS UNIQUES
                    total_valeurs = len(resultat['valeurs_valides_uniques']) + len(resultat['valeurs_invalides_uniques'])
                    taux_valeurs = (len(resultat['valeurs_valides_uniques']) / total_valeurs * 100) if total_valeurs > 0 else 0
                    
                    # Taux basé sur les LIGNES
                    total_lignes = resultat['nb_lignes_valides'] + resultat['nb_lignes_invalides']
                    taux_lignes = (resultat['nb_lignes_valides'] / total_lignes * 100) if total_lignes > 0 else 0
                    
                    # Déterminer la couleur selon le taux
                    if taux_valeurs == 100:
                        bg_color = "#d4edda"
                        border_color = "#28a745"
                    elif taux_valeurs >= 80:
                        bg_color = "#fff3cd"
                        border_color = "#ffc107"
                    else:
                        bg_color = "#f8d7da"
                        border_color = "#dc3545"
                    
                    st.markdown(f"""
                    <div style='background:{bg_color}; padding:20px; border-radius:8px; margin:15px 0; border-left:5px solid {border_color};'>
                        <h4 style='color:#333; margin-top:0;'>✓ Validation #{resultat['index']} : {resultat['colonne_excel']}</h4>
                        <div style='color:#666; font-size:13px; margin-bottom:10px;'>
                            Comparé avec : <strong>{resultat['colonne_reference']}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:28px; color:#EC4400; font-weight:bold;'>{taux_valeurs:.1f}%</div>
                            <div style='font-size:11px; color:#666;'>Taux valeurs</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:22px; color:#28a745; font-weight:bold;'>{len(resultat['valeurs_valides_uniques'])}</div>
                            <div style='font-size:11px; color:#666;'>✅ Valeurs OK</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:22px; color:#dc3545; font-weight:bold;'>{len(resultat['valeurs_invalides_uniques'])}</div>
                            <div style='font-size:11px; color:#666;'>❌ Valeurs KO</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:22px; color:#17a2b8; font-weight:bold;'>{resultat['nb_lignes_valides']}</div>
                            <div style='font-size:11px; color:#666;'>📄 Lignes valides</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col5:
                        st.markdown(f"""
                        <div style='text-align:center;'>
                            <div style='font-size:22px; color:#6c757d; font-weight:bold;'>{resultat['total_reference']}</div>
                            <div style='font-size:11px; color:#666;'>📊 Références</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Afficher les valeurs invalides si présentes
                    if resultat['valeurs_invalides_uniques']:
                        with st.expander(f"🔍 Voir les {len(resultat['valeurs_invalides_uniques'])} valeurs UNIQUES invalides"):
                            st.warning(f"Ces valeurs apparaissent dans {resultat['nb_lignes_invalides']} lignes au total")
                            for i, valeur in enumerate(resultat['valeurs_invalides_uniques'][:100]):
                                st.write(f"- {valeur}")
                            if len(resultat['valeurs_invalides_uniques']) > 100:
                                st.write(f"... et {len(resultat['valeurs_invalides_uniques']) - 100} autres")
                    else:
                        st.success("🎉 Toutes les valeurs sont valides !")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la validation : {str(e)}")
                st.exception(e)
    
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
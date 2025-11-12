import streamlit as st
import pandas as pd
import pyodbc

# Configuration
st.set_page_config(page_title="Étape 3 - Validation", page_icon="🔍", layout="centered")

# Vérifier les prérequis
if "uploaded_data" not in st.session_state:
    st.warning("⚠️ Vous devez d'abord importer un fichier Excel.")
    if st.button("⬅️ Retour à l'étape 1"):
        st.switch_page("pages/1_Upload.py")
    st.stop()

if not st.session_state.get("sql_ok", False):
    st.warning("⚠️ Vous devez d'abord configurer la connexion SQL Server.")
    if st.button("⬅️ Retour à l'étape 2"):
        st.switch_page("pages/2_Connexion.py")
    st.stop()

# Header avec progression
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <div style='color:#999; font-size:14px; margin-bottom:5px;'>Étape 3 / 4</div>
    <h2 style='color:#EC4400; margin:0;'>🔍 Configuration et Validation</h2>
</div>
""", unsafe_allow_html=True)

# Barre de progression
st.markdown("""
<div style='width:100%; height:6px; background:#e0e0e0; border-radius:3px; margin:20px 0;'>
    <div style='width:75%; height:100%; background:#EC4400; border-radius:3px;'></div>
</div>
""", unsafe_allow_html=True)

# Récupérer les données
df = st.session_state.uploaded_data
conn_str = st.session_state.connection_string

# Section 1 : Sélection de la base et table
st.markdown("<h4 style='margin-top:30px;'>1️⃣ Sélection de la table SQL</h4>", unsafe_allow_html=True)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Lister les bases de données
    cursor.execute("""
        SELECT name FROM sys.databases 
        WHERE state = 0 AND name NOT IN ('master', 'tempdb', 'model', 'msdb')
        ORDER BY name
    """)
    databases = [row[0] for row in cursor.fetchall()]
    
    selected_db = st.selectbox("📊 Base de données", databases, key="sel_db")
    
    if selected_db:
        # Changer de base
        cursor.execute(f"USE [{selected_db}]")
        
        # Lister les tables
        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        tables = cursor.fetchall()
        table_options = [f"{schema}.{name}" for schema, name in tables]
        
        selected_table = st.selectbox("📋 Table", table_options, key="sel_table")
        
        if selected_table:
            st.session_state.selected_db = selected_db
            st.session_state.selected_table = selected_table
            
            # Récupérer les colonnes de la table
            schema, table_name = selected_table.split('.')
            cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """, schema, table_name)
            colonnes_table = [row[0] for row in cursor.fetchall()]
            st.session_state.colonnes_table = colonnes_table
    
    conn.close()
    
except Exception as e:
    st.error(f"❌ Erreur : {str(e)}")

# Section 2 : Mapping des colonnes
if 'colonnes_table' in st.session_state:
    st.markdown("<h4 style='margin-top:30px;'>2️⃣ Mapping des colonnes</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📤 Colonne Excel**")
        colonne_excel = st.selectbox(
            "Sélectionnez la colonne à valider",
            options=df.columns.tolist(),
            key="col_excel"
        )
    
    with col2:
        st.markdown("**🗃️ Colonne SQL**")
        colonne_bd = st.selectbox(
            "Sélectionnez la colonne de référence",
            options=st.session_state.colonnes_table,
            key="col_bd"
        )

# Section 3 : Lancer la validation
if 'col_excel' in st.session_state and 'col_bd' in st.session_state:
    st.markdown("<div style='margin-top:40px;'>", unsafe_allow_html=True)
    
    if st.button("🚀 Lancer la validation", use_container_width=True, type="primary"):
        with st.spinner("Validation en cours..."):
            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute(f"USE [{st.session_state.selected_db}]")
                
                # Récupérer les valeurs de référence depuis SQL
                colonne_bd = st.session_state.col_bd
                selected_table = st.session_state.selected_table
                
                cursor.execute(f"""
                    SELECT DISTINCT [{colonne_bd}] 
                    FROM {selected_table} 
                    WHERE [{colonne_bd}] IS NOT NULL
                """)
                valeurs_reference = {str(row[0]) for row in cursor.fetchall()}
                conn.close()
                
                # Récupérer les valeurs du fichier Excel
                colonne_excel = st.session_state.col_excel
                valeurs_excel = df[colonne_excel].dropna().astype(str).unique()
                
                # Comparer
                valeurs_valides = [v for v in valeurs_excel if v in valeurs_reference]
                valeurs_invalides = [v for v in valeurs_excel if v not in valeurs_reference]
                
                # Sauvegarder les résultats
                st.session_state.resultats_validation = {
                    'valides': valeurs_valides,
                    'invalides': valeurs_invalides,
                    'colonne_excel': colonne_excel,
                    'colonne_bd': colonne_bd,
                    'table_bd': selected_table
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
                
                col1, col2 = st.columns(2)
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
                
            except Exception as e:
                st.error(f"❌ Erreur lors de la validation : {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Navigation
st.markdown("<div style='margin-top:50px;'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Étape précédente", use_container_width=True):
        st.switch_page("pages/2_🔌_Connexion.py")

with col2:
    is_disabled = 'resultats_validation' not in st.session_state
    if st.button("Suivant : Résultats ➡️", use_container_width=True, 
                 type="primary", disabled=is_disabled):
        st.switch_page("pages/4_📊_Resultats.py")
st.markdown("</div>", unsafe_allow_html=True)
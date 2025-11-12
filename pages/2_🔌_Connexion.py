import streamlit as st
import pyodbc

# Configuration
st.set_page_config(page_title="Étape 2 - Connexion SQL", page_icon="🔌", layout="centered")

# Header avec progression
st.markdown("""
<div style='text-align:center; margin-bottom:30px;'>
    <div style='color:#999; font-size:14px; margin-bottom:5px;'>Étape 2 / 4</div>
    <h2 style='color:#EC4400; margin:0;'>🔌 Connexion SQL Server</h2>
</div>
""", unsafe_allow_html=True)

# Barre de progression
st.markdown("""
<div style='width:100%; height:6px; background:#e0e0e0; border-radius:3px; margin:20px 0;'>
    <div style='width:50%; height:100%; background:#EC4400; border-radius:3px;'></div>
</div>
""", unsafe_allow_html=True)

# Formulaire de connexion
st.markdown("<div style='margin:40px 0;'>", unsafe_allow_html=True)

with st.form("connexion_sql_form"):
    serveur = st.text_input(
        "Serveur",
        value=st.session_state.get("sql_server", "WIN-E2SJ7PMI5BU\\BI"),
        placeholder="localhost ou WIN-xxx\\INSTANCE"
    )
    
    base = st.text_input(
        "Base de données",
        value=st.session_state.get("sql_database", ""),
        placeholder="Nom de la base (optionnel)"
    )
    
    utilisateur = st.text_input(
        "Utilisateur",
        value=st.session_state.get("sql_user", "sa")
    )
    
    motdepasse = st.text_input(
        "Mot de passe",
        type="password",
        value=st.session_state.get("sql_password", "")
    )
    
    st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
    tester = st.form_submit_button("🔍 Tester la connexion", use_container_width=True, type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

# Résultat du test
if tester:
    if not all([serveur, utilisateur, motdepasse]):
        st.markdown("""
        <div style='padding:15px; background:#fff3cd; border-left:4px solid #ffc107; border-radius:4px; margin:20px 0;'>
            ⚠️ <strong>Attention :</strong> Veuillez remplir au minimum le serveur, l'utilisateur et le mot de passe
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Test de connexion en cours..."):
            try:
                # Construction de la chaîne de connexion
                if base:
                    conn_str = f"""
                        DRIVER={{ODBC Driver 17 for SQL Server}};
                        SERVER={serveur};
                        DATABASE={base};
                        UID={utilisateur};
                        PWD={motdepasse};
                        TrustServerCertificate=yes;
                        Connection Timeout=5;
                    """
                else:
                    conn_str = f"""
                        DRIVER={{ODBC Driver 17 for SQL Server}};
                        SERVER={serveur};
                        UID={utilisateur};
                        PWD={motdepasse};
                        TrustServerCertificate=yes;
                        Connection Timeout=5;
                    """
                
                # Test de connexion
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                cursor.execute("SELECT @@SERVERNAME, DB_NAME()")
                server_name, db_name = cursor.fetchone()
                conn.close()

                # Succès
                st.markdown("""
                <div style='padding:15px; background:#d4edda; border-left:4px solid #28a745; border-radius:4px; margin:20px 0;'>
                    ✅ <strong>Connexion réussie !</strong>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style='padding:15px; background:#f8f9fa; border-radius:8px;'>
                        <div style='color:#666; font-size:12px;'>SERVEUR</div>
                        <div style='font-weight:600; color:#EC4400;'>{server_name}</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style='padding:15px; background:#f8f9fa; border-radius:8px;'>
                        <div style='color:#666; font-size:12px;'>BASE DE DONNÉES</div>
                        <div style='font-weight:600; color:#EC4400;'>{db_name or 'Par défaut'}</div>
                    </div>
                    """, unsafe_allow_html=True)

                # Sauvegarder les informations
                st.session_state.sql_server = serveur
                st.session_state.sql_database = base
                st.session_state.sql_user = utilisateur
                st.session_state.sql_password = motdepasse
                st.session_state.sql_ok = True
                st.session_state.connection_string = conn_str

            except Exception as e:
                st.markdown(f"""
                <div style='padding:15px; background:#f8d7da; border-left:4px solid #dc3545; border-radius:4px; margin:20px 0;'>
                    ❌ <strong>Connexion échouée</strong><br>
                    <div style='margin-top:8px; font-size:13px;'>{str(e)}</div>
                </div>
                """, unsafe_allow_html=True)
                st.session_state.sql_ok = False

# Afficher le statut si déjà connecté
if st.session_state.get("sql_ok", False) and not tester:
    st.markdown("""
    <div style='padding:15px; background:#d4edda; border-left:4px solid #28a745; border-radius:4px; margin:20px 0;'>
        ✅ Connexion déjà établie
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Navigation
st.markdown("<div style='margin-top:50px;'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Étape précédente", use_container_width=True):
        st.switch_page("pages/1_📤_Upload.py")

with col2:
    is_disabled = not st.session_state.get("sql_ok", False)
    if st.button("Suivant : Validation ➡️", use_container_width=True, 
                 type="primary", disabled=is_disabled):
        st.switch_page("pages/3_🔍_Validation.py")
st.markdown("</div>", unsafe_allow_html=True)
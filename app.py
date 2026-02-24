import streamlit as st
import pandas as pd
import plotly.express as px


# --- CONFIGURATION & CHARGEMENT ---
@st.cache_data 
def load_data():
    file_id = '14cbUlLwF9FXAVBxa3CHe_w8Y5veh3UBd'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'fires_clean.csv'
    
    # Téléchargement seulement s'il n'est pas déjà là
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)
    
    # Lecture (low_memory=False aide à éviter les avertissements de types)
    df = pd.read_csv(output, low_memory=False)
    
    # Optionnel : Conversion de colonnes temporelles si nécessaire
    if 'FIRE_YEAR' in df.columns:
        df['FIRE_YEAR'] = df['FIRE_YEAR'].astype(int)
        
    return df
    
# On charge le dataframe
df = load_data()

# Configuration de la page
st.set_page_config(page_title="Wildfires Analysis", layout="wide")

st.title("🔥 Analyse des Incendies aux USA")

# Barre latérale pour la navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Exploration des données", "Visualisations"])

if page == "Accueil":
    st.write("### Bienvenue dans le projet d'analyse des Wildfires")
    st.write("Ce dashboard interactif présente les résultats de notre étude sur les incendies de 1992 à 2015.")
    st.info("Utilisez le menu à gauche pour explorer les différentes étapes.")
    if st.checkbox("Afficher un aperçu des données"):
    st.dataframe(df.head(10))

elif page == "Exploration des données":
    st.header("🔍 Exploration et Qualité des données")
    st.write("Cette section présente l'analyse initiale des colonnes et les taux de valeurs manquantes.")
    
    # Ici vous pourrez ajouter vos fonctions d'analyse de colonnes
    # Exemple : st.write(df.isna().mean() * 100)

elif page == "Visualisations":
    st.header("📊 Graphiques et Cartographies")
    st.write("Analyse temporelle et géographique des incendies.")

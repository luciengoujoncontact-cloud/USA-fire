import streamlit as st
import pandas as pd
import plotly.express as px
import gdown
import os


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

# Données meteo - Lucien
elif page == "Analyse Météo":
    st.header("Influence des conditions Météo")
    st.write("Analyse de la corrélation entre la température, le vent et la sévérité des incendies.")

    # --- Graphique 1 : Histogramme Température ---
    st.subheader("Distribution des incendies selon la température")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['temp_max'], bins=30, kde=True, color='orange', edgecolor='black', ax=ax1)
    ax1.set_title('Fréquence des incendies selon la Température Maximale')
    ax1.set_xlabel('Température Maximale (°C)')
    ax1.set_ylabel('Nombre d\'incendies')
    st.pyplot(fig1)

    # --- Graphique 2 : Hexbin Densité (Temp vs Vent) ---
    st.subheader("Densité des feux : Température vs Vent")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    hb2 = ax2.hexbin(df['temp_max'], df['vent_max'], gridsize=30, cmap='YlOrRd', mincnt=1)
    cb2 = fig2.colorbar(hb2, ax=ax2)
    cb2.set_label('Densité des feux')
    ax2.set_title('Densité des feux : Température vs Vent')
    ax2.set_xlabel('Température Maximale (°C)')
    ax2.set_ylabel('Vitesse du vent (km/h)')
    st.pyplot(fig2)

    # --- Graphique 3 : Hexbin Sévérité (Taille Moyenne) ---
    st.subheader("Sévérité des feux : Température vs Vent")
    
    # Nettoyage rapide pour ce graphique spécifique
    df_plot = df.dropna(subset=['temp_max', 'vent_max', 'FIRE_SIZE_HECT'])
    
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    hb3 = ax3.hexbin(df_plot['temp_max'],
                    df_plot['vent_max'],
                    C=df_plot['FIRE_SIZE_HECT'],
                    reduce_C_function=np.mean,
                    gridsize=30,
                    cmap='YlOrBr',
                    mincnt=1)
    cb3 = fig3.colorbar(hb3, ax=ax3)
    cb3.set_label('Taille moyenne des feux (hectares)')
    ax3.set_title('Sévérité des feux selon les conditions météo')
    ax3.set_xlabel('Température Maximale (°C)')
    ax3.set_ylabel('Vitesse du vent (km/h)')
    st.pyplot(fig3)


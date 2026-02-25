import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import gdown
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Wildfires Analysis USA", layout="wide")

# FONCTION DE CHARGEMENT DES DONNÉES (CACHE) 
@st.cache_data 
def load_data():
    file_id = '14cbUlLwF9FXAVBxa3CHe_w8Y5veh3UBd'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'fires_clean.csv'
    
    # Téléchargement si le fichier n'est pas localement présent sur le serveur
    if not os.path.exists(output):
        with st.spinner('Téléchargement du dataset nettoyé... Veuillez patienter.'):
            gdown.download(url, output, quiet=False)
    
    df = pd.read_csv(output, low_memory=False)
    
    # Conversion de l'année en entier pour éviter les virgules dans les filtres
    if 'FIRE_YEAR' in df.columns:
        df['FIRE_YEAR'] = df['FIRE_YEAR'].astype(int)
        
    return df

# Chargement effectif du dataframe
df = load_data()

# --- 3. STRUCTURE DE L'INTERFACE ---

st.title("🔥 Analyse des Incendies aux USA (1992-2015)")

# Barre latérale pour la navigation
page = st.sidebar.radio("Navigation", ["Accueil", "Analyse Temporelle", "Analyse Météo", "Analyse de Sévérité"])

# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.write("### Bienvenue dans le projet d'analyse des Wildfires")
    st.write("""
    Ce dashboard interactif permet d'explorer les facteurs influençant les incendies de forêt.
    Nous avons croisé les données historiques du service forestier américain avec des données météo précises.
    """)
    
    st.info("Utilisez le menu à gauche pour naviguer entre l'analyse météo et les visualisations globales.")
    
    if st.checkbox("Afficher un aperçu des données brutes (10 premières lignes)"):
        st.dataframe(df.head(10))

# --- PAGE ANALYSE MÉTÉO (LUCIEN) ---
elif page == "Analyse Météo":
    st.header("🌦️ Influence des conditions Météo")
    
    # Dictionnaire des noms d'états
    state_mapping = {
        "Tous les États": "ALL",
        "California": "CA",
        "Georgia": "GA",
        "Texas": "TX",
        "North Carolina": "NC",
        "Florida": "FL"
    }
    
    # Filtre Global / Par État
    st.write("### Sélection du périmètre d'analyse")
    selected_full_name = st.selectbox(
        "Choisir la zone à analyser :", 
        options=list(state_mapping.keys())
    )
    
    # Logique du filtre global
    selected_abbrev = state_mapping[selected_full_name]
    if selected_abbrev == "ALL":
        # On ne garde que les lignes qui ont des données météo pour que les graphs soient cohérents
        df_filtered = df.dropna(subset=['temp_max', 'vent_max'])
        st.info("Affichage des statistiques globales (basé sur les 5 États du Top)")
    else:
        df_filtered = df[df['STATE'] == selected_abbrev]
        st.info(f"Analyse en cours pour : **{selected_full_name}**")
    
    st.divider()

    # DISTRIBUTION TEMPÉRATURE 
    col_top1, col_top2 = st.columns([2, 1]) 
    
    with col_top1:
        st.subheader("1. Fréquence selon la Température")
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.histplot(df_filtered['temp_max'], bins=30, kde=True, color='orange', edgecolor='black', ax=ax1)
        ax1.set_xlabel('Température Maximale (°C)')
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col_top2:
        st.write("### 🌡️ Facteur de chaleur")
        st.write("""
        La température est un **facteur de risque confirmé** : on observe une corrélation directe 
        entre l'augmentation des températures et le nombre de départs de feux. 
        C'est le moteur principal de l'inflammabilité de la végétation.
        """)

    st.divider()

    # --- LIGNE 2 : HEXBINS CÔTE À CÔTE ---
    st.subheader("2. Le rôle  du vent : Densité vs Taille")
    
    st.warning("""
    **Analyse :** Si la majorité des incendies se déclarent par temps calme (peu de vent), 
    le vent reste un facteur clé de dangerosité. On observe que les incendies les plus vastes 
    coïncident souvent avec des rafales plus importantes, car le vent permet une propagation 
    rapide et incontrôlable des flammes.
    """)

    col1, col2 = st.columns(2)

    with col1:
        # Graphique Densité
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        hb2 = ax2.hexbin(df_filtered['temp_max'], df_filtered['vent_max'], gridsize=25, cmap='YlOrRd', mincnt=1)
        fig2.colorbar(hb2, ax=ax2, label='Nombre de feux')
        ax2.set_title('Densité vs vent et tempéarture')
        ax2.set_xlabel('Température (°C)')
        ax2.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig2)

    with col2:
        # Graphique Sévérité
        df_plot = df_filtered.dropna(subset=['FIRE_SIZE_HECT'])
        fig3, ax3 = plt.subplots(figsize=(10, 7))
        hb3 = ax3.hexbin(df_plot['temp_max'],
                        df_plot['vent_max'],
                        C=df_plot['FIRE_SIZE_HECT'],
                        reduce_C_function=np.mean,
                        gridsize=25,
                        cmap='YlOrBr',
                        mincnt=1)
        fig3.colorbar(hb3, ax=ax3, label='Taille moy. (ha)')
        ax3.set_title('Taille vs vent et tempéarture')
        ax3.set_xlabel('Température (°C)')
        ax3.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig3)


# --- PAGE ANALYSE SEVERITE (ISMAIL) ---
elif page == "Analyse de Sévérité":
    st.write("### Analyse de la sévérité des feux")

    # 1️⃣ Distribution de la taille des feux (échelle log)
    st.subheader("Distribution de la taille des feux (échelle log)")
    fig = plt.figure(figsize=(10,5))
    sns.histplot(np.log10(df["FIRE_SIZE_HECT"] + 1), bins=50, color='orange')
    plt.xlabel("Log10(FIRE_SIZE_HECT + 1)")
    plt.ylabel("Nombre de feux")
    col1, col2 = st.columns([2,1])
    
    with col1:
        st.pyplot(fig)

    with col2:
        st.markdown("""
    ### 📌 Lecture du graphique
    
    La distribution est fortement asymétrique :
    - La majorité des incendies sont de petite taille.
    - Quelques feux très importants créent une longue "queue".
    
    L’échelle logarithmique permet de visualiser simultanément
    les petits et les très grands incendies.
    """)

    # 2️⃣ Nombre de feux par classe (A à G)
    st.subheader("Nombre de feux par classe (FIRE_SIZE_CLASS)")
    fig = plt.figure(figsize=(8,5))
    df['FIRE_SIZE_CLASS'].value_counts().sort_index().plot(kind='bar', color='green')
    plt.xlabel("Classe de taille (A à G)")
    plt.ylabel("Nombre de feux")
    plt.title("Répartition des classes de feux")
    st.pyplot(fig)
    col1, col2 = st.columns([2,1])
    st.markdown("""
    ### 📌 Lecture du graphique

    - Les classes A et B dominent largement en nombre.
    - Les grands feux (F, G) sont très rares.

    👉 La majorité des incendies restent localisés et contrôlables.
    """)

    # 3️⃣ Surface totale brûlée par classe de feu
    st.subheader("Surface totale brûlée par classe de feu")
    fig = plt.figure(figsize=(8,5))
    df.groupby('FIRE_SIZE_CLASS')['FIRE_SIZE_HECT'].sum().sort_index().plot(kind='bar', color='red')
    plt.xlabel("Classe de taille (A à G)")
    plt.ylabel("Total hectares brûlés")
    plt.title("Surface totale brûlée par classe de feu")
    st.pyplot(fig)
    st.markdown("""
    ### 📌 Lecture du graphique

    Bien que rares, les feux de classe F et G
    représentent la majorité des surfaces brûlées.

    👉 Ce ne sont pas les petits feux qui posent problème,
    mais les événements extrêmes.
    """)

    # 4️⃣ Tendance de la sévérité des feux par année
    st.subheader("Tendance de la sévérité des feux par année (médiane FIRE_SIZE_HECT)")
    fig = plt.figure(figsize=(12,6))
    sns.barplot(data=df, x='FIRE_YEAR', y='FIRE_SIZE_HECT', estimator='median', ci=None, color='purple')
    plt.xlabel("Année")
    plt.ylabel("Taille du feu (hectares)")
    plt.xticks(rotation=45)
    st.pyplot(fig)
    st.markdown("""
    ### 📌 Lecture du graphique

    La médiane annuelle varie selon les années.
    Certaines années présentent des incendies
    typiquement plus étendus.

    👉 Cela suggère une influence de facteurs annuels
    (climat, sécheresse, politiques de gestion).
    """)

    # 5️⃣ Distribution de la taille des feux par cause
    st.subheader("Distribution de la taille des feux par cause")
    fig = plt.figure(figsize=(12,6))
    sns.boxplot(x='STAT_CAUSE_DESCR', y='FIRE_SIZE_HECT', data=df)
    plt.yscale('log')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Cause du feu")
    plt.ylabel("Taille du feu (hectares, échelle log)")
    plt.title("Distribution de la taille des feux par cause")
    st.pyplot(fig)
    st.markdown("""
    ### 📌 Lecture du graphique

    - La médiane reste relativement similaire selon les causes.
    - Cependant, certaines causes (ex: foudre)
    présentent davantage d'incendies extrêmes.

    👉 La différence se situe surtout dans les valeurs extrêmes,
    pas dans les feux typiques.
    """)


# --- PAGE ANALYSE TEMPORELLE (SOPHIE) ---
elif page == "Analyse Temporelle":
    st.write("### Analyse temporelle des feux")
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    
    # 1️⃣ Evolution de la fréquence et taille des feux  par an
    st.subheader("Evolution de fréquence et de la la taille des feux  par an")
    st.warning("""
    **Analyse :** On constate une fréquence des feux par an globalement constante, mais avec des feux qui sont par contre de plus en plus sévères au fil du temps car de plus grande taille :
    """)
    
    df_year_size=df.groupby(["FIRE_YEAR"],as_index=False)["FIRE_SIZE_HECT"].sum()

    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Histogram(x        = df['FIRE_YEAR'],
                                   name = "fréquence des feux",
                                   marker_line = dict(width = 0.5, color = 'black')))


    fig.add_trace(go.Scatter(x        = df_year_size['FIRE_YEAR'],
                                 y        = df_year_size['FIRE_SIZE_HECT'],
                                 name = "Taille des feux",
                                 line=dict(color='black', width=4),
                                 marker_line = dict(width = 0.5, color = 'black')),
                      secondary_y=True,)

    fig.update_layout(title="Evolution de la fréquence et de la taille des feux par année",
                          width=1500,
                          height=500,
                          bargap=0.3)

    fig.update_xaxes(title_text="Année")

    fig.update_yaxes(title_text="Quantité de feux déclarés", secondary_y=False)
    fig.update_yaxes(title_text="Taille des feux en hectares", secondary_y=True)

    fig.show()

    st.plotly_chart(fig)

    # 2️⃣ Répartition des feux  par mois
    st.subheader("Répartition des feux  par mois")
    st.warning("""
    **Analyse :** Les feux de forêts ont lieu principalement au printemps et en été :
    """)

    df_month_qty=df.groupby(["DISCOVERY_MONTH"],as_index=False)["OBJECTID"].count()

    Bar_Month_Qty = px.bar(df_month_qty,
             x= 'DISCOVERY_MONTH',
             y = 'OBJECTID')

    Bar_Month_Qty.update_layout(title_text = "Fréquence des feux par mois cumulée sur les 23 années analysées",
                            xaxis_title  = "Mois",
                            yaxis_title = "Quantité de feux déclarés",
                            xaxis = dict(
                                tickmode = 'array',
                                tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                ticktext = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', "Aug", "Sept", "Oct", "Nov", "Dec"]))

    Bar_Month_Qty.show()
    st.plotly_chart(Bar_Month_Qty)


    st.warning("""
    **Analyse :** C'est en été que l'on a les feux les plus sévères en taille :
    """)

    df_month_size=df.groupby(["DISCOVERY_MONTH"],as_index=False)["FIRE_SIZE_HECT"].sum()
    df_month_size=df_month_size.sort_values(by='DISCOVERY_MONTH')

    Bar_Month_Size = go.Figure()

    Bar_Month_Size=px.bar(df_month_size,
             x = 'DISCOVERY_MONTH',
             y = 'FIRE_SIZE_HECT',
             color = 'FIRE_SIZE_HECT',
             color_continuous_scale=px.colors.sequential.Viridis_r)

    Bar_Month_Size.update_layout(title_text = "Somme des tailles des feux par mois sur les 23 années analysées",
                             xaxis_title  = "Mois",
                            yaxis_title = "Taille des feux en hectares",
                             legend_title = "Taille des feux en hectares",
                             xaxis = dict(
                                tickmode = 'array',
                                tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                ticktext = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', "Aug", "Sept", "Oct", "Nov", "Dec"]))

    Bar_Month_Size.show()
    st.plotly_chart(Bar_Month_Size)

    # 3️⃣ Analyse des causes par mois :
    st.subheader("Analyse des causes par mois")

    st.warning("""
    **Analyse :** Les causes principales diffèrent entre le printemps (Debris Burning) et l’été (Lightning):
    """)

    import plotly.express as px

    # map stat cause to a color
    c = dict(zip(df["STAT_CAUSE_DESCR"].unique(), px.colors.qualitative.T10))

    Rootcause_Month = px.histogram(df,
                                   x="DISCOVERY_MONTH",
                                  color='STAT_CAUSE_DESCR',
                                   barmode='group',
                                  height=600,
                                   color_discrete_map=c)
                                  #color_discrete_sequence=px.colors.qualitative.T10)

    Rootcause_Month.update_layout(title_text = "Fréquence des feux par rootcause par mois sur les 23 années analysées",
                             xaxis_title  = "Mois",
                            yaxis_title = "Fréquence des feux",
                             legend_title = "Rootcause des feux",
                             xaxis = dict(
                                tickmode = 'array',
                                tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                ticktext = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', "Aug", "Sept", "Oct", "Nov", "Dec"]))

    Rootcause_Month.show()
    st.plotly_chart(Rootcause_Month)

    st.write("Il est intéressant de constater d'autres saisonalités dans ce graph, comme par exemple les feux de forêt liés au feux d'artifice, si on ne sélectionne que cette cause sur le graph ci-dessous (en cliquant sur les élements de légende) on constate un pic en juillet à 6446 feux, ce qui reste malgré tout très faible au vu du nombre total de feux en juillet qui s'élève à plus de 237 000.")


    #4️⃣ Analyse cause par an
    st.subheader("Analyse des causes par an")

    df_year_cause_size=df.groupby(["FIRE_YEAR", "STAT_CAUSE_DESCR"],as_index=False ).agg({"FIRE_SIZE_HECT" : "sum", "OBJECTID" : "count"})
    df_year_cause_size=df_year_cause_size.sort_values(by= "FIRE_YEAR")


    st.warning("""
    **Analyse :** La hiérarchie au sein des causes est restée sensiblement la même au fil des années, on ne voit pas de causes qui disparaissent ou d'autres qui apparaissent avec le temps 
               et les causes principales sont « Debris Burning » suivi de « Arson » (incendie criminel) et « Lightning » (Orages) :
    """)
    c = dict(zip(df["STAT_CAUSE_DESCR"].unique(), px.colors.qualitative.T10))

    plt.figure(figsize=[180,200])
    year_cause_freq=px.line(df_year_cause_size,
                            x = "FIRE_YEAR",
                            y = "OBJECTID",
                            color = "STAT_CAUSE_DESCR",
                            color_discrete_map=c)

    year_cause_freq.update_layout(title='Evolution de la quantité de feux par rootcause et par an',
                                  xaxis_title='Année',
                                  yaxis_title='Quantité de feux',
                                  legend_title = "Rootcause des feux")

    year_cause_freq.show()
    st.plotly_chart(year_cause_freq)



    st.warning("""
    **Analyse :** L’évolution de ces causes en taille de feux suit l’augmentation des feux de forêt au fil des années, les orages (Lightning) étant la cause principale:
    """)


    plt.figure(figsize=[180,200])
    year_cause_size=px.line(df_year_cause_size,
                            x = "FIRE_YEAR",
                            y = "FIRE_SIZE_HECT",
                            color = "STAT_CAUSE_DESCR",
                            color_discrete_map=c)

    year_cause_size.update_layout(title='Evolution de la taille des feux par rootcause et par an',
                                  xaxis_title='Année',
                                  yaxis_title='Taille des feux en hectare',
                                  legend_title = "Rootcause des feux")

    year_cause_size.show()
    st.plotly_chart(year_cause_size)

# --- PAGE ANALYSE LOCALISATION (TIPHAINE) ---
elif page == "Analyse de par Localisation":

    # 1️⃣ Hectares brûlés par État
    df_state = df.groupby("STATE", as_index=False).agg({"FIRE_SIZE_HECT": "sum"})
    fig = px.choropleth(
        df_state,
        locations="STATE",
        locationmode="USA-states",
        color="FIRE_SIZE_HECT",
        scope="usa",
        color_continuous_scale="Reds",
        title="Hectares brûlés par État"
    )
    st.plotly_chart(fig)
    max_state = df_state.loc[df_state["FIRE_SIZE_HECT"].idxmax(), "STATE"]
    max_value = df_state["FIRE_SIZE_HECT"].max()
    st.markdown(f"""
    ### 📌 Lecture du graphique
    - L'État le plus touché est **{max_state}** avec **{int(max_value):,} hectares brûlés**.
    - Les autres États présentent des surfaces brûlées beaucoup plus faibles, illustrant la concentration des incendies.
    """)

    # 2️⃣ Cause principale des feux par État
    df_region = df.groupby(['STATE', 'STAT_CAUSE_DESCR'], as_index=False).size().rename(columns={'size':'count'})
    df_major_cause = df_region.loc[df_region.groupby('STATE')['count'].idxmax()]
    fig = px.choropleth(
        df_major_cause,
        locations='STATE',
        locationmode='USA-states',
        color='STAT_CAUSE_DESCR',
        scope='usa',
        title='Cause principale des feux par États'
    )
    st.plotly_chart(fig)
    st.markdown("""
    ### 📌 Lecture du graphique
    - Chaque État est coloré selon la cause la plus fréquente des incendies.
    - On peut identifier rapidement si la foudre, l’activité humaine ou d’autres causes dominent.
    """)

    # 3️⃣ Hectares brûlés par région
    df_zone = df.groupby("REGION", as_index=False)["FIRE_SIZE_HECT"].sum().sort_values("FIRE_SIZE_HECT", ascending=False)
    fig = px.bar(
        df_zone,
        x="REGION",
        y="FIRE_SIZE_HECT",
        text="FIRE_SIZE_HECT",
        title="Hectares brûlés par régions",
        labels={"FIRE_SIZE_HECT":"Hectares brûlés", "REGION":"Région"},
        color="FIRE_SIZE_HECT",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig)
    top_region = df_zone.iloc[0]
    st.markdown(f"""
    ### 📌 Lecture du graphique
    - La région la plus touchée est **{top_region['REGION']}** avec **{int(top_region['FIRE_SIZE_HECT']):,} hectares brûlés**.
    - Les autres régions ont des surfaces brûlées beaucoup moins importantes, ce qui montre la concentration géographique des feux.
    """)
    
    # 4️⃣ Durée moyenne des feux par État
    if pd.api.types.is_timedelta64_dtype(df['FIRE_DURATION']):
        df['FIRE_DURATION_DAYS'] = df['FIRE_DURATION'].dt.days
    else:
        df['FIRE_DURATION_DAYS'] = np.nan
        
    df_state_duration = df.groupby('STATE', as_index=False)['FIRE_DURATION_DAYS'].mean()
    fig = px.choropleth(
        df_state_duration,
        locations='STATE',
        locationmode='USA-states',
        color='FIRE_DURATION_DAYS',
        scope='usa',
        color_continuous_scale='YlOrBr',
        labels={'FIRE_DURATION_DAYS': 'Durée moyenne (jours)'},
        title='Durée moyenne des feux par État'
    )
    st.plotly_chart(fig)
    st.markdown("""
    ### 📌 Lecture du graphique
    - Chaque État est coloré selon la durée moyenne des feux.
    - Permet d’identifier les États où les incendies sont fréquents et prolongés.
    - Ces informations sont utiles pour la planification et la prévention.
    """)







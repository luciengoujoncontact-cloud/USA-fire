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
    df=df.sort_values("FIRE_SIZE_HECT", ascending = False)
    
    # Conversion de l'année en entier pour éviter les virgules dans les filtres
    if 'FIRE_YEAR' in df.columns:
        df['FIRE_YEAR'] = df['FIRE_YEAR'].astype(int)
        
    return df

# Chargement effectif du dataframe
df = load_data()

# --- 3. STRUCTURE DE L'INTERFACE ---

st.title("🔥 Analyse des feux de forêt aux Etats-Unis (1992-2015)")

# Barre latérale pour la navigation
st.sidebar.image("dessin feux foret.webp", use_container_width=True)
page = st.sidebar.radio("Navigation", ["Accueil", "Analyse temporelle", "Analyse de sévérité", "Analyse géographique", "Analyse météorologique", "Conclusion"])
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")
st.sidebar.markdown(""" \n""")


st.sidebar.markdown("""
                    <p style="line-height: 1.2; margin: 0;">Qui sommes nous ? </p>
                    <p style="line-height: 1.2; margin: 0;">🔥 Sophie BENCHAA</p>
                    <p style="line-height: 1.2; margin: 0;">🔥 Tiphaine BIHOUR</p>
                    <p style="line-height: 1.2; margin: 0;">🔥 Ismaïl BOUAZIZI</p>
                    <p style="line-height: 1.2; margin: 0;">🔥 Lucien GOUJON</p>
                    """, unsafe_allow_html=True)

st.sidebar.image("Liora.png", width=80)
st.markdown("""
    <style>
    [data-testid="stSidebar"] [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)
# --- PAGE ACCUEIL ---
if page == "Accueil":
    st.write("### Bienvenue dans le projet d'analyse des feux de forêt aux Etats-Unis")
    st.write("""
    Ce dashboard interactif permet d'explorer les facteurs influençant les incendies de forêt.\n
    """)
    
        # --- 1. Synthèse par axes ---
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("📋 Les données sources")
        st.write("""
        - Nous avons analysé les données historiques des services forestiers américains recensant les feux pendant 23 ans : entre 1992 et 2015.
        - Le dataset source de notre travail contient les caractéristiques de 1 880 465 feux sur cette période.
        - Ces données sont en libre accès sur la plateforme Kaggle.
        """)

    with col_c2:
        st.subheader("📊 Notre travail")
        st.write("""
        - Nous avons selectionné, nettoyé et transformé ces données pour les rendre exploitables.
        - Initialement consitué de 39 colonnes caractérisant les feux, nous n'en avons selectionné que 21 pertinentes pour l'analyse.
        - En effet certaines étaient redondantes entre elles, ou trop incomplètes pour être utiles à notre analyse.
        - Nous avons ensuite ajouté 3 colonnes contenant les données météorologiques (température, vitesse du vent et pluie) associées aux principaux Etats touchés par les feux.
        - Nous avons mené l'exploration suivant quatre axes : l'axe temporel, de sévérité, géographique et météorologique.
        """)

    st.divider()

    st.subheader("""
    **🔍 Bonne lecture !**\n
    """)

    st.info("Utilisez le menu à gauche pour naviguer entre les différents axes d'analyse.")
    
    if st.checkbox("Afficher un aperçu des données sur les 10 premières lignes, correspondant aux 10 plus grands feux"):
        st.dataframe(df.head(10))


# --- PAGE ANALYSE MÉTÉO (LUCIEN) ---

elif page == "Analyse météorologique":
    st.write("## 🌦️ Influence des conditions météorologiques")
    
    st.write("""
    Cette section explore comment les variables atmosphériques dictent le rythme des incendies. 
    L'analyse se concentre sur les 5 États les plus critiques pour garantir une corrélation précise entre les départs de feux et les relevés d'Open-Meteo.
    """)

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
    st.subheader("Périmètre d'observation")
    selected_full_name = st.selectbox(
        "Sélectionner une zone géographique :", 
        options=list(state_mapping.keys())
    )
    
    # Logique du filtre
    selected_abbrev = state_mapping[selected_full_name]
    if selected_abbrev == "ALL":
        df_filtered = df.dropna(subset=['temp_max', 'vent_max', 'pluie_mm'])
    else:
        df_filtered = df[df['STATE'] == selected_abbrev]

    # --- KPI ---
    st.write(f"### État des lieux : {selected_full_name}")
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        st.metric("Température Moy.", f"{df_filtered['temp_max'].mean():.1f} °C")
    with col_kpi2:
        st.metric("Vent Moyen", f"{df_filtered['vent_max'].mean():.1f} km/h")
    with col_kpi3:
        st.metric("Précip. Moyennes", f"{df_filtered['pluie_mm'].mean():.2f} mm")
    with col_kpi4:
        st.metric("Total Incendies", f"{len(df_filtered):,}")

    st.divider()

    # --- 1. TEMPÉRATURE ET HUMIDITÉ (PLUIE) ---
    st.subheader("\n 1. Quels sont les impacts combinés de la chaleur et de l'humidité sur l'éclosion des feux ?")
    
    col_top1, col_top2 = st.columns([2, 1]) 
    cmap = plt.get_cmap('YlOrRd')
    couleur_feu = cmap(0.6)
    
    with col_top1:
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        
        # Axe 1 : Température
        sns.histplot(df_filtered['temp_max'], bins=30, kde=True, color=couleur_feu, label='Température (°C)', ax=ax1)
        ax1.set_xlabel('Température Maximale (°C)')
        ax1.set_ylabel('Nombre d\'incendies')

        # Axe 2 : Pluie (Indicateur d'humidité)
        ax1_twin = ax1.twinx()
        sns.kdeplot(df_filtered['pluie_mm'], color='blue', fill=True, ax=ax1_twin, label='Précipitations (mm)')
        ax1_twin.set_ylabel('Densité d\'absence d\'humidité (Pluie)')
        
        # Légende unique
        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax1_twin.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper right')
        
        plt.tight_layout()
        st.pyplot(fig1)
    
    with col_top2:
        st.write("\n" * 2) 
        st.write("""
        ###### 📌 Réponse visuelle : 
        - **Le seuil critique :** On observe une explosion du nombre de feux dès que la température dépasse les **25°C**.
        - **Le facteur humidité :** La courbe bleue montre que la densité d'incendies est maximale quand les précipitations sont à **0mm**. 
        - **Conclusion :** Le stress hydrique de la végétation (basse humidité) combiné à une forte chaleur constitue le "cocktail explosif" idéal pour le départ d'un feu.
        """)

    st.divider()

    # --- 2. LE VENT ET LA SÉVÉRITÉ ---
    st.subheader("\n 2. Comment le vent transforme-t-il un départ de feu en catastrophe majeure ?")
    
    st.write("""
    L'analyse croisée ci-dessous permet de distinguer deux phénomènes : ce qui crée le feu (la chaleur) et ce qui le propage (le vent).
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig2, ax2 = plt.subplots(figsize=(10, 7))
        hb2 = ax2.hexbin(df_filtered['temp_max'], df_filtered['vent_max'], gridsize=25, cmap='YlOrRd', mincnt=1)
        fig2.colorbar(hb2, ax=ax2, label='Nombre de feux')
        ax2.set_title('Fréquence : Où naissent les feux ?', fontstyle='italic')
        ax2.set_xlabel('Température (°C)')
        ax2.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig2)

    with col2:
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
        ax3.set_title('Sévérité : Quels feux deviennent incontrôlables ?', fontstyle='italic')
        ax3.set_xlabel('Température (°C)')
        ax3.set_ylabel('Vent (km/h)')
        plt.tight_layout()
        st.pyplot(fig3)

    st.markdown("""
    ###### 📌 Réponse visuelle : 
    - **Le vent, moteur de propagation :** Si le premier graphique montre que beaucoup de feux naissent par vent faible, le second révèle que les **incendies les plus vastes** (en sombre) surviennent lorsque le vent forcit.
    - **L'effet couloir :** Un vent soutenu (> 20-30 km/h) couplé à une forte température empêche l'extinction rapide et favorise les sautes de feu.
    """)
# --- PAGE ANALYSE SEVERITE (ISMAIL) OPTIMISÉE ---
elif page == "Analyse de sévérité":
    import plotly.io as pio
    import streamlit.components.v1 as components
    import plotly.express as px
    st.write("## Analyse de sévérité des feux")

    # --- Graphiques et affichage rapide via HTML pour accélérer ---
    def st_plotly_fast(fig, height=500):
        """Affiche un graphique Plotly via HTML pour réduire la surcharge Streamlit"""
        components.html(pio.to_html(fig, include_plotlyjs='cdn', full_html=False), height=height)

    # --- Explication des classes de feux ---
    st.markdown("#### 📌 Classement des feux par taille")
    colA, colB = st.columns(2)
    with colA:
        st.markdown("""
        **Classes A à D**  
        - **A :** 0 – 1 000 m² (~0 – 0,1 ha)  
        - **B :** 1 001 – 40 000 m² (~0,1 – 4 ha)  
        - **C :** 4 – 40 ha  
        - **D :** 40 – 120 ha
        """)
    with colB:
        st.markdown("""
        **Classes E à G**  
        - **E :** 120 – 400 ha  
        - **F :** 400 – 2 000 ha  
        - **G :** > 2 000 ha
        """)

    # --- Mise en page côte à côte pour les deux premiers graphes ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("1. Nombre de feux par classe")
        df_class = df['FIRE_SIZE_CLASS'].value_counts().sort_index().reset_index()
        df_class.columns = ['FIRE_SIZE_CLASS','count']
        fig2 = px.bar(
            df_class,
            x='FIRE_SIZE_CLASS',
            y='count',
            color_discrete_sequence=['rgb(254,178,76)']
        )
        st_plotly_fast(fig2, height=400)
        st.markdown("""
        ### 📌 Lecture du graphique
        - Les petites classes (A, B, C) représentent le plus grand nombre de feux.
        - Les classes D à G sont moins fréquentes, mais leur impact sur la surface totale brûlée est important.
        """)

    with col2:
        st.subheader("2. Surface totale brûlée par classe")
        df_sum = df.groupby('FIRE_SIZE_CLASS')['FIRE_SIZE_HECT'].sum().sort_index().reset_index()
        fig3 = px.bar(
            df_sum,
            x='FIRE_SIZE_CLASS',
            y='FIRE_SIZE_HECT',
            color_discrete_sequence=['rgb(254,178,76)']
        )
        st_plotly_fast(fig3, height=400)
        st.markdown("""
        ### 📌 Lecture du graphique
        - Les classes F et G, bien que rares, représentent la majorité de la surface brûlée.
        - Les classes A à D contribuent peu à la surface totale malgré leur fréquence.
        """)

    # 3️⃣ Tendance de la sévérité par année
    st.subheader("3. Tendance annuelle de la taille médiane des feux")
    df_year = df.groupby('FIRE_YEAR')['FIRE_SIZE_HECT'].median().reset_index()
    fig4 = px.line(
        df_year,
        x='FIRE_YEAR',
        y='FIRE_SIZE_HECT',
        markers=True,
        line_shape='linear',
        color_discrete_sequence=['rgb(128,0,38)']
    )
    st_plotly_fast(fig4, height=400)
    st.markdown("""
    ### 📌 Lecture du graphique
    - La taille médiane des feux reste globalement stable entre 0,2 et 0,4 ha sur la période 1992–2015.
    - Cela indique que la plupart des incendies sont de petite taille et sont rapidement maîtrisés.
    - Les variations selon les années peuvent s’expliquer par les conditions climatiques ou la gestion des feux.
    """)

    # 4️⃣ Distribution des causes par taille de feu
    st.subheader("4. Distribution des causes par taille de feu")
    fig5 = px.box(
        df,
        x='STAT_CAUSE_DESCR',
        y='FIRE_SIZE_HECT',
        log_y=True,
        color='STAT_CAUSE_DESCR',
        color_discrete_sequence=px.colors.qualitative.T10
    )
    st_plotly_fast(fig5, height=450)
    st.markdown("""
    ### 📌 Lecture du graphique
    - La majorité des feux sont de petite taille, indépendamment de la cause.
    - Certaines causes (foudre, brûlage de débris, diverses causes) peuvent générer des incendies exceptionnellement grands.
    - La distribution est très asymétrique : la plupart des feux restent petits, mais les outliers peuvent avoir un impact significatif.
    - Ces points extrêmes doivent être pris en compte pour la planification et la prévention, car ils représentent les feux les plus destructeurs.
    """)

    st.subheader("\n -> Maintenant qu'on a vu la sévérité selon la taille et la cause : quelles régions concentrent ces incendies ? ")

elif page == "Analyse temporelle":
    st.write("## Analyse temporelle des feux")
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # 1️⃣ Evolution de la fréquence et taille des feux  par an
    st.subheader("\n 1. Comment ont évolué le nombre et la taille des feux au fil des années ? ")
    st.write("""
    Nous possédons pour chaque feu de la base de données, sa date de déclaration ainsi que sa taille. \n
    Nous pouvons donc analyser l'évolution de la fréquence et de la taille des feux sur l'intégralité des vingt-trois années de données : 
    """) 

    #création d'un df taille par an :
    df_year_size=df.groupby(["FIRE_YEAR"],as_index=False)["FIRE_SIZE_HECT"].sum()

    #création du visuel histogram à partir de ce df :

    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Histogram(x        = df['FIRE_YEAR'],
                                    name = "Fréquence des feux",
                                   marker_color =  'rgb(254,178,76)',
                                   ))
    fig.add_trace(go.Scatter(x        = df_year_size['FIRE_YEAR'],
                                 y        = df_year_size['FIRE_SIZE_HECT'],
                                 name = "Taille des feux",
                                 line=dict(color='rgb(128,0,38)', width=4),
                                 marker_line = dict(width = 0.5, color = 'black')),
                      secondary_y=True,)
    fig.update_layout(title_text = "Evolution de la fréquence et de la taille des feux par année",
                      title_font_style= "italic",
                      width=1500,
                          height=500,
                          bargap=0.3)
    # Set x-axis title
    fig.update_xaxes(title_text="Année")
    # Set y-axes titles
    fig.update_yaxes(title_text="Quantité de feux déclarés", secondary_y=False)
    fig.update_yaxes(title_text="Taille des feux en hectares", secondary_y=True)
    # affichage du visuel :
    fig.show()
    st.plotly_chart(fig)

    st.write("""
    ###### 📌 Analyse : 
    - On constate une fréquence des feux par an globalement constante
    - En revanche les feux sont de plus en plus sévères au fil du temps, la surface brulée suit une courbe en croissance.
    \n \n """)

    

    # 2️⃣ Répartition des feux  par mois
    st.subheader("\n 2. Y a t-il des mois qui concentrent le plus de feux ?")

    df_month_qty=df.groupby(["DISCOVERY_MONTH"],as_index=False)["OBJECTID"].count()

    Bar_Month_Qty = px.bar(df_month_qty,
             x= 'DISCOVERY_MONTH',
             y = 'OBJECTID')
    Bar_Month_Qty.update_traces(marker_color='rgb(254,178,76)')
    Bar_Month_Qty.update_layout(title_text = "Fréquence des feux par mois cumulée sur les 23 années analysées",
                            xaxis_title  = "Mois",
                            yaxis_title = "Quantité de feux déclarés",
                            xaxis = dict(
                                tickmode = 'array',
                                tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                ticktext = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', "Aug", "Sept", "Oct", "Nov", "Dec"]))

    Bar_Month_Qty.show()
    st.plotly_chart(Bar_Month_Qty)

    st.markdown("""
    ###### 📌 Analyse :  
    On constate deux saisons principales pour l'apparition des feux de forêt : 
    - Au printemps (mars/avril)
    - En été (juillet/aout)
     \n \n   """)

    st.subheader("\n 3. Est-ce que cette périodicité mensuelle est la même si on regarde la taille des feux ?")
    df_month_size=df.groupby(["DISCOVERY_MONTH"],as_index=False)["FIRE_SIZE_HECT"].sum()
    df_month_size=df_month_size.sort_values(by='DISCOVERY_MONTH')

    Bar_Month_Size = go.Figure()

    Bar_Month_Size=px.bar(df_month_size,
             x = 'DISCOVERY_MONTH',
             y = 'FIRE_SIZE_HECT',
             color = 'FIRE_SIZE_HECT',
             color_continuous_scale=px.colors.sequential.YlOrRd)

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

    st.markdown("""
    ###### 📌 Analyse : 
    Il est flagrant de constater que c'est seulement l'été que l'on trouve les feux de plus grande taille.
    \n \n """)

    # 3️⃣ Analyse des causes par mois :
    st.subheader("4. Quelles sont les principales causes pour chaque mois ?")
 

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

    Rootcause_Month.update_layout(title_text = "Fréquence des feux par cause par mois sur les 23 années analysées",
                             xaxis_title  = "Mois",
                            yaxis_title = "Fréquence des feux",
                             legend_title = "Rootcause des feux",
                             xaxis = dict(
                                tickmode = 'array',
                                tickvals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                                ticktext = ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', "Aug", "Sept", "Oct", "Nov", "Dec"]))

    Rootcause_Month.show()
    st.plotly_chart(Rootcause_Month)

    st.markdown("""
    ###### 📌 Analyse : 
    Les causes principales diffèrent suivant les saisons : 
    - Au printemps : Déchets brulés (Debris Burning)
    - En été : Orages (Lightning)
    \n """)

    st.warning("""
    **Pour compléter :** Il est intéressant de constater d'autres saisonalités dans ce visuel.
               Par exemple les feux de forêt liés au feux d'artifice :
               Si on ne sélectionne que cette cause sur le visuel ci-dessus (en cliquant sur les élements de légende) on constate un pic en juillet à 6446 feux, ce qui reste malgré tout très faible au vu du nombre total de feux en juillet qui s'élève à plus de 237 000.
               """)


    #4️⃣ Analyse cause par an
    st.subheader("5. Est-ce qu'au fil du temps la hiérarchie des causes a évolué ?")

    df_year_cause_size=df.groupby(["FIRE_YEAR", "STAT_CAUSE_DESCR"],as_index=False ).agg({"FIRE_SIZE_HECT" : "sum", "OBJECTID" : "count"})
    df_year_cause_size=df_year_cause_size.sort_values(by= "FIRE_YEAR")

    c = dict(zip(df["STAT_CAUSE_DESCR"].unique(), px.colors.qualitative.T10))

    plt.figure(figsize=[180,200])
    year_cause_freq=px.line(df_year_cause_size,
                            x = "FIRE_YEAR",
                            y = "OBJECTID",
                            color = "STAT_CAUSE_DESCR",
                            color_discrete_map=c)

    year_cause_freq.update_layout(title='Evolution de la quantité de feux par cause et par an',
                                  xaxis_title='Année',
                                  yaxis_title='Quantité de feux',
                                  legend_title = "Rootcause des feux")

    year_cause_freq.show()
    st.plotly_chart(year_cause_freq)

    st.markdown("""
    ###### 📌 Analyse : 
    - La hiérarchie au sein des causes est restée sensiblement la même au fil des années.
    - On ne voit pas de causes qui disparaissent ou d'autres qui apparaissent avec le temps.
    - Les causes principales sont « Debris Burning » suivi de « Arson » (incendie criminel) et « Lightning » (Orages).
    \n \n """)

    st.subheader("6. Et si on regarde la taille de feux, qu'en est-il de cette hiérarchie des causes au fil du temps ?")


    plt.figure(figsize=[180,200])
    year_cause_size=px.line(df_year_cause_size,
                            x = "FIRE_YEAR",
                            y = "FIRE_SIZE_HECT",
                            color = "STAT_CAUSE_DESCR",
                            color_discrete_map=c)

    year_cause_size.update_layout(title='Evolution de la taille des feux par cause et par an',
                                  xaxis_title='Année',
                                  yaxis_title='Taille des feux en hectare',
                                  legend_title = "Rootcause des feux")

    year_cause_size.show()
    st.plotly_chart(year_cause_size)
    
    st.markdown("""
    ###### 📌 Analyse : 
    - L’évolution de ces causes en taille de feux suit l’augmentation des feux de forêt au fil des années.
    - Les orages (Lightning) sont la cause principale des grands feux d'été.
    \n \n """)


    st.subheader("\n -> Nous savons désormais quand et pourquoi interviennent les plus grands feux. \n ### Et si nous analysions maintenant plus précisemment la taille des feux ? ")




# --- PAGE ANALYSE LOCALISATION (TIPHAINE) ---
elif page == "Analyse géographique":
    st.write("## Analyse géographique des feux")

    # 1️⃣ Hectares brûlés par région
    st.subheader("\n 1. Quelles sont les régions les plus touchées ?")

    df_zone = df.groupby("REGION", as_index=False)["FIRE_SIZE_HECT"].sum().sort_values("FIRE_SIZE_HECT", ascending=False)
    fig = px.bar(
        df_zone,
        x="REGION",
        y="FIRE_SIZE_HECT",
        text="FIRE_SIZE_HECT",
        labels={"FIRE_SIZE_HECT":"Hectares brûlés", "REGION":"Région"},
        color="FIRE_SIZE_HECT",
        color_continuous_scale="YlOrRd"
    )
    st.plotly_chart(fig)
    top_region = df_zone.iloc[0]
    st.markdown("""
    ###### 📌 Analyse : 
    - La région la plus touchée est la région Ouest avec environ 43 millions d'hectares brûlés. 
    - Les autres régions ont des surfaces brûlées beaucoup moins importantes, ce qui montre la concentration géographique des feux.
    """)

    # 2️⃣ Hectares brûlés par État
    st.subheader("\n 2. Quels sont les États les plus touchés ?")

    df_state = df.groupby("STATE", as_index=False).agg({"FIRE_SIZE_HECT": "sum"})
    fig = px.choropleth(
        df_state,
        locations="STATE",
        locationmode="USA-states",
        color="FIRE_SIZE_HECT",
        scope="usa",
        color_continuous_scale="YlOrRd",
    )
    st.plotly_chart(fig)
    max_state = df_state.loc[df_state["FIRE_SIZE_HECT"].idxmax(), "STATE"]
    max_value = df_state["FIRE_SIZE_HECT"].max()
    st.markdown("""
    ###### 📌 Analyse : 
    - L'État le plus touché est L'Alaska avec 13 Millions d'hectares brûlés. 
    - Les autres États présentent des surfaces brûlées beaucoup plus faibles, ce qui montre la concentration des incendies.
    """)

    # 3️⃣ Cause principale des feux par État
    st.subheader("\n 3. Quelles sont les causes principales des feux par État ?")

    c = dict(zip(df["STAT_CAUSE_DESCR"].unique(), px.colors.qualitative.T10))
    df_region = df.groupby(['STATE', 'STAT_CAUSE_DESCR'], as_index=False).size().rename(columns={'size':'count'})
    df_major_cause = df_region.loc[df_region.groupby('STATE')['count'].idxmax()]
    fig = px.choropleth(
        df_major_cause,
        locations='STATE',
        locationmode='USA-states',
        color='STAT_CAUSE_DESCR',
        scope='usa',
        color_discrete_map=c,
    )
    st.plotly_chart(fig)
    st.markdown("""
    ###### 📌 Analyse : 
    - Chaque État est coloré selon la cause la plus fréquente des incendies. 
    - On peut identifier rapidement que la foudre et l'activité humaine (avec Debris burning) sont les causes principales.
    """)
    
    # 4️⃣ Durée moyenne des feux par État
    st.subheader("\n 4. Quelle est la durée moyenne des feux par État ?")

    df['FIRE_DURATION'] = pd.to_timedelta(df['FIRE_DURATION'], errors='coerce')
    df['FIRE_DURATION_DAYS'] = df['FIRE_DURATION'].dt.total_seconds() / (24*3600)
    df['FIRE_DURATION_DAYS'] = df['FIRE_DURATION_DAYS'].fillna(0)

    df_state_duration = df.groupby('STATE', as_index=False)['FIRE_DURATION_DAYS'].mean()

    fig = px.choropleth(
    df_state_duration,
    locations='STATE',
    locationmode='USA-states',
    color='FIRE_DURATION_DAYS',
    scope='usa',
    color_continuous_scale='YlOrRd',
    labels={'FIRE_DURATION_DAYS': 'Durée moyenne (jours)'},
    title='Durée moyenne des feux par État'
    )
    st.plotly_chart(fig)

    st.markdown("""
    ###### 📌 Analyse : 
    - Chaque État est coloré selon la durée moyenne des feux. 
    - Cela nous permet d’identifier les États où les incendies sont fréquents et prolongés. 
    - Ces informations sont utiles pour la planification et la prévention.
    """)

    st.subheader("\n 5. Quelle est la répartition géographique des forêts et déserts aux USA ?")

    image_path = os.path.join(os.path.dirname(__file__), "cartographieusa.jpg")

    # Affichage de l'image avec largeur maximale
    st.image(image_path, caption="https://super-duper.fr/country/usa.php", width=800)
    
    st.markdown("""
    ###### 📌 Analyse : 
    - Cette carte nous montre la répartition géographique des forêts aux États-Unis
    - Cela qui nous permet de visualiser les zones les plus vulnérables aux incendies.
    """)

    st.subheader("\n 6. Quelle est la cartographie des climats des USA ?")

    image_path = os.path.join(os.path.dirname(__file__), "https://www.climatsetvoyages.com/cllmat/etats-unis")

    # Affichage de l'image avec largeur maximale
    st.image(image_path, caption="https://www.climatsetvoyages.com/cllmat/etats-unis", width=800)
    
    st.markdown("""
    ###### 📌 Analyse : 
    - Cette carte permet de visualiser les différents climats aux États-Unis 
    - Cela  les conditions météorologiques qui influencent la propagation des incendies.
    """)

    st.subheader("\n ->  Nous pouvons maintenant nous demander si les conditions météorologiques jouent un rôle dans la localisation des feux de forêt ?")


    
    # --- PAGE CONCLUSION ---
elif page == "Conclusion":
    st.header("🏁 Conclusion Générale du Projet")

    st.write("""
    Ce projet d’analyse des incendies aux États-Unis (1992-2015) nous a permis de transformer un dataset massif de **1,88 million de lignes** en une plateforme décisionnelle interactive. 
    L'approche multidimensionnelle adoptée par l'équipe révèle que la lutte contre les feux de forêt ne peut être efficace qu'en croisant les facteurs temporels, géographiques et météorologiques.
    """)

    # --- 1. Synthèse par axes ---
    col_c1, col_c2 = st.columns(2)

    with col_c1:
        st.subheader("📍 Dynamique Géographique et Sévérité")
        st.write("""
        - **Localisation :** L'analyse  a montré une disparité flagrante : si le Sud est la région la plus souvent touchée en nombre de départs, l'**Ouest américain (et l'Alaska)** concentre l'essentiel des surfaces dévastées.
        - **Sévérité :** L'étude souligne la loi du "90/10" : 90% des feux sont maîtrisés rapidement (Classes A-B), mais moins de 1% des feux (Classe G) causent plus de 80% des dégâts totaux.
        """)

    with col_c2:
        st.subheader("🌦️ Facteurs Climatiques et Temporels")
        st.write("""
        - **Temporalité :** L'analyse confirme une saisonnalité critique en **juillet et août**, période où les ressources de lutte doivent être à leur maximum.
        - **Météo (Le duo fatal) :** L'étude démontre que la **température** élevée est le "détonateur" (éclosion), tandis que la vitesse du **vent** est le véritable "propagateur" (sévérité). L'absence de pluie est la condition sine qua non de ces catastrophes.
        """)

    st.divider()

    # --- 2. Apports du Dashboard ---
    st.subheader("🚀 L'apport de l'outil Streamlit")
    st.success("""
    L'interactivité de ce tableau de bord, notamment grâce aux **filtres dynamiques par État**, permet de sortir des statistiques globales pour effectuer un **drill-down** localisé. 
    C'est un outil précieux pour :
    1. **Anticiper** les besoins en ressources selon les prévisions météo.
    2. **Cibler** les campagnes de prévention selon les causes majoritaires identifiées par État (ex: foudre vs activité humaine).
    """)

    # --- 3. Ouverture ---
    st.info("""
    **Perspectives :** Ce projet pourrait évoluer vers une dimension prédictive. En intégrant des modèles de **Machine Learning**, l'application pourrait estimer en temps réel le risque de propagation d'un nouveau foyer dès son signalement, en fonction des données vent/température/humidité du jour.
    """)

    # Crédits finaux
    st.markdown("---")
    st.markdown("<center>Projet réalisé dans le cadre de la formation Data Analyst - 2025</center>", unsafe_allow_html=True)

# Potion Craft - Tableau de Bord d'Analyse

Bienvenue sur **Potion Craft**, une application interactive développée avec **Streamlit** et **Plotly** dans le cadre du cours Python de la formation CDAN. Ce projet permet d'analyser, de transformer et de visualiser des données complexes autour de la fabrication de potions magiques, des ingrédients, des compétences et de la rentabilité.



L'application est également accessible sur le web en <a href="https://igensia.streamlit.app"> cliquant ici</a>.

---

## Fonctionnalités & Visualisations

L'application propose un tableau de bord complet comprenant :
* **Histogramme des potions rentables** : Analyse comparative de la rentabilité des différentes potions.
* **Heatmap des ingrédients** : Visualisation des co-occurrences et relations entre les ingrédients.
* **Diagramme de Kiviat (Radar)** : Évaluation multi-critères des compétences et caractéristiques.
* **Sunburst (Diagramme Solaire)** : Exploration hiérarchique sur 3 niveaux des potions et de leur composition.
* **Graphe de Réseau** : Représentation interactive des connexions et des relations.
* **Détection d'anomalies** : Audit automatique du jeu de données pour identifier et lister les incohérences par feuille.

---

## Stack Technique & Bibliothèques

Ce projet repose entièrement sur **Python** et utilise les librairies suivantes :
* **[Streamlit](https://streamlit.io/)** : Framework pour la création de l'application web interactive et du tableau de bord.
* **[Plotly](https://plotly.com/)** : Génération des graphiques interactifs (histogrammes, heatmaps, radars, sunbursts, graphes de réseau).
* **[Pandas](https://pandas.pydata.org/)** & **[NumPy](https://numpy.org/n)** : Manipulation, nettoyage et transformation des données tabulaires.
* **[NetworkX](https://networkx.org/)** : Analyse et modélisation des graphes et des réseaux d'ingrédients.

---

## Arborescence du Projet

```text
root/
│
├── main.py                  # Point d'entrée principal de l'application Streamlit
├── requirements.txt         # Liste des dépendances Python du projet
├── README.md                # Documentation du projet
├── potion-craft.pdf         # Directives concernant le projet et le livrable
│
├── data/
│   ├── processed_csv/       # Fichiers CSV générés et utilisés par les visualisations
│   │   ├── ingredients_cooccurrence.csv
│   │   ├── nb_potions_par_competence.csv
│   │   ├── network_edges.csv
│   │   ├── network_nodes.csv
│   │   ├── potions_plus_rentables.csv
│   │   └── sunburst_potions.csv
│   └── potions-craft.xlsx   # Fichier source donné par l'académie 
│
├── graphs/                  # Modules de génération des graphiques Plotly
│   ├── heatmap.py
│   ├── histogramme.py
│   ├── kiviat.py
│   ├── network.py
│   └── sunburst.py
│
└── scripts/                 # Scripts de traitement des données et d'analyse
    ├── anomalies.py
    ├── traitement_heatmap.py
    ├── traitement_histogramme.py
    ├── traitement_inventeurs.py
    └── traitement_sunburst.py
```

---

## Installation et Lancement

### Créer un environnement virtuel

```
py -m venv .venv
```

### Activer l'environnement virtuel

Pour Windows :
```
.venv\scripts\activate
```

Pour Linux:
```
source .venv/bin/activate
```

### Récupérer les dépendances

```
pip install -r requirements.txt
```

### Lancer l'application (en local)

```
streamlit run main.py
```
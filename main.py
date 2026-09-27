import streamlit as st
from graphs.histogramme import create_histogram
from graphs.heatmap import create_heatmap
from graphs.network import create_network_graph
from pathlib import Path

st.set_page_config(page_title="Potion craft", layout="wide")
st.title("Potion craft")

# Affichage de l'histogramme
st.plotly_chart(create_histogram(), width='stretch')

# Affichage de la heatmap
st.plotly_chart(create_heatmap(), width='stretch')

# Affichage du graphe réseau (sans filtres)
DATA_DIR = Path("data") / "processed_csv"
NODES_CSV = DATA_DIR / "network_nodes.csv"
EDGES_CSV = DATA_DIR / "network_edges.csv"

if NODES_CSV.exists() and EDGES_CSV.exists():
    fig_network = create_network_graph()
    st.plotly_chart(fig_network, width='stretch')
else:
    st.warning('Les fichiers data/processed_csv/network_nodes.csv et network_edges.csv sont manquants. Lancez scripts/process_potions.py pour les générer.')
import streamlit as st
from graphs.histogramme import create_histogram
from graphs.heatmap import create_heatmap

st.set_page_config(page_title="Potion craft", layout="wide")
st.title("Potion craft")

# Affichage de l'histogramme
st.plotly_chart(create_histogram(), width='stretch')

# Affichage de la heatmap
st.plotly_chart(create_heatmap(), width='stretch')
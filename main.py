import streamlit as st
from graphs.histogramme import create_histogram
st.set_page_config(page_title="Potion craft", layout="wide")
st.title("Potion craft")
st.plotly_chart(create_histogram(), use_container_width=True)
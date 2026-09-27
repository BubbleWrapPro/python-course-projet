import streamlit as st
from pathlib import Path
from zipfile import BadZipFile

from graphs.histogramme import create_histogram
from graphs.heatmap import create_heatmap
from graphs.network import create_network_graph
from scripts.traitement_histogramme import prepare_histogram
from scripts.traitement_heatmap import prepare_heatmap_data
from scripts.tratiement_inventeurs import generate_network_csv_files

st.set_page_config(page_title="Potion craft", layout="wide")
st.title("Potion craft")

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "processed_csv"
REQUIRED_CSVS = (
    DATA_DIR / "potions_plus_rentables.csv",
    DATA_DIR / "ingredients_cooccurrence.csv",
    DATA_DIR / "network_nodes.csv",
    DATA_DIR / "network_edges.csv",
)

# Generate the CSV files used by the charts before loading them.
try:
    prepare_histogram()
    prepare_heatmap_data()
    generate_network_csv_files()
except (BadZipFile, IndexError, KeyError, OSError, TypeError, ValueError) as error:
    missing_csvs = [path.name for path in REQUIRED_CSVS if not path.is_file()]
    if missing_csvs:
        st.error(
            f"CSV generation failed: {error}. "
            f"Cannot display the charts; missing: {', '.join(missing_csvs)}."
        )
        can_display_charts = False
    else:
        st.warning(
            f"CSV generation failed: {error}. "
            "Using existing CSV files, which may contain older data."
        )
        can_display_charts = True
else:
    missing_csvs = [path.name for path in REQUIRED_CSVS if not path.is_file()]
    if missing_csvs:
        st.error(
            "CSV generation completed without creating all required files. "
            f"Cannot display the charts; missing: {', '.join(missing_csvs)}."
        )
        can_display_charts = False
    else:
        can_display_charts = True

if can_display_charts:
    # Affichage de l'histogramme
    st.plotly_chart(create_histogram(), width="stretch")

    # Affichage de la heatmap
    st.plotly_chart(create_heatmap(), width="stretch")

    # Affichage du graphe réseau (sans filtres)
    fig_network = create_network_graph()
    st.plotly_chart(fig_network, width='stretch')
import streamlit as st
from pathlib import Path
from zipfile import BadZipFile

from graphs.histogramme import create_histogram
from graphs.heatmap import create_heatmap
from graphs.kiviat import create_kiviat
from graphs.network import create_network_graph
from graphs.sunburst import create_sunburst
from scripts.anomalies import SHEET_NAMES, detect_anomalies
from scripts.traitement_histogramme import prepare_histogram
from scripts.traitement_heatmap import prepare_heatmap_data
from scripts.traitement_inventeurs import generate_network_csv_files
from scripts.traitement_sunburst import prepare_sunburst_data

st.set_page_config(page_title="Potion craft", layout="wide")
st.title("Potion craft")

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data" / "processed_csv"
REQUIRED_CSVS = (
    DATA_DIR / "potions_plus_rentables.csv",
    DATA_DIR / "nb_potions_par_competence.csv",
    DATA_DIR / "ingredients_cooccurrence.csv",
    DATA_DIR / "network_nodes.csv",
    DATA_DIR / "network_edges.csv",
    DATA_DIR / "sunburst_potions.csv",
)

# Generate the CSV files used by the charts before loading them.
try:
    # Try to generate the CSV files required to display the charts.
    prepare_histogram()
    prepare_heatmap_data()
    generate_network_csv_files()
    prepare_sunburst_data()
except (BadZipFile, IndexError, KeyError, OSError, TypeError, ValueError) as error:
    # If CSV generation fails, check whether the required files already exist.
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
    # If CSV generation succeeds, check that all required files were created.
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
    # Display the histogram.
    st.plotly_chart(create_histogram(), width="stretch")

    # Display the heatmap.
    st.plotly_chart(create_heatmap(), width="stretch")

    # Display the Kiviat chart.
    st.plotly_chart(create_kiviat(), width="stretch")

    # Display the three-level potion sunburst.
    st.plotly_chart(create_sunburst(), width="stretch")

    # Display the network graph (without filters).
    fig_network = create_network_graph()
    st.plotly_chart(fig_network, width='stretch')



# Display the detected anomalies.
st.divider()
st.subheader("Anomalies détectées dans le classeur")
anomalies = detect_anomalies()
if anomalies.empty:
    st.success("Aucune anomalie détectée.")
else:
    st.caption(f"{len(anomalies)} anomalie(s) recensée(s).")
    # Show the anomaly count for each sheet, including sheets with no anomalies (fill_value=0).
    counts_by_sheet = (
        anomalies.groupby("Feuille")
        .size()
        .reindex(SHEET_NAMES, fill_value=0)
        .rename("Nombre d'anomalies")
        .rename_axis("Feuille")
        .reset_index()
    )
    # Display the anomaly details and the counts for each sheet.
    # st.dataframe creates an interactive table with sorting and search.
    st.dataframe(counts_by_sheet, hide_index=True, width="stretch")
    st.dataframe(anomalies, hide_index=True, width="stretch")

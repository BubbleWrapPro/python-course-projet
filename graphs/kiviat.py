import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from theme import apply_plotly_theme

DATA_PATH = Path("data") / "processed_csv" / "nb_potions_par_competence.csv"

def create_kiviat():
    data = pd.read_csv(DATA_PATH)

    r = list(data["nombre_de_potions"])
    theta = list(
        data["competences"] + " (" + data["nombre_de_potions"].astype(str) + ")"
    )

    # On remet le premier point à la fin pour fermer le graphique
    r.append(r[0])
    theta.append(theta[0])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        name="Potions",
        r=r,
        theta=theta
    ))

    fig.update_traces(
        fill='tonext',
        mode="lines+markers",
        line_color="#9D4EDD",
        marker_color='#3A86FF',
        fillcolor='rgba(157, 78, 221, 0.35)',
        line_width=4,
        marker_size=8
    )
    fig.update_layout(
        title="Nombre de potions par compétence",
        polar=dict(
            radialaxis=dict(visible=True, showticklabels=True, gridcolor="#2E2A45", linecolor="#2E2A45"),
            angularaxis=dict(gridcolor="#2E2A45", linecolor="#2E2A45", tickfont=dict(color="#E0E6ED")),
            bgcolor="#1A1829",
        )
    )
    return apply_plotly_theme(fig)

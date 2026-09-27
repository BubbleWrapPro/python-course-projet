import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

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

    fig.update_traces(fill='tonext', mode="lines+markers",  line_color="#3AC8D8", marker_color='#50BCC7', line_width=5, marker_size=8)
    fig.update_layout(title="Nombre de potions par compétence")
    return fig
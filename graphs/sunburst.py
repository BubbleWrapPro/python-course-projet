from pathlib import Path

import pandas as pd
import plotly.express as px

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed_csv" / "sunburst_potions.csv"


def create_sunburst():
    """
    Creates a sunburst chart visualizing the distribution of potions by type of magic and skill.
    """
    data = pd.read_csv(DATA_PATH)
    figure = px.sunburst(
        data,
        path=["type_magie", "competence", "potion"],
        values="poids",
        color="type_magie",
        title="Répartition des potions par type de magie et compétence",
        color_discrete_map={
            "Noire": "#303030",
            "Blanche": "#E3E3E3",
            "Verte": "#2E8B57",
            "Rouge": "#D9534F",
            "Pourpre": "#845EC2",
            "Bleue": "#4285C5",
        },
        custom_data=["poids"],
    )
    # Update the hover template to show the number of potions in each segment.
    figure.update_traces(
        textinfo="label",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Nombre de potions : %{value:.0f}<extra></extra>"
        ),
        insidetextorientation="radial",
    )
    # Add an explicit color key because Plotly does not show a legend for sunbursts.
    colors = {
        "Noire": "#303030",
        "Blanche": "#E3E3E3",
        "Verte": "#2E8B57",
        "Rouge": "#D9534F",
        "Pourpre": "#845EC2",
        "Bleue": "#4285C5",
    }
    # Add invisible scatter traces for each magic type to create a legend.
    for magic, color in colors.items():
        figure.add_scatter(
            x=[None], y=[None], mode="markers", name=magic,
            marker=dict(size=11, color=color, line=dict(color="#777777", width=0.5)),
            legendgroup=magic, hoverinfo="skip"
        )
    # Update layout for better appearance and legend positioning.
    figure.update_layout(
        template="plotly_white",
        height=750,
        margin=dict(t=80, l=20, r=20, b=85),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        legend=dict(
            title="Types de magie",
            orientation="h",
            x=0.5, y=-0.08,
            xanchor="center", yanchor="top",
            itemsizing="constant",
            font=dict(size=12),
            bgcolor="rgba(0,0,0,0)"
        ),
    )
    return figure


if __name__ == "__main__":
    create_sunburst().show()


from pathlib import Path

import pandas as pd
import plotly.express as px
from theme import THEME_COLORS, apply_plotly_theme

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed_csv" / "sunburst_potions.csv"


def create_sunburst():
    """
    Creates a sunburst chart visualizing the distribution of potions by type of magic and skill.
    """
    data = pd.read_csv(DATA_PATH)
    total_potions = int(data["poids"].sum())

    # Add a constant root column to data.
    data["total"] = f"{total_potions} potions."
    
    colors = dict(THEME_COLORS["magic"])
    colors[f"{total_potions} potions."] = "#1A1829"

    figure = px.sunburst(
        data,
        path=["total", "type_magie", "competence", "potion"],
        values="poids",
        color="type_magie",
        title="Répartition des potions par type de magie et compétence",
        color_discrete_map=colors,
        custom_data=["poids"]
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
    for magic, color in THEME_COLORS["magic"].items():
        figure.add_scatter(
            x=[None], y=[None], mode="markers", name=magic,
            marker=dict(size=11, color=color, line=dict(color="#2E2A45", width=1)),
            legendgroup=magic, hoverinfo="skip"
        )
    
    # Update layout for better appearance and legend positioning.
    figure.update_layout(
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
    return apply_plotly_theme(figure)


if __name__ == "__main__":
    create_sunburst().show()

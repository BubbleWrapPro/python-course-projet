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
    total_potions = int(data["poids"].sum())
    
    # We add a dummy root row so that the sunburst has a central root circle containing the total number of potions.
    root_df = pd.DataFrame({
        "type_magie": ["Total"],
        "competence": [f"{total_potions} potions"],
        "potion": [""],
        "poids": [total_potions]
    })
    
    # Alternatively, using pandas concat to prepend or just setting path properly. 
    # Actually, Plotly sunburst automatically creates a root node if we add a top-level category or if we format path.
    # Let's add a constant root column to data.
    data["total"] = f"{total_potions} potions."
    
    figure = px.sunburst(
        data,
        path=["total", "type_magie", "competence", "potion"],
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
            f"{total_potions} potions.": "#FFFFFF"
        },
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
    colors = {
        "Noire": "#303030",
        "Blanche": "#E3E3E3",
        "Verte": "#2E8B57",
        "Rouge": "#D9534F",
        "Pourpre": "#845EC2",
        "Bleue": "#4285C5",
        f"{total_potions} potions.": "#FFFFFF"
    }
    # Add invisible scatter traces for each magic type to create a legend (excluding the root total).
    for magic, color in colors.items():
        if magic.startswith("Total"):
            continue
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


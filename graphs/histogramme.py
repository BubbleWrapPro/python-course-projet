from pathlib import Path
import pandas as pd
import plotly.express as px
from theme import THEME_COLORS, apply_plotly_theme

DATA_PATH = Path("data") / "processed_csv" / "potions_plus_rentables.csv"


def create_histogram():
    data = pd.read_csv(DATA_PATH)
    histogram = px.bar(
        data,
        x="benefice",
        y="potion",
        color="type_magie",
        orientation="h",
        text=data["benefice"].round(2).astype(str),
        title="Top 10 des potions les plus rentables",
        labels={"benefice": "Bénéfice (en pièces d'or)", "potion": "Potion", "type_magie": "Type de magie"},
        color_discrete_map=THEME_COLORS["magic"],
    )
    histogram.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    histogram.update_traces(
        hovertemplate="%{y} bénéfice: %{x:.2f} pièces d'or",
        textposition="outside",
    )

    return apply_plotly_theme(histogram)

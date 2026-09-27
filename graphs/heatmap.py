from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed_csv" / "ingredients_cooccurrence.csv"


def create_heatmap():
    matrix = pd.read_csv(DATA_PATH, index_col=0)

    # The diagonal shows each ingredient's raw frequency; the other cells show co-occurrences.
    figure = go.Figure(
        data=go.Heatmap(
            z=matrix.values,
            x=matrix.columns,
            y=matrix.index,
            colorscale=[[0, "#F3F7FF"], [0.5, "#2BDE43"], [1, "#0A5624"]],
            hovertemplate="<b>%{y}</b> / <b>%{x}</b><br>Valeur: %{z}<extra></extra>",
            colorbar=dict(title="Fréquence\n/ cooccurrence"),
            zmin=0,
            zmax=max(1, int(matrix.to_numpy().max())),
            showscale=True,
        )
    )

    # Mark the diagonal to make the chart clearer and easier to read.
    for i in range(len(matrix.index)):
        figure.add_trace(
            go.Scatter(
                x=[matrix.columns[i]],
                y=[matrix.index[i]],
                mode="markers",
                marker=dict(size=0, opacity=0),
                showlegend=False,
                hoverinfo="skip",
            )
        )

    # Update the layout to make the chart more readable and visually appealing.
    figure.update_layout(
        title="Heatmap de cooccurrence des 10 ingrédients les plus utilisés",
        xaxis_title="Ingrédient",
        yaxis_title="Ingrédient",
        template="plotly_white",
        height=800,
        width=900,
        margin=dict(l=160, r=40, t=80, b=200),
        xaxis=dict(tickangle=45),
        yaxis=dict(autorange="reversed"),
    )

    return figure


if __name__ == "__main__":
    create_heatmap().show()

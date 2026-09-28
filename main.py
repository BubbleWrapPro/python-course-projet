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
from theme import apply_custom_theme

st.set_page_config(page_title="Potion Craft - Tableau de Bord", layout="wide")
apply_custom_theme()

# Header Hero Banner
st.markdown("""
<div class="potion-hero-banner">
    <h1 style="margin: 0 0 6px 0; font-size: 2.2rem; color: #F8FAFC;">Potion Craft</h1>
    <p style="margin: 0; color: #94A3B8; font-size: 1.05rem;">
        Tableau de bord d'analyse alchimique, de rentabilité et de cartographie des compétences.
    </p>
</div>
""", unsafe_allow_html=True)

# Carte de présentation des bibliothèques importées avec logos vectoriels SVG épurés
st.markdown("""
<div style="background-color: #131826; border: 1px solid #22293A; border-radius: 12px; padding: 20px; margin-bottom: 24px;">
    <h3 style="margin-top: 0; color: #F8FAFC; font-size: 1.1rem; margin-bottom: 14px; font-family: 'Outfit', sans-serif;">Bibliothèques Python utilisées</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px;">
        <div style="background-color: #0B0E17; border: 1px solid #22293A; border-radius: 8px; padding: 12px; display: flex; gap: 12px; align-items: flex-start;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#FF4B4B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
            <div>
                <span style="color: #F8FAFC; font-weight: 600; font-size: 0.9rem;">Streamlit</span>
                <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem; line-height: 1.3;">Interface web interactive et tableau de bord dynamique.</p>
            </div>
        </div>
        <div style="background-color: #0B0E17; border: 1px solid #22293A; border-radius: 8px; padding: 12px; display: flex; gap: 12px; align-items: flex-start;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
            <div>
                <span style="color: #F8FAFC; font-weight: 600; font-size: 0.9rem;">Plotly</span>
                <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem; line-height: 1.3;">Génération des visualisations interactives personnalisées.</p>
            </div>
        </div>
        <div style="background-color: #0B0E17; border: 1px solid #22293A; border-radius: 8px; padding: 12px; display: flex; gap: 12px; align-items: flex-start;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#34D399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            <div>
                <span style="color: #F8FAFC; font-weight: 600; font-size: 0.9rem;">Pandas & NumPy</span>
                <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem; line-height: 1.3;">Manipulation, nettoyage et agrégation des données tabulaires.</p>
            </div>
        </div>
        <div style="background-color: #0B0E17; border: 1px solid #22293A; border-radius: 8px; padding: 12px; display: flex; gap: 12px; align-items: flex-start;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#C084FC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="18" r="3"/><circle cx="6" cy="18" r="3"/><line x1="8.5" y1="7.5" x2="15.5" y2="16.5"/><line x1="6" y1="9" x2="6" y2="15"/></svg>
            <div>
                <span style="color: #F8FAFC; font-weight: 600; font-size: 0.9rem;">NetworkX</span>
                <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem; line-height: 1.3;">Modélisation relationnelle en graphes et calculs de disposition.</p>
            </div>
        </div>
        <div style="background-color: #0B0E17; border: 1px solid #22293A; border-radius: 8px; padding: 12px; display: flex; gap: 12px; align-items: flex-start;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#E2E8F0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
            <div>
                <span style="color: #F8FAFC; font-weight: 600; font-size: 0.9rem;">Pathlib & ZipFile</span>
                <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 0.8rem; line-height: 1.3;">Gestion des fichiers et vérification de l'intégrité du projet.</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

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
    prepare_histogram()
    prepare_heatmap_data()
    generate_network_csv_files()
    prepare_sunburst_data()
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


def render_chart_explanation(title, description, explanation, justification):
    """
    Renders a clean explanatory card detailing the description, analytical explanation, and concise code justification for a chart.
    """
    st.markdown(f"""
    <div style="background-color: #131826; border: 1px solid #22293A; border-radius: 10px; padding: 18px 22px; margin-top: 24px; margin-bottom: 14px;">
        <h3 style="margin: 0 0 12px 0; color: #F8FAFC; font-family: 'Outfit', sans-serif; font-size: 1.15rem;">{title}</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; color: #E2E8F0; font-size: 0.88rem;">
            <div>
                <strong style="color: #38BDF8; display: block; margin-bottom: 4px;">Description du Graphique :</strong>
                <span style="color: #94A3B8; line-height: 1.4;">{description}</span>
            </div>
            <div>
                <strong style="color: #38BDF8; display: block; margin-bottom: 4px;">Explication & Analyse :</strong>
                <span style="color: #94A3B8; line-height: 1.4;">{explanation}</span>
            </div>
            <div>
                <strong style="color: #38BDF8; display: block; margin-bottom: 4px;">Justification du Code :</strong>
                <span style="color: #94A3B8; line-height: 1.4;">{justification}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


if can_display_charts:
    # 1. Histogram
    render_chart_explanation(
        title="1. Top 10 des Potions les Plus Rentables",
        description="Barres horizontales ordonnées représentant le bénéfice net (en pièces d'or) généré par potion, avec un codage couleur par type de magie.",
        explanation="Permet d'identifier immédiatement les recettes générant la plus forte marge financière afin d'orienter la stratégie de fabrication alchimique vers la rentabilité optimale.",
        justification="Calcul du coût net par conversion d'unités et ajout du diluant. Filtrage des 10 meilleures marges via Pandas (sort_values + head(10)) et rendu Plotly horizontal avec cartographie de couleurs par magie."
    )
    st.plotly_chart(create_histogram(), width="stretch")

    # 2. Sunburst
    render_chart_explanation(
        title="2. Répartition Hiérarchique des Potions",
        description="Structure hiérarchique circulaire organisée sur 3 niveaux : Total des potions -> Type de magie -> Compétence requise -> Nom de la potion.",
        explanation="Révèle la distribution relative de chaque école de magie et permet une exploration interactive par zoom des catégories jusqu'aux formules individuelles.",
        justification="Extraction de la hiérarchie magie/compétence/potion, ajout d'un nœud racine global via Pandas (data['poids'].sum()) et rendu d'une arborescence circulaire interactive avec px.sunburst."
    )
    st.plotly_chart(create_sunburst(), width="stretch")

    # 3. Kiviat (Radar)
    render_chart_explanation(
        title="3. Distribution des Potions par Compétence",
        description="Graphique polaire fermé (Radar) mesurant le volume total de potions associées à chaque compétence alchimique requise.",
        explanation="Met en évidence les compétences fortement représentées dans le grimoire (spécialités majeures) ainsi que les compétences plus rares nécessitant un apprentissage ciblé.",
        justification="Découpage des compétences croisées (str.split + explode), comptage par catégorie et fermeture du polygone polaire dans Plotly en raccordant le premier point en fin de liste (r.append(r[0]))."
    )
    st.plotly_chart(create_kiviat(), width="stretch")

    # 4. Heatmap
    render_chart_explanation(
        title="4. Matrice de Cooccurrence des Ingrédients",
        description="Carte thermique mesurant la fréquence de présence conjointe des 10 ingrédients les plus utilisés, la diagonale affichant leur fréquence individuelle.",
        explanation="Permet d'identifier les paires d'ingrédients fréquemment combinées dans les recettes et de repérer les ingrédients centraux (pivots alchimiques).",
        justification="Sélection du Top 10 des ingrédients (Counter.most_common) et calcul des paires via itertools.combinations pour générer une matrice de cooccurrence affichée en palette émeraude."
    )
    st.plotly_chart(create_heatmap(), width="stretch")

    # 5. Network Graph
    render_chart_explanation(
        title="5. Cartographie du Réseau des Inventeurs et Potions",
        description="Graphe relationnel reliant les inventeurs (nœuds principaux) à leurs potions créées, regroupant les inventeurs selon leurs lignées et familles de magie.",
        explanation="Visualise la centralité des grands maîtres inventeurs, le volume de leur production et les liens d'affiliation au sein des familles alchimiques.",
        justification="Modélisation du réseau avec NetworkX (nx.Graph), positionnement spatial reproductible par ressorts (nx.spring_layout, seed=42) et dispersion géométrique des potions autour de leur inventeur."
    )
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
    counts_by_sheet = (
        anomalies.groupby("Feuille")
        .size()
        .reindex(SHEET_NAMES, fill_value=0)
        .rename("Nombre d'anomalies")
        .rename_axis("Feuille")
        .reset_index()
    )
    st.dataframe(counts_by_sheet, hide_index=True, width="stretch")
    st.dataframe(anomalies, hide_index=True, width="stretch")

import streamlit as st
import plotly.graph_objects as go

# Palette de couleurs du thème "Atelier d'Alchimie"
THEME_COLORS = {
    "bg_dark": "#0B0E17",
    "bg_card": "#131826",
    "bg_card_border": "#22293A",
    "text_main": "#E2E8F0",
    "text_muted": "#94A3B8",
    "primary": "#38BDF8",      # Bleu Ciel Moderne
    "secondary": "#A855F7",    # Pourpre Arcane
    "accent": "#34D399",       # Émeraude
    "magic": {
        "Noire": "#334155",    # Magie Noire (Ardoise)
        "Blanche": "#E2E8F0",  # Magie Blanche (Argent)
        "Verte": "#34D399",    # Magie Verte (Émeraude)
        "Rouge": "#F87171",    # Magie Rouge (Rubis)
        "Pourpre": "#C084FC",  # Magie Pourpre (Améthyste)
        "Bleue": "#38BDF8",    # Magie Bleue (Saphir)
    }
}


def apply_custom_theme():
    """
    Injects custom CSS styles into the Streamlit app with clean typography and no AI-style accent bars or pills.
    """
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700&display=swap');

    /* Global Base Styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #E2E8F0;
    }

    .stApp {
        background-color: #0B0E17;
    }

    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Outfit', 'Inter', sans-serif !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.02em;
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        color: #38BDF8 !important;
        font-size: 2rem !important;
    }

    div[data-testid="stMetric"] {
        background-color: #131826;
        border: 1px solid #22293A;
        border-radius: 10px;
        padding: 16px;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #131826 !important;
        border-radius: 8px !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', sans-serif !important;
        border: 1px solid #22293A !important;
    }

    /* Tabs styling */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #94A3B8 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38BDF8 !important;
        border-bottom: 2px solid #38BDF8 !important;
    }

    /* Custom Hero Header */
    .potion-hero-banner {
        background-color: #131826;
        border: 1px solid #22293A;
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #22293A;
    }

    /* Divider line */
    hr {
        border-color: #22293A !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def apply_plotly_theme(fig):
    """
    Applies the custom Plotly layout theme with dark background and clean typography.
    """
    fig.update_layout(
        paper_bgcolor="#0B0E17",
        plot_bgcolor="#131826",
        font=dict(
            family="Inter, sans-serif",
            color="#E2E8F0",
            size=12,
        ),
        title=dict(
            font=dict(
                family="Outfit, sans-serif",
                size=17,
                color="#F8FAFC",
            )
        ),
        xaxis=dict(
            gridcolor="#22293A",
            zerolinecolor="#22293A",
            tickfont=dict(color="#94A3B8"),
            title=dict(font=dict(color="#E2E8F0")),
        ),
        yaxis=dict(
            gridcolor="#22293A",
            zerolinecolor="#22293A",
            tickfont=dict(color="#94A3B8"),
            title=dict(font=dict(color="#E2E8F0")),
        ),
        legend=dict(
            bgcolor="rgba(19, 24, 38, 0.9)",
            bordercolor="#22293A",
            borderwidth=1,
            font=dict(color="#E2E8F0", size=11),
        ),
        hoverlabel=dict(
            bgcolor="#131826",
            bordercolor="#38BDF8",
            font=dict(family="Inter, sans-serif", color="#F8FAFC"),
        ),
    )
    return fig


def render_theme_section():
    """
    Renders the theme presentation section with detailed explanations and visual illustrations.
    """
    st.markdown("""
    <div class="potion-hero-banner">
        <h2 style="margin: 0 0 8px 0; color: #F8FAFC;">Charte Graphique et Thème Visuel</h2>
        <p style="margin: 0; color: #94A3B8; font-size: 1rem;">
            Conception visuelle, palette chromatique et principes d'ergonomie appliqués au tableau de bord.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_concept, tab_swatches, tab_illustration, tab_preview = st.tabs([
        "Explications et Concept",
        "Nuancier des Magies",
        "Illustration Visuelle",
        "Composants Stylisés"
    ])

    with tab_concept:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### Direction Artistique
            L'interface adopte un style épuré axé sur la lisibilité des données complexes :

            * **Mode Sombre** : Un fond neutre (`#0B0E17`) avec des cartes en contraste doux (`#131826`).
            * **Hiérarchie Visuelle** : Usage de contrastes mesurés pour diriger l'attention vers les graphiques sans surcharge décorative.
            * **Typographie** : Alliance des polices *Outfit* pour les titres et *Inter* pour le corps de texte.
            """)

        with col2:
            st.markdown("""
            ### Ergonomie et Accessibilité
            * **Unité Chromatique** : Les 6 types de magie conservent un code couleur identique sur l'ensemble des 5 visualisations.
            * **Lisibilité** : Niveaux de contraste conformes aux standards de visualisation de données.
            * **Interactivité** : Surbrillance au survol pour faciliter l'exploration dynamique.
            """)

    with tab_swatches:
        st.markdown("### Nuancier Sémantique des Types de Magie")
        st.caption("Couleurs associées à chaque école de magie à travers les visualisations.")

        cols = st.columns(6)
        swatches_data = [
            ("Magie Noire", "#334155", "#FFFFFF", "Ardoise", "Sorts d'ombre et secrets"),
            ("Magie Blanche", "#E2E8F0", "#0F172A", "Argent", "Soins et protections"),
            ("Magie Verte", "#34D399", "#0F172A", "Émeraude", "Botanique et alchimie végétale"),
            ("Magie Rouge", "#F87171", "#FFFFFF", "Rubis", "Potions d'attaque et de feu"),
            ("Magie Pourpre", "#C084FC", "#FFFFFF", "Améthyste", "Mystères et arcanes"),
            ("Magie Bleue", "#38BDF8", "#0F172A", "Saphir", "Mana et esprits"),
        ]

        for col, (name, hex_code, text_col, ref_title, desc) in zip(cols, swatches_data):
            with col:
                st.markdown(f"""
                <div style="background-color: #131826; border: 1px solid #22293A; border-radius: 8px; padding: 12px; text-align: center;">
                    <div style="background-color: {hex_code}; height: 48px; border-radius: 6px; margin-bottom: 8px; display: flex; align-items: center; justify-content: center; color: {text_col}; font-weight: 600; font-size: 0.8rem;">
                        {hex_code}
                    </div>
                    <div style="font-weight: 600; font-size: 0.9rem; color: #F8FAFC;">{name}</div>
                    <div style="font-size: 0.75rem; color: #38BDF8; margin-top: 2px;">{ref_title}</div>
                    <p style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px; line-height: 1.2;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)

    with tab_illustration:
        st.markdown("### Illustration Vectorielle : Flacon d'Alchimie")

        col_svg, col_info = st.columns([1, 2])
        with col_svg:
            st.markdown("""
            <div style="text-align: center; background-color: #131826; padding: 20px; border-radius: 12px; border: 1px solid #22293A;">
                <svg width="160" height="200" viewBox="0 0 200 240" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="85" y="15" width="30" height="15" rx="3" fill="#64748B"/>
                    <path d="M80 30 H120 V60 L150 120 C170 160 160 210 100 210 C40 210 30 160 50 120 L80 60 V30 Z" fill="#131826" stroke="#38BDF8" stroke-width="2"/>
                    <path d="M55 130 C70 125 90 135 100 130 C120 125 135 135 145 130 C158 155 152 200 100 200 C48 200 42 155 55 130 Z" fill="url(#liquidGrad)" opacity="0.8"/>
                    <circle cx="90" cy="160" r="4" fill="#E2E8F0" opacity="0.6"/>
                    <circle cx="115" cy="145" r="5" fill="#E2E8F0" opacity="0.8"/>
                    <defs>
                        <linearGradient id="liquidGrad" x1="0" y1="120" x2="0" y2="210">
                            <stop offset="0%" stop-color="#38BDF8"/>
                            <stop offset="100%" stop-color="#C084FC"/>
                        </linearGradient>
                    </defs>
                </svg>
            </div>
            """, unsafe_allow_html=True)

        with col_info:
            st.markdown("""
            #### Structure de l'Illustration
            * **Récipient** : Représentation schématique du flacon alchimique.
            * **Graduation de Couleurs** : Dégradé reliant le Saphir (`#38BDF8`) à l'Améthyste (`#C084FC`), symbolisant la variété des formules traitées dans le projet.
            """)

    with tab_preview:
        st.markdown("### Démonstration des Composants UI")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric(label="Potions Référencées", value="150", delta="+12")
        m2.metric(label="Ingrédients Analysés", value="42", delta="100%")
        m3.metric(label="Bénéfice Maximal", value="128.5 po", delta="+18.4%")
        m4.metric(label="Anomalies Détectées", value="14", delta="-3", delta_color="inverse")

        st.markdown("""
        <div style="background-color: #131826; border: 1px solid #22293A; padding: 16px; border-radius: 8px; margin-top: 16px;">
            <p style="margin: 0; color: #94A3B8; font-size: 0.9rem;">
                Les graphiques Plotly et composants Streamlit héritent de cette feuille de style uniforme.
            </p>
        </div>
        """, unsafe_allow_html=True)

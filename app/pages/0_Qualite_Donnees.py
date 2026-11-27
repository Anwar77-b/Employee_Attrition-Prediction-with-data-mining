"""Page 0 — Data quality and descriptive outlier review."""
from pathlib import Path
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

st.set_page_config(
    page_title="Qualité & Outliers — Attrition RH",
    page_icon="🧪",
    layout="wide",
)

from app.theme import apply_theme, footer_html, page_divider_html
from app.utils import (
    load_data,
    load_outlier_report,
    render_sidebar,
    section_header,
    show_missing_artifact_warning,
    kpi_card,
    PRIMARY_COLOR,
    COLOR_NO,
    COLOR_WARN,
    COLOR_YES,
)
from app.visualization import outlier_bar
from src.preprocessing import ID_COL, NUMERIC_COLS, ORDINAL_COLS, TARGET

apply_theme()
df = load_data()

st.title("🧪 Qualité & Outliers")
st.markdown(page_divider_html(), unsafe_allow_html=True)
render_sidebar(df=None, show_filters=False)

if df is None:
    show_missing_artifact_warning(
        "Jeu de données (Employee_Attrition_DataSet.csv)",
        "Placez le fichier dans data/raw/",
    )
    st.markdown(footer_html("Qualité indisponible sans jeu source."), unsafe_allow_html=True)
    st.stop()

section_header(
    "Audit rapide du jeu source",
    "Contrôles descriptifs sur les 10 000 lignes du fichier brut",
    icon="🔎",
)

missing_total = int(df.isna().sum().sum())
duplicate_total = int(df.duplicated().sum())
numeric_cols = [c for c in NUMERIC_COLS + ORDINAL_COLS if c in df.columns]

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Lignes", f"{len(df):,}", border_color=PRIMARY_COLOR)
with c2:
    kpi_card("Colonnes", str(df.shape[1]), border_color=PRIMARY_COLOR)
with c3:
    kpi_card("Valeurs manquantes", str(missing_total), border_color=COLOR_NO if missing_total == 0 else COLOR_WARN)
with c4:
    kpi_card("Doublons", str(duplicate_total), border_color=COLOR_NO if duplicate_total == 0 else COLOR_WARN)

st.markdown("##### Plages observées")
ranges = pd.DataFrame(
    {
        "Variable": numeric_cols,
        "Minimum": [df[c].min() for c in numeric_cols],
        "Maximum": [df[c].max() for c in numeric_cols],
        "Médiane": [df[c].median() for c in numeric_cols],
    }
)
st.dataframe(ranges, use_container_width=True, hide_index=True)

section_header(
    "Rapport outliers versionné",
    "Quatre méthodes complémentaires, calculées sur le jeu brut à des fins descriptives",
    icon="📐",
)

report = load_outlier_report()
if report is None:
    show_missing_artifact_warning(
        "results/outliers_report.csv",
        "python scripts/run_outliers.py",
    )
else:
    k1, k2, k3 = st.columns(3)
    with k1:
        kpi_card("Méthodes", str(report["methode"].nunique()), border_color=PRIMARY_COLOR)
    with k2:
        kpi_card("Lignes de rapport", str(len(report)), border_color=PRIMARY_COLOR)
    with k3:
        kpi_card("Occurrences signalées", f"{int(report['n_outliers'].sum()):,}", border_color=COLOR_WARN)

    st.plotly_chart(outlier_bar(report), use_container_width=True)
    st.dataframe(report, use_container_width=True, hide_index=True)

    st.info(
        "Un outlier n'est pas automatiquement une erreur. La winsorisation est recommandée "
        "après vérification manuelle ; la suppression est réservée aux erreurs avérées. "
        "Ni la cible ni l'identifiant n'ont servi à la détection."
    )

    with st.expander("Lecture du fichier et méthodologie", expanded=False):
        st.caption(
            f"Colonnes du rapport : {', '.join(report.columns)}. "
            f"Cible exclue : `{TARGET}` ; identifiant exclu : `{ID_COL}`."
        )
        st.caption("Le détail des formules et des seuils figure dans docs/OUTLIERS.md.")

st.markdown(footer_html("Audit descriptif · Aucune modification du jeu ni des résultats."), unsafe_allow_html=True)

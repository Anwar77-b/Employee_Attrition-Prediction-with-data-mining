"""Shared utilities, UI components and theme bridge for the Streamlit app.

The business schema is imported from ``src.preprocessing``; this module only
provides display helpers and read-only artifact loaders.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from app.theme import (
    ACCENT_AMBER,
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_ROSE,
    TEXT_MUTED,
    apply_theme,
    footer_html,
    page_divider_html,
    risk_badge_html,
    sidebar_header_html,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import load_bundle as _load_bundle  # noqa: E402
from src.preprocessing import (  # noqa: E402
    CATEGORICAL_FEATURES as _CATEGORICAL_FEATURES,
    FEATURE_COLS,
    ID_COL,
    NUMERICAL_FEATURES as _NUMERICAL_FEATURES,
    TARGET,
)

# ── Paths ──────────────────────────────────────────────────────────────
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA = DATA_DIR / "raw" / "Employee_Attrition_DataSet.csv"
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"
OUTLIER_REPORT = RESULTS_DIR / "outliers_report.csv"

# ── Design tokens (re-exported for page imports) ─────────────────────────
PRIMARY_COLOR = ACCENT_CYAN
SECONDARY_COLOR = ACCENT_GREEN
COLOR_NO = ACCENT_GREEN
COLOR_YES = ACCENT_ROSE
COLOR_WARN = ACCENT_AMBER
COLOR_MAP = {"No": COLOR_NO, "Yes": COLOR_YES}

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_COLORWAY = [
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_ROSE,
    ACCENT_AMBER,
    "#7C5CE7",
    "#4BA3C7",
    "#97A4C2",
    "#64748B",
]

# ── Feature definitions (single source of truth: src.preprocessing) ────
NUMERICAL_FEATURES = list(_NUMERICAL_FEATURES)
CATEGORICAL_FEATURES = list(_CATEGORICAL_FEATURES)
ALL_FEATURES = list(FEATURE_COLS)  # alias conservé pour les pages existantes

MODEL_NAMES = {
    "ZeroR": "Zero-R (Baseline)",
    "KNN": "K-NN",
    "DecisionTree": "Arbre de Décision",
    "RandomForest": "Forêt Aléatoire",
    "NaiveBayes": "Naive Bayes",
    "SVM": "SVM",
}

DEPARTMENT_LIST = ["Sales", "Engineering", "Operations", "Marketing", "Finance", "IT", "HR"]


def get_plotly_template() -> str:
    """Return the Plotly template matching the always-dark console theme."""
    return PLOTLY_TEMPLATE


# ── CSS loading ──────────────────────────────────────────────────────────
def load_css() -> None:
    """Inject the unique console stylesheet."""
    st.session_state["dark_mode"] = True
    apply_theme()


def inject_custom_css() -> None:
    """Backwards compatibility alias."""
    load_css()


# ── Reusable UI components ───────────────────────────────────────────────
def kpi_card(
    titre: str,
    valeur: Any,
    delta: Optional[str] = None,
    delta_type: str = "neutral",
    border_color: str = PRIMARY_COLOR,
    help_text: Optional[str] = None,
) -> None:
    """Render a compact console metric card."""
    delta_html = ""
    if delta:
        delta_class = "neutral"
        if delta_type == "positive" or (isinstance(delta, str) and delta.startswith("+")):
            delta_class = "positive"
        elif delta_type == "negative" or (isinstance(delta, str) and delta.startswith("-")):
            delta_class = "negative"
        delta_html = f'<div class="kpi-delta {delta_class}">{delta}</div>'

    title_attr = f'title="{help_text}"' if help_text else ""
    st.markdown(
        f"""
        <div class="kpi-card" style="border-top-color:{border_color} !important;" {title_attr}>
            <div class="kpi-title">{titre}</div>
            <div class="kpi-value">{valeur}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(title: str, value: Any, css_class: str = "") -> None:
    """Backwards compatibility metric card."""
    border_color = PRIMARY_COLOR
    if "green" in css_class:
        border_color = COLOR_NO
    elif "red" in css_class:
        border_color = COLOR_YES
    elif "orange" in css_class or "amber" in css_class:
        border_color = COLOR_WARN
    elif "blue" in css_class or "cyan" in css_class:
        border_color = SECONDARY_COLOR
    kpi_card(title, value, border_color=border_color)


def risk_badge(probabilite: float, large: bool = False) -> str:
    """Return the HTML badge used by prediction pages."""
    label, _, _ = get_risk_level(probabilite)
    prediction = "Yes" if (probabilite * 100 if probabilite <= 1 else probabilite) >= 50 else "No"
    return risk_badge_html(label, probabilite, prediction)


def section_header(titre: str, sous_titre: Optional[str] = None, icon: Optional[str] = None) -> None:
    """Render a consistent section header with the console divider."""
    icon_html = f"<span>{icon}</span> " if icon else ""
    sub_html = f'<p class="section-header-subtitle">{sous_titre}</p>' if sous_titre else ""
    st.markdown(
        f"""
        <div class="section-header-container">
            <h3 class="section-header-title">{icon_html}{titre}</h3>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(page_divider_html(), unsafe_allow_html=True)


def gauge_chart(probabilite: float, title: str = "Risque d'attrition") -> go.Figure:
    """Generate a dark Plotly gauge for the attrition probability."""
    p_pct = probabilite * 100 if probabilite <= 1.0 else probabilite
    if p_pct < 30.0:
        bar_color = COLOR_NO
    elif p_pct < 60.0:
        bar_color = COLOR_WARN
    else:
        bar_color = COLOR_YES

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=p_pct,
            number={"suffix": "%", "font": {"size": 38, "color": "#E6EDF7", "family": "monospace"}},
            title={"text": f"<b>{title}</b>", "font": {"size": 16, "color": TEXT_MUTED}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": TEXT_MUTED},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "#101826",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 30], "color": "#12352E"},
                    {"range": [30, 60], "color": "#3B2C14"},
                    {"range": [60, 100], "color": "#3D1B27"},
                ],
                "threshold": {"line": {"color": bar_color, "width": 4}, "thickness": 0.8, "value": p_pct},
            },
        )
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=260,
        margin=dict(t=40, b=10, l=30, r=30),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "monospace", "color": "#E6EDF7"},
    )
    return fig


# ── Data and artifact loading ────────────────────────────────────────────
@st.cache_data
def load_data() -> Optional[pd.DataFrame]:
    """Load the raw dataset; return None when the CSV is absent."""
    if not RAW_DATA.exists():
        return None
    return pd.read_csv(RAW_DATA)


@st.cache_resource
def load_bundle(name: str = "best_model"):
    """Load the trained Pipeline bundle, including the optimized threshold."""
    path = MODELS_DIR / f"{name}.joblib"
    if not path.exists():
        return None
    try:
        return _load_bundle(path)
    except Exception:
        return None


@st.cache_resource
def load_model(name: str = "best_model"):
    """Compatibility helper: return the Pipeline held by the bundle."""
    bundle = load_bundle(name)
    return None if bundle is None else bundle["model"]


@st.cache_data
def load_json(filename: str) -> Optional[dict]:
    """Load a JSON artifact from results/; return None on failure."""
    path = RESULTS_DIR / filename
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return None


@st.cache_data
def load_outlier_report() -> Optional[pd.DataFrame]:
    """Read the versioned outlier report. Never recomputes or modifies it."""
    if not OUTLIER_REPORT.exists():
        return None
    try:
        return pd.read_csv(OUTLIER_REPORT)
    except Exception:
        return None


def _detect_test_artifacts() -> bool:
    """Flag only explicit test artifacts; never infer a status from results."""
    for folder in (MODELS_DIR, RESULTS_DIR):
        if not folder.exists():
            continue
        for path in folder.iterdir():
            name = path.name.lower()
            if name.startswith("test_") or name.endswith("_test.joblib") or "artefact_test" in name:
                return True
    return False


# ── Risk helpers ─────────────────────────────────────────────────────────
def get_risk_level(proba: float) -> Tuple[str, str, str]:
    """Return (label, css_class, emoji) from an attrition probability."""
    p_pct = proba * 100 if proba <= 1.0 else proba
    if p_pct < 30.0:
        return "Faible", "rh-risk-low", "🟢"
    if p_pct < 60.0:
        return "Modéré", "rh-risk-medium", "🟡"
    return "Élevé", "rh-risk-high", "🔴"


def get_risk_color(proba: float) -> str:
    """Return the hex color associated with a probability."""
    p_pct = proba * 100 if proba <= 1.0 else proba
    if p_pct < 30.0:
        return COLOR_NO
    if p_pct < 60.0:
        return COLOR_WARN
    return COLOR_YES


# ── Recommendations ──────────────────────────────────────────────────────
def generate_recommendations(row: dict, proba: float) -> List[str]:
    """Generate rule-based retention leads from editable HR features."""
    recs: List[str] = []
    if row.get("OverTime") == "Yes":
        recs.append("⏰ **Réduire les heures supplémentaires** : l'overtime est un facteur majeur de départ.")
    if row.get("JobSatisfaction", 5) <= 2:
        recs.append("😊 **Améliorer la satisfaction au travail** : organiser un entretien individuel d'écoute.")
    if row.get("WorkLifeBalance", 5) <= 2:
        recs.append("⚖️ **Équilibre vie pro/perso** : proposer du télétravail ou des horaires aménagés.")
    if row.get("YearsAtCompany", 0) <= 2:
        recs.append("🎯 **Renforcer le parcours d'intégration** : les nouvelles recrues sont les plus vulnérables.")
    if row.get("MonthlyIncome", 99999) < 5500:
        recs.append("💰 **Réviser la grille salariale** : le salaire se situe sous la moyenne observée.")
    if row.get("DistanceFromHome", 0) > 25:
        recs.append("🏠 **Aménager le transport / distanciel** : le temps de trajet domicile-travail est élevé.")
    if row.get("PromotionLast5Years") == "No" and row.get("YearsAtCompany", 0) >= 5:
        recs.append("📈 **Planifier une évolution de carrière** : aucune promotion enregistrée depuis 5 ans.")
    if row.get("TrainingHoursLastYear", 99) < 10:
        recs.append("📚 **Proposer des formations** : le développement des compétences fidélise les talents.")
    if not recs:
        recs.append("✅ **Profil stable** : maintenir les actions régulières de reconnaissance et d'écoute.")
    return recs


# ── Sidebar and global filters ───────────────────────────────────────────
def init_session_state(df: Optional[pd.DataFrame] = None) -> None:
    """Initialise global filter values once per session."""
    if "global_departments" not in st.session_state:
        if df is not None and "Department" in df.columns:
            st.session_state.global_departments = sorted(df["Department"].unique().tolist())
        else:
            st.session_state.global_departments = DEPARTMENT_LIST
    if "global_overtime" not in st.session_state:
        st.session_state.global_overtime = "Tous"
    if "global_promotion" not in st.session_state:
        st.session_state.global_promotion = "Tous"
    if "global_age_range" not in st.session_state:
        if df is not None and "Age" in df.columns:
            st.session_state.global_age_range = (int(df["Age"].min()), int(df["Age"].max()))
        else:
            st.session_state.global_age_range = (20, 65)
    if "global_income_range" not in st.session_state:
        if df is not None and "MonthlyIncome" in df.columns:
            st.session_state.global_income_range = (int(df["MonthlyIncome"].min()), int(df["MonthlyIncome"].max()))
        else:
            st.session_state.global_income_range = (2000, 20000)


@st.cache_data(show_spinner=False)
def filter_employee_data(
    df: pd.DataFrame,
    departments: Tuple[str, ...],
    overtime: str,
    age_range: Tuple[int, int],
    income_range: Tuple[int, int],
) -> pd.DataFrame:
    """Apply sidebar filters and return a copy."""
    filtered = df
    if departments:
        filtered = filtered[filtered["Department"].isin(departments)]
    if overtime == "Oui":
        filtered = filtered[filtered["OverTime"] == "Yes"]
    elif overtime == "Non":
        filtered = filtered[filtered["OverTime"] == "No"]
    return filtered[
        (filtered["Age"] >= age_range[0])
        & (filtered["Age"] <= age_range[1])
        & (filtered["MonthlyIncome"] >= income_range[0])
        & (filtered["MonthlyIncome"] <= income_range[1])
    ].copy()


def render_sidebar(df: Optional[pd.DataFrame] = None, show_filters: bool = True) -> Optional[pd.DataFrame]:
    """Render the console sidebar, status panel and optional global filters."""
    load_css()
    init_session_state(df)

    dataset_available = df is not None or RAW_DATA.exists()
    model_available = load_model() is not None
    st.sidebar.markdown(
        sidebar_header_html(dataset_available, model_available, _detect_test_artifacts()),
        unsafe_allow_html=True,
    )

    filtered_df = df.copy() if df is not None else None

    if show_filters and df is not None:
        st.sidebar.markdown("##### 🔎 Filtres globaux")
        with st.sidebar.expander("⚙️ Paramètres des filtres", expanded=True):
            all_depts = sorted(df["Department"].unique().tolist())
            st.session_state.global_departments = st.multiselect(
                "Départements",
                options=all_depts,
                default=st.session_state.global_departments,
                help="Filtrer par un ou plusieurs départements",
            )
            ot_options = ["Tous", "Oui", "Non"]
            ot_index = ot_options.index(st.session_state.global_overtime) if st.session_state.global_overtime in ot_options else 0
            st.session_state.global_overtime = st.radio(
                "Heures supplémentaires",
                options=ot_options,
                index=ot_index,
                horizontal=True,
            )
            min_age, max_age = int(df["Age"].min()), int(df["Age"].max())
            st.session_state.global_age_range = st.slider(
                "Tranche d'âge", min_value=min_age, max_value=max_age,
                value=st.session_state.global_age_range,
            )
            min_income, max_income = int(df["MonthlyIncome"].min()), int(df["MonthlyIncome"].max())
            st.session_state.global_income_range = st.slider(
                "Revenu mensuel", min_value=min_income, max_value=max_income,
                value=st.session_state.global_income_range, step=500,
            )

        filtered_df = filter_employee_data(
            filtered_df,
            tuple(st.session_state.global_departments),
            st.session_state.global_overtime,
            tuple(st.session_state.global_age_range),
            tuple(st.session_state.global_income_range),
        )

    render_sidebar_footer()
    return filtered_df


def render_sidebar_footer() -> None:
    """Render the sidebar academic disclaimer."""
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div class="rh-status-row" style="line-height:1.5;">
            <strong>📊 Data Mining 2026/2027</strong><br>
            Mini-projet — classification supervisée<br>
            ⚠️ Jeu synthétique : aucune décision RH réelle.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_footer() -> None:
    """Render the identical footer on every page."""
    st.markdown(
        footer_html(
            "Console RH académique · Données synthétiques · "
            "<strong>Aucune décision RH automatisée</strong>"
        ),
        unsafe_allow_html=True,
    )


# ── Missing artifact warning ────────────────────────────────────────────
def show_missing_artifact_warning(artifact_name: str, fix_command: str = "") -> None:
    """Show a styled warning banner when an artifact is missing."""
    message = f"⚠️ **Artefact manquant : {artifact_name}**"
    if fix_command:
        message += f"\n\nCommande de régénération :\n```powershell\n{fix_command}\n```"
    st.warning(message)

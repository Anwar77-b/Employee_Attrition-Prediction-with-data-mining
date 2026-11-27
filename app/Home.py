"""Home page — Console landing page for the Employee Attrition application."""
from pathlib import Path
import sys

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

st.set_page_config(
    page_title="Attrition RH — Console",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

from app.theme import apply_theme, footer_html, page_divider_html
from app.utils import (
    COLOR_NO,
    COLOR_WARN,
    COLOR_YES,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    kpi_card,
    load_data,
    render_sidebar,
    section_header,
    show_missing_artifact_warning,
)

apply_theme()
render_sidebar(df=None, show_filters=False)

st.title("💼 Prédiction de l'Attrition des Employés")
st.markdown(page_divider_html(), unsafe_allow_html=True)
st.caption(
    "Console analytique pour anticiper les départs, explorer les facteurs d'engagement "
    "et comparer les modèles. Données synthétiques à vocation académique."
)

df = load_data()
if df is not None:
    total = len(df)
    attrition_count = int((df["Attrition"] == "Yes").sum())
    attrition_rate = attrition_count / total * 100
    avg_salary = float(df["MonthlyIncome"].mean())
    avg_tenure = float(df["YearsAtCompany"].mean())
    avg_satisfaction = float(df["JobSatisfaction"].mean())

    section_header("Indicateurs clés", "Lecture globale du jeu source, avant modélisation", icon="📌")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Effectif total", f"{total:,}", border_color=PRIMARY_COLOR)
    with c2:
        kpi_card("Taux d'attrition", f"{attrition_rate:.2f}%", delta=f"{attrition_count} départs", delta_type="negative", border_color=COLOR_YES)
    with c3:
        kpi_card("Salaire moyen", f"{avg_salary:,.0f} MAD", delta="Mensuel brut", border_color=COLOR_NO)
    with c4:
        kpi_card("Ancienneté moyenne", f"{avg_tenure:.1f} ans", delta=f"Satisfaction {avg_satisfaction:.1f}/5", border_color=COLOR_WARN)
else:
    show_missing_artifact_warning("Jeu de données (Employee_Attrition_DataSet.csv)", "Placez le fichier dans data/raw/")

section_header("Modules de la console", "Huit écrans couvrant la qualité, l'exploration, la prédiction et la restitution", icon="🗂️")

NAV = [
    ("pages/0_Qualite_Donnees.py", "🧪", "0. Qualité & outliers", "Contrôles, plages et lecture du rapport des quatre méthodes de détection.", "Vérifier la qualité", PRIMARY_COLOR),
    ("pages/1_Dashboard.py", "📊", "1. Exploration RH", "Filtres dynamiques, distributions, fréquences, corrélations et tests statistiques.", "Explorer les données", SECONDARY_COLOR),
    ("pages/2_Prediction.py", "🔮", "2. Prédiction individuelle", "Formulaire des 12 variables, jauge de risque, recommandations et scénarios.", "Tester un profil", COLOR_YES),
    ("pages/3_Performance_Modeles.py", "🏆", "3. Performance modèles", "Comparaison des six algorithmes, CV 5 plis, ROC/PR et matrices de confusion.", "Comparer les modèles", PRIMARY_COLOR),
    ("pages/4_Facteurs_Demission.py", "🔍", "4. Facteurs de démission", "Importance des variables et explications SHAP avec la même charte graphique.", "Analyser les facteurs", COLOR_WARN),
    ("pages/5_Prediction_en_lot.py", "📦", "5. Prédiction en lot", "Trame CSV, téléversement, avertissements de schéma et export des scores.", "Lancer un lot", SECONDARY_COLOR),
    ("pages/6_A_Propos.py", "📖", "6. À propos", "Démarche CRISP-DM, dictionnaire, contrat modèle, éthique et limites.", "Consulter la documentation", PRIMARY_COLOR),
]

for start in range(0, len(NAV), 3):
    row = NAV[start:start + 3]
    columns = st.columns(len(row))
    for col, item in zip(columns, row):
        path, icon, title, desc, label, color = item
        with col:
            st.markdown(
                f"""
                <div class="nav-card" style="border-top:2px solid {color};">
                    <div class="nav-card-icon">{icon}</div>
                    <div class="nav-card-title">{title}</div>
                    <div class="nav-card-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(path, label=label, icon=icon, use_container_width=True)

section_header(
    "Pipeline scientifique",
    "CRISP-DM appliqué à un jeu synthétique de 10 000 collaborateurs",
    icon="⚙️",
)
st.markdown(
    """
    | Phase | Opérations | Garanties |
    |---|---|---|
    | 1. Audit & exploration | Qualité, cible, quatre méthodes d'outliers | Jeu brut non modifié |
    | 2. Tests statistiques | Shapiro, χ², Kruskal-Wallis, Mann-Whitney, Spearman | Conclusions associatives |
    | 3. Préparation | Encodage et standardisation dans une pipeline | Ajustement sur l'apprentissage seulement |
    | 4. Modélisation | Six algorithmes, validation croisée stratifiée | Sélection sur la CV, jamais sur le test |
    | 5. Déploiement | Console Streamlit à huit écrans | Métriques affichées, jamais recalculées |
    """
)

st.markdown(footer_html("Console RH académique · Données synthétiques · <strong>Aucune décision RH automatisée</strong>"), unsafe_allow_html=True)

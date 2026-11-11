"""Page 6 — About: Detailed project background, methodology, dataset dictionary and ethics."""
from pathlib import Path
import sys

import streamlit as st

# Ensure project root is on sys.path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

st.set_page_config(
    page_title="À Propos — Attrition RH",
    page_icon="📖",
    layout="wide",
)

from app.utils import (
    load_css,
    kpi_card,
    section_header,
    render_sidebar,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    COLOR_NO,
    COLOR_YES,
    COLOR_WARN,
)

# Inject custom stylesheet
load_css()

# Render shared sidebar
render_sidebar(df=None, show_filters=False)

# ── Header ─────────────────────────────────────────────────────────────
section_header(
    "À Propos du Projet — Data Mining 2026/2027",
    "Méthodologie, dictionnaire des variables, cadre éthique et détails algorithmiques",
    icon="📖",
)

# ── Overview Cards ─────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("Cadre Académique", "Track A : Sup.", delta="Classification binaire", border_color=PRIMARY_COLOR)
with c2:
    kpi_card("Volume de Données", "10 000 lignes", delta="14 variables", border_color=SECONDARY_COLOR)
with c3:
    kpi_card("Algorithmes Évalués", "6 Modèles ML", delta="Zero-R à SVM", border_color=COLOR_NO)
with c4:
    kpi_card("Validation Croisée", "5-Fold Stratifiée", delta="Optimisation GridSearchCV", border_color=COLOR_WARN)

st.markdown("<br>", unsafe_allow_html=True)

tab_dict, tab_models, tab_metrics, tab_ethics = st.tabs([
    "📚 Dictionnaire des Données",
    "🤖 Algorithmes de Machine Learning",
    "📐 Métriques d'Évaluation",
    "⚖️ Cadre Éthique & Déontologique",
])

# ── Tab 1: Data Dictionary ─────────────────────────────────────────────
with tab_dict:
    st.markdown("#### 📚 Dictionnaire des 14 Caractéristiques du Dataset")
    st.markdown(
        """
        | Nom de la variable | Type | Description | Valeurs possibles |
        |---|---|---|---|
        | **EmployeeID** | Catégoriel (ID) | Identifiant unique anonymisé | `EMP0000` à `EMP9999` |
        | **Age** | Numérique | Âge chronologique du collaborateur | 18 à 60 ans |
        | **Department** | Catégoriel | Département d'affectation principal | Sales, Engineering, Operations, Marketing, Finance, IT, HR |
        | **JobLevel** | Numérique ordinal | Échelon hiérarchique au sein de l'entreprise | 1 (Junior) à 5 (Direction) |
        | **YearsAtCompany** | Numérique | Ancienneté consécutive dans la société | 0 à 40 années |
        | **MonthlyIncome** | Numérique | Rémunération brute mensuelle | ~2 500 à ~30 000 MAD |
        | **JobSatisfaction** | Numérique ordinal | Niveau de satisfaction au travail | 1 (Très faible) à 4 (Très satisfaisant) |
        | **WorkLifeBalance** | Numérique ordinal | Équilibre perçu entre vie professionnelle et vie privée | 1 (Mauvais) à 4 (Optimal) |
        | **OverTime** | Catégoriel | Réalisation fréquente d'heures supplémentaires | `Yes` / `No` |
        | **DistanceFromHome** | Numérique | Distance kilométrique domicile-travail | 1 à 50 km |
        | **PromotionLast5Years** | Catégoriel | Promotion obtenue au cours des 5 dernières années | `Yes` / `No` |
        | **PerformanceRating** | Numérique ordinal | Évaluation annuelle des performances | 1 (Insuffisant) à 4 (Remarquable) |
        | **TrainingHoursLastYear** | Numérique | Heures de formation professionnelle reçues | 0 à 35 heures |
        | **Attrition (Cible)** | Catégoriel binaire | Statut de départ volontaire de l'employé | `Yes` (Démissionnaire) / `No` (Fidélisé) |
        """
    )

# ── Tab 2: Machine Learning Models ─────────────────────────────────────
with tab_models:
    st.markdown("#### 🤖 Les 6 Modèles Évalués dans le Benchmark")
    st.markdown(
        """
        Conformément aux directives du projet, **seuls les algorithmes classiques de Data Mining / Machine Learning** 
        ont été employés (aucun grand modèle de langage ni réseau profond n'est utilisé en tant qu'oracle prédictif).

        1. **Zero-R (Modèle Naïf de Référence) :**
           - *Principe :* Affecte systématiquement à tout individu la classe majoritaire observée dans la population d'entraînement (`Attrition = No`).
           - *Objectif :* Établit la ligne de base minimale indispensable pour vérifier qu'un modèle apprend une structure non triviale.

        2. **K-Plus Proches Voisins (K-Nearest Neighbors - KNN) :**
           - *Principe :* Prédit le statut d'un collaborateur en fonction de la majorité constatée chez ses *k* voisins les plus proches dans l'espace multidimensionnel normalisé (StandardScaler).
           - *Hyperparamètres :* Nombre de voisins `k`, métriques de distance (Euclidienne, Manhattan), pondération par l'inverse de la distance.

        3. **Arbre de Décision (Decision Tree - CART) :**
           - *Principe :* Construit une partition récursive de l'espace par des règles de décision transparentes basées sur le gain d'information (Critères de Gini ou d'Entropie).
           - *Hyperparamètres :* Profondeur maximale (`max_depth`), taille minimale de feuille (`min_samples_leaf`).

        4. **Forêt Aléatoire (Random Forest) :**
           - *Principe :* Méthode ensembliste par ensachage (*bagging*) combinant plusieurs dizaines d'arbres décorrélés pour réduire la variance et offrir une excellente robustesse au surapprentissage.
           - *Hyperparamètres :* Nombre d'estimateurs, profondeur maximale, fractionnement aléatoire.

        5. **Classifieur Naïf Bayesien (Gaussian Naive Bayes) :**
           - *Principe :* Modèle probabiliste fondé sur le théorème de Bayes sous l'hypothèse de conditionnelle indépendance des variables explicatives sachant la classe.
           - *Hyperparamètres :* Lissage de variance (`var_smoothing`).

        6. **Machine à Vecteurs de Support (Support Vector Machine - SVM) :**
           - *Principe :* Recherche l'hyperplan optimal maximisant la marge entre les classes dans un espace de Hilbert via des noyaux (Kernel RBF ou Linéaire).
           - *Hyperparamètres :* Coefficient de régularisation `C`, coefficient de noyau `gamma`.
        """
    )

# ── Tab 3: Evaluation Metrics ──────────────────────────────────────────
with tab_metrics:
    st.markdown("#### 📐 Métriques d'Évaluation Rigoureuses")
    st.markdown(
        """
        Le jeu de données présentant un léger déséquilibre de classe (taux d'attrition d'environ 15% à 20%), 
        l'évaluation ne repose pas sur la seule **Accuracy**.

        - **Recall (Sensibilité) :**
          $$\\text{Recall} = \\frac{VP}{VP + FN}$$
          *Importance RH :* Maximise la détection des collaborateurs qui vont réellement partir (minimise les départs manqués).

        - **Precision :**
          $$\\text{Precision} = \\frac{VP}{VP + FP}$$
          *Importance RH :* Évite les fausses alertes pour ne pas mobiliser inutilement des ressources RH.

        - **F1-Score (Métrique d'Arbitrage Principale) :**
          $$F1 = 2 \\times \\frac{\\text{Precision} \\times \\text{Recall}}{\\text{Precision} + \\text{Recall}}$$
          *Rôle :* Moyenne harmonique conciliant fidélité de détection et pureté des prédictions.

        - **AUC-ROC (Area Under the Curve) :**
          Mesure la capacité discriminante globale du modèle à tous les seuils de décision possibles indépendamment du seuil par défaut à 0.5.
        """
    )

# ── Tab 4: Ethics & Legal ──────────────────────────────────────────────
with tab_ethics:
    st.markdown("#### ⚖️ Cadre Éthique, RGPD & Responsabilité Managériale")
    st.markdown(
        """
        > ⚠️ **Avertissement Déontologique Important**
        >
        > Ce projet s'inscrit exclusivement dans un **cadre académique et d'apprentissage des techniques de Data Mining**.
        > Le jeu de données utilisé est issu d'une **simulation synthétique** et ne correspond pas à des employés réels.

        ##### Principes directeurs de l'IA appliquée aux Ressources Humaines :
        1. **Non-automatisation des décisions RH :** Les scores fournis par cette application constituent un *outil d'aide à la réflexion* et ne doivent en aucun cas fonder automatiquement un licenciement, une non-promotion ou une mise à l'écart.
        2. **Prévention et Bienveillance :** La finalité légitime de l'analyse prédictive d'attrition est l'amélioration de l'environnement de travail (réduction de la charge mentale, aménagement des horaires, reconnaissance professionnelle).
        3. **Transparence et Explicabilité :** L'intégration des décompositions **SHAP** et de l'importance des variables garantit que le modèle n'opère jamais en boîte noire fermée.
        """
    )


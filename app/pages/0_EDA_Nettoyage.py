"""0_EDA_Nettoyage.py — Exploratory Data Analysis & Data Cleaning page.

7 tabs:
  a) Aperçu          — shape, dtypes, head, descriptive stats
  b) Qualité         — missing values, duplicates, constant cols, outliers
  c) Nettoyage       — before/after comparison, cleaning steps
  d) Univariée       — histograms / bar charts per variable
  e) Bivariée        — relationship of each feature with Attrition
  f) Corrélations    — heatmap, top corr with target, class imbalance
  g) Export          — download cleaned CSV
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from scipy import stats as scipy_stats

# ── Path setup ──────────────────────────────────────────────────────────────
APP_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = APP_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils import (
    COLOR_MAP,
    COLOR_NO,
    COLOR_WARN,
    COLOR_YES,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    TARGET,
    ID_COL,
    PLOTLY_COLORWAY,
    PLOTLY_TEMPLATE,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    kpi_card,
    load_css,
    load_data,
    render_sidebar,
    section_header,
)
from app.cleaning import clean_data, detect_outliers_iqr

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDA & Nettoyage — Attrition RH",
    page_icon="🔬",
    layout="wide",
)
load_css()

# ── Load data ────────────────────────────────────────────────────────────────
raw_df = load_data()
if raw_df is None:
    st.error("❌ Fichier de données introuvable. Vérifiez `data/raw/Employee_Attrition_DataSet.csv`.")
    st.stop()

# ── Sidebar (without global filters — EDA uses raw data) ────────────────────
render_sidebar(df=raw_df, show_filters=False)

# ── Cached cleaning ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def get_cleaned(df: pd.DataFrame):
    return clean_data(df)


# ── Page header ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background:linear-gradient(135deg,#4F46E5 0%,#06B6D4 100%);
                border-radius:1rem;padding:1.6rem 2rem;margin-bottom:1.5rem;color:#fff;">
        <h2 style="margin:0;font-size:1.8rem;">🔬 EDA & Nettoyage des Données</h2>
        <p style="margin:0.4rem 0 0;opacity:.85;font-size:1rem;">
            Exploration visuelle, contrôle qualité et préparation du dataset Employee Attrition
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Top KPIs ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    kpi_card("Lignes", f"{len(raw_df):,}", border_color=PRIMARY_COLOR)
with c2:
    kpi_card("Colonnes", raw_df.shape[1], border_color=SECONDARY_COLOR)
with c3:
    kpi_card("Numériques", len(NUMERICAL_FEATURES), border_color="#10B981")
with c4:
    kpi_card("Catégorielles", len(CATEGORICAL_FEATURES), border_color="#F59E0B")
with c5:
    taux = raw_df[TARGET].value_counts(normalize=True).get("Yes", 0) * 100
    kpi_card("Taux Attrition", f"{taux:.1f} %", border_color=COLOR_YES)

st.markdown("<div style='margin-bottom:1rem;'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════════════════
(
    tab_apercu,
    tab_qualite,
    tab_nettoyage,
    tab_uni,
    tab_bi,
    tab_corr,
    tab_export,
) = st.tabs([
    "📋 Aperçu",
    "🔍 Qualité",
    "🧹 Nettoyage",
    "📊 Univariée",
    "🔗 Bivariée",
    "🌡️ Corrélations",
    "📥 Export",
])


# ─────────────────────────────────────────────────────────────────────────────
# a) APERÇU
# ─────────────────────────────────────────────────────────────────────────────
with tab_apercu:
    section_header("Aperçu du dataset", "Dimensions, types et statistiques descriptives", "📋")

    with st.container(border=True):
        st.markdown("#### 🗂️ Structure du dataset")
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f"- **Lignes :** {raw_df.shape[0]:,}")
            st.markdown(f"- **Colonnes :** {raw_df.shape[1]}")
            st.markdown(f"- **Mémoire :** {raw_df.memory_usage(deep=True).sum() / 1024:.1f} Ko")
        with col_right:
            type_counts = raw_df.dtypes.value_counts().reset_index()
            type_counts.columns = ["Type", "Nb colonnes"]
            st.dataframe(type_counts, use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.markdown("#### 🔎 Types de colonnes")
        dtype_df = pd.DataFrame({
            "Colonne": raw_df.columns,
            "Type": raw_df.dtypes.astype(str).values,
            "Valeurs uniques": [raw_df[c].nunique() for c in raw_df.columns],
            "Exemple": [str(raw_df[c].iloc[0]) for c in raw_df.columns],
        })
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.markdown("#### 👀 Premières lignes")
        n_rows = st.slider("Nombre de lignes à afficher", 5, 50, 10, key="head_rows")
        st.dataframe(raw_df.head(n_rows), use_container_width=True)

    with st.container(border=True):
        st.markdown("#### 📐 Statistiques descriptives")
        desc = raw_df[NUMERICAL_FEATURES].describe().T.round(2)
        desc.index.name = "Variable"
        desc = desc.reset_index()
        st.dataframe(desc, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# b) QUALITÉ
# ─────────────────────────────────────────────────────────────────────────────
with tab_qualite:
    section_header("Qualité des données", "Valeurs manquantes, doublons, constantes, aberrants", "🔍")

    # Missing values
    with st.container(border=True):
        st.markdown("#### ❓ Valeurs manquantes")
        missing = raw_df.isna().sum().reset_index()
        missing.columns = ["Colonne", "Nb NaN"]
        missing["% NaN"] = (missing["Nb NaN"] / len(raw_df) * 100).round(2)
        missing = missing.sort_values("Nb NaN", ascending=False)

        total_nan = int(missing["Nb NaN"].sum())
        if total_nan == 0:
            st.success("✅ Aucune valeur manquante détectée dans le dataset.")
        else:
            st.warning(f"⚠️ {total_nan} valeur(s) manquante(s) détectée(s).")
            st.dataframe(missing[missing["Nb NaN"] > 0], use_container_width=True, hide_index=True)
            fig_nan = px.bar(
                missing[missing["Nb NaN"] > 0],
                x="Colonne", y="% NaN",
                title="Taux de valeurs manquantes par colonne",
                template=PLOTLY_TEMPLATE,
                color_discrete_sequence=[COLOR_YES],
            )
            st.plotly_chart(fig_nan, use_container_width=True)

    # Duplicates & constant cols
    col_dup, col_const = st.columns(2)
    with col_dup:
        with st.container(border=True):
            st.markdown("#### 🔁 Doublons")
            n_dup = int(raw_df.duplicated().sum())
            if n_dup == 0:
                st.success("✅ Aucun doublon détecté.")
            else:
                st.warning(f"⚠️ {n_dup} doublon(s) trouvé(s).")

    with col_const:
        with st.container(border=True):
            st.markdown("#### 📌 Colonnes constantes / identifiant")
            constant_cols = [c for c in raw_df.columns if raw_df[c].nunique() <= 1]
            id_cols = [c for c in raw_df.columns if "id" in c.lower()]
            if constant_cols:
                st.warning(f"Colonnes constantes : {constant_cols}")
            else:
                st.success("✅ Aucune colonne constante.")
            if id_cols:
                st.info(f"ℹ️ Colonnes identifiant à supprimer : **{id_cols}**")

    # Outliers
    with st.container(border=True):
        st.markdown("#### 📦 Valeurs aberrantes (méthode IQR × 1.5)")
        with st.spinner("Calcul des outliers en cours…"):
            outlier_df = detect_outliers_iqr(raw_df, NUMERICAL_FEATURES)
        st.dataframe(outlier_df, use_container_width=True, hide_index=True)

        selected_col = st.selectbox(
            "Variable à visualiser (boxplot)",
            NUMERICAL_FEATURES,
            key="outlier_box_col",
        )
        fig_box = px.box(
            raw_df, y=selected_col, color=TARGET,
            color_discrete_map=COLOR_MAP,
            title=f"Boxplot — {selected_col} par statut d'attrition",
            template=PLOTLY_TEMPLATE,
            points="outliers",
        )
        fig_box.update_layout(margin=dict(t=50, b=20))
        st.plotly_chart(fig_box, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# c) NETTOYAGE
# ─────────────────────────────────────────────────────────────────────────────
with tab_nettoyage:
    section_header("Nettoyage des données", "Étapes appliquées et comparaison avant/après", "🧹")

    with st.spinner("Application du pipeline de nettoyage…"):
        cleaned_df, report = get_cleaned(raw_df)

    # Steps list
    with st.container(border=True):
        st.markdown("#### 🔧 Étapes de nettoyage appliquées")
        for step in report.get("steps", []):
            st.markdown(step)

    # Before / After comparison
    with st.container(border=True):
        st.markdown("#### 📊 Comparaison Avant / Après")
        comparison = pd.DataFrame({
            "Métrique": ["Nombre de lignes", "Nombre de colonnes", "Valeurs manquantes"],
            "Avant": [report["rows_before"], report["cols_before"], report["nan_before"]],
            "Après": [report["rows_after"], report["cols_after"], report["nan_after"]],
        })
        comparison["Δ"] = comparison["Après"] - comparison["Avant"]
        st.dataframe(comparison, use_container_width=True, hide_index=True)

        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name="Avant", x=comparison["Métrique"], y=comparison["Avant"],
                                   marker_color=SECONDARY_COLOR))
        fig_comp.add_trace(go.Bar(name="Après", x=comparison["Métrique"], y=comparison["Après"],
                                   marker_color=PRIMARY_COLOR))
        fig_comp.update_layout(
            barmode="group", template=PLOTLY_TEMPLATE,
            title="Avant vs Après nettoyage",
            margin=dict(t=50, b=20), height=350,
        )
        st.plotly_chart(fig_comp, use_container_width=True)

    # Outliers capped detail
    if report.get("outliers_capped"):
        with st.container(border=True):
            st.markdown("#### 📦 Détail des outliers écrêtés")
            oc_df = pd.DataFrame(list(report["outliers_capped"].items()),
                                  columns=["Variable", "Valeurs corrigées"])
            st.dataframe(oc_df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Aucun outlier écrêté (toutes les valeurs dans les bornes IQR).")

    with st.container(border=True):
        st.markdown("#### 👀 Aperçu du dataset nettoyé")
        st.dataframe(cleaned_df.head(10), use_container_width=True)
        st.caption(f"Dataset nettoyé : **{cleaned_df.shape[0]:,} lignes × {cleaned_df.shape[1]} colonnes**")


# ─────────────────────────────────────────────────────────────────────────────
# d) ANALYSE UNIVARIÉE
# ─────────────────────────────────────────────────────────────────────────────
with tab_uni:
    section_header("Analyse Univariée", "Distribution de chaque variable", "📊")

    all_vars = NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    selected_var = st.selectbox("Choisir une variable", all_vars, key="uni_var")

    if selected_var in NUMERICAL_FEATURES:
        col_hist, col_stats = st.columns([3, 1])
        with col_hist:
            with st.container(border=True):
                fig_hist = px.histogram(
                    raw_df, x=selected_var,
                    marginal="box",
                    color_discrete_sequence=[PRIMARY_COLOR],
                    title=f"Distribution de {selected_var}",
                    template=PLOTLY_TEMPLATE,
                    nbins=40,
                )
                fig_hist.update_layout(margin=dict(t=50, b=20))
                st.plotly_chart(fig_hist, use_container_width=True)

        with col_stats:
            with st.container(border=True):
                s = raw_df[selected_var]
                st.metric("Moyenne", f"{s.mean():.2f}")
                st.metric("Médiane", f"{s.median():.2f}")
                st.metric("Écart-type", f"{s.std():.2f}")
                sk = s.skew()
                sk_label = "✅ Symétrique" if abs(sk) < 0.5 else ("📈 Étalé droite" if sk > 0 else "📉 Étalé gauche")
                st.metric("Asymétrie (skew)", f"{sk:.2f}", delta=sk_label, delta_color="off")
                st.metric("Min", f"{s.min():.2f}")
                st.metric("Max", f"{s.max():.2f}")

    else:  # Categorical
        with st.container(border=True):
            vc = raw_df[selected_var].value_counts().reset_index()
            vc.columns = [selected_var, "Effectif"]
            vc["Pourcentage"] = (vc["Effectif"] / len(raw_df) * 100).round(1)

            fig_bar = px.bar(
                vc, x=selected_var, y="Effectif",
                text="Pourcentage",
                color=selected_var,
                color_discrete_sequence=PLOTLY_COLORWAY,
                title=f"Répartition de {selected_var}",
                template=PLOTLY_TEMPLATE,
            )
            fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_bar.update_layout(showlegend=False, margin=dict(t=50, b=20))
            st.plotly_chart(fig_bar, use_container_width=True)
            st.dataframe(vc, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# e) ANALYSE BIVARIÉE
# ─────────────────────────────────────────────────────────────────────────────
with tab_bi:
    section_header(
        "Analyse Bivariée",
        "Relation de chaque variable avec la cible Attrition",
        "🔗",
    )

    sub_num, sub_cat = st.tabs(["Numériques × Attrition", "Catégorielles × Attrition"])

    # ── Numerical × Attrition ────────────────────────────────────────────
    with sub_num:
        sel_num = st.selectbox("Variable numérique", NUMERICAL_FEATURES, key="bi_num_var")
        with st.container(border=True):
            fig_bx = px.box(
                raw_df, x=TARGET, y=sel_num,
                color=TARGET,
                color_discrete_map=COLOR_MAP,
                title=f"{sel_num} selon le statut d'Attrition",
                template=PLOTLY_TEMPLATE,
                points="outliers",
            )
            fig_bx.update_layout(margin=dict(t=50, b=20))
            st.plotly_chart(fig_bx, use_container_width=True)

        # T-test
        g_no = raw_df.loc[raw_df[TARGET] == "No", sel_num].dropna()
        g_yes = raw_df.loc[raw_df[TARGET] == "Yes", sel_num].dropna()
        _, p_val = scipy_stats.ttest_ind(g_no, g_yes, equal_var=False)
        sig = "✅ Différence statistiquement significative" if p_val < 0.05 else "❌ Différence non significative"
        with st.container(border=True):
            col_a, col_b, col_c = st.columns(3)
            col_a.metric(f"Moyenne ({TARGET}=No)", f"{g_no.mean():.2f}")
            col_b.metric(f"Moyenne ({TARGET}=Yes)", f"{g_yes.mean():.2f}")
            col_c.metric("p-valeur (t-test Welch)", f"{p_val:.4f}")
            st.markdown(f"**Test t de Welch :** {sig} (α = 0.05)")

    # ── Categorical × Attrition ──────────────────────────────────────────
    with sub_cat:
        sel_cat = st.selectbox("Variable catégorielle", CATEGORICAL_FEATURES, key="bi_cat_var")
        cross = pd.crosstab(raw_df[sel_cat], raw_df[TARGET])
        cross_pct = cross.div(cross.sum(axis=1), axis=0) * 100

        with st.container(border=True):
            fig_stacked = go.Figure()
            for col_name, color in zip(["No", "Yes"], [COLOR_NO, COLOR_YES]):
                if col_name in cross_pct.columns:
                    fig_stacked.add_trace(go.Bar(
                        name=f"Attrition={col_name}",
                        x=cross_pct.index.astype(str),
                        y=cross_pct[col_name].values,
                        marker_color=color,
                        text=cross_pct[col_name].round(1).astype(str) + "%",
                        textposition="inside",
                    ))
            fig_stacked.update_layout(
                barmode="stack",
                title=f"Taux d'attrition par {sel_cat}",
                yaxis_title="Pourcentage (%)",
                xaxis_title=sel_cat,
                template=PLOTLY_TEMPLATE,
                margin=dict(t=50, b=20),
            )
            st.plotly_chart(fig_stacked, use_container_width=True)

        # Chi2 test
        with st.container(border=True):
            st.markdown("#### 📐 Taux d'attrition par modalité")
            rate_df = cross_pct.reset_index()
            rate_df.columns = [sel_cat] + [f"% {c}" for c in cross_pct.columns]
            rate_df = rate_df.round(1)
            st.dataframe(rate_df, use_container_width=True, hide_index=True)

            try:
                from scipy.stats import chi2_contingency
                chi2, p_chi2, _, _ = chi2_contingency(cross)
                sig_chi = "✅ Association statistiquement significative" if p_chi2 < 0.05 else "❌ Pas d'association significative"
                col_x, col_y = st.columns(2)
                col_x.metric("Statistique χ²", f"{chi2:.2f}")
                col_y.metric("p-valeur (χ²)", f"{p_chi2:.4f}")
                st.markdown(f"**Test du Chi² :** {sig_chi} (α = 0.05)")
            except Exception:
                pass


# ─────────────────────────────────────────────────────────────────────────────
# f) CORRÉLATIONS
# ─────────────────────────────────────────────────────────────────────────────
with tab_corr:
    section_header("Corrélations & Déséquilibre de Classes", icon="🌡️")

    # Class imbalance
    with st.container(border=True):
        st.markdown("#### ⚖️ Déséquilibre de classes (Attrition)")
        vc_target = raw_df[TARGET].value_counts()
        fig_donut = go.Figure(go.Pie(
            labels=vc_target.index,
            values=vc_target.values,
            hole=0.55,
            marker_colors=[COLOR_NO, COLOR_YES],
            textinfo="label+percent+value",
        ))
        fig_donut.update_layout(
            template=PLOTLY_TEMPLATE,
            title="Répartition de la variable cible (Attrition)",
            margin=dict(t=60, b=20),
            height=350,
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        ratio = vc_target.get("No", 0) / max(vc_target.get("Yes", 1), 1)
        st.warning(
            f"⚠️ Dataset **très déséquilibré** : ratio No/Yes ≈ {ratio:.1f}:1. "
            "Des techniques de rééchantillonnage (SMOTE, class_weight) sont recommandées."
        )

    # Correlation heatmap (numerical features only)
    with st.container(border=True):
        st.markdown("#### 🌡️ Heatmap de corrélation")
        corr_df = raw_df[NUMERICAL_FEATURES].corr()
        fig_heat = px.imshow(
            corr_df,
            text_auto=".2f",
            color_continuous_scale="RdBu_r",
            zmin=-1, zmax=1,
            title="Matrice de corrélation (variables numériques)",
            template=PLOTLY_TEMPLATE,
            aspect="auto",
        )
        fig_heat.update_layout(margin=dict(t=60, b=20), height=500)
        st.plotly_chart(fig_heat, use_container_width=True)

    # Top correlations with target
    with st.container(border=True):
        st.markdown("#### 🎯 Corrélations avec la cible (Attrition)")
        df_corr_target = raw_df.copy()
        df_corr_target["Attrition_num"] = (df_corr_target[TARGET] == "Yes").astype(int)
        corr_with_target = (
            df_corr_target[NUMERICAL_FEATURES + ["Attrition_num"]]
            .corr()["Attrition_num"]
            .drop("Attrition_num")
            .sort_values(key=abs, ascending=False)
        )
        corr_df2 = corr_with_target.reset_index()
        corr_df2.columns = ["Variable", "Corrélation avec Attrition"]
        corr_df2["Corrélation avec Attrition"] = corr_df2["Corrélation avec Attrition"].round(4)

        fig_corr_bar = px.bar(
            corr_df2, x="Variable", y="Corrélation avec Attrition",
            color="Corrélation avec Attrition",
            color_continuous_scale="RdBu_r",
            title="Corrélation de Pearson des variables numériques avec Attrition",
            template=PLOTLY_TEMPLATE,
        )
        fig_corr_bar.add_hline(y=0, line_dash="dash", line_color="gray")
        fig_corr_bar.update_layout(margin=dict(t=50, b=20))
        st.plotly_chart(fig_corr_bar, use_container_width=True)
        st.dataframe(corr_df2, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# g) EXPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab_export:
    section_header("Export du Dataset Nettoyé", "Téléchargez le dataset prêt pour la modélisation", "📥")

    with st.spinner("Préparation du dataset nettoyé…"):
        cleaned_df_exp, report_exp = get_cleaned(raw_df)

    with st.container(border=True):
        st.markdown("#### 📋 Résumé du nettoyage")
        for step in report_exp.get("steps", []):
            st.markdown(step)

    col_meta1, col_meta2, col_meta3 = st.columns(3)
    with col_meta1:
        kpi_card("Lignes (après)", f"{report_exp['rows_after']:,}", border_color=PRIMARY_COLOR)
    with col_meta2:
        kpi_card("Colonnes (après)", report_exp["cols_after"], border_color=SECONDARY_COLOR)
    with col_meta3:
        kpi_card("NaN restants", report_exp["nan_after"], border_color=COLOR_NO)

    with st.container(border=True):
        st.markdown("#### 👀 Aperçu du dataset nettoyé")
        st.dataframe(cleaned_df_exp.head(20), use_container_width=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # Convert categorical columns back to object for CSV compatibility
    csv_df = cleaned_df_exp.copy()
    for col in csv_df.select_dtypes("category").columns:
        csv_df[col] = csv_df[col].astype(str)

    csv_bytes = csv_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Télécharger le dataset nettoyé (CSV)",
        data=csv_bytes,
        file_name="Employee_Attrition_Cleaned.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.success(f"✅ Dataset prêt : **{report_exp['rows_after']:,} lignes × {report_exp['cols_after']} colonnes**, 0 NaN.")

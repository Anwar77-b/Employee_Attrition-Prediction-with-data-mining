"""Data cleaning logic for the Employee Attrition dataset.

This module provides a reusable clean_data() function that is compatible
with Streamlit's @st.cache_data decorator (pure function, no ST calls).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Columns to drop because they carry no predictive information
_ID_COLUMNS = ["EmployeeID"]

# Numerical columns on which to cap outliers (IQR method)
_NUMERICAL = [
    "Age", "JobLevel", "YearsAtCompany", "MonthlyIncome",
    "JobSatisfaction", "WorkLifeBalance", "DistanceFromHome",
    "PerformanceRating", "TrainingHoursLastYear",
]


def detect_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Return a DataFrame with one row per column showing IQR outlier statistics.

    Columns: variable, Q1, Q3, IQR, lower_bound, upper_bound, n_outliers, pct_outliers
    """
    rows = []
    for col in columns:
        if col not in df.columns:
            continue
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        mask = (df[col] < lower) | (df[col] > upper)
        n = int(mask.sum())
        rows.append({
            "Variable": col,
            "Q1": round(q1, 2),
            "Q3": round(q3, 2),
            "IQR": round(iqr, 2),
            "Borne inf.": round(lower, 2),
            "Borne sup.": round(upper, 2),
            "Nbre aberrants": n,
            "% aberrants": round(100 * n / max(len(df), 1), 2),
        })
    return pd.DataFrame(rows)


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clean the raw dataset and return (cleaned_df, report_dict).

    Steps applied (in order):
    1. Drop ID columns (EmployeeID)
    2. Remove duplicate rows
    3. Drop fully-constant columns
    4. Treat missing values (drop rows with NaN after dropping ID)
    5. Cap outliers on numerical columns using 1.5 × IQR method
    6. Correct dtypes (categorical → category)

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame (as loaded from CSV).

    Returns
    -------
    cleaned : pd.DataFrame
        The cleaned DataFrame.
    report : dict
        A dictionary with before/after metrics and step descriptions.
    """
    report: dict = {}

    # ── Before metrics ──────────────────────────────────────────────────
    report["rows_before"] = len(df)
    report["cols_before"] = len(df.columns)
    report["nan_before"] = int(df.isna().sum().sum())
    report["duplicates_before"] = int(df.duplicated().sum())

    cleaned = df.copy()

    # ── Step 1: Drop ID columns ──────────────────────────────────────────
    id_cols_present = [c for c in _ID_COLUMNS if c in cleaned.columns]
    cleaned = cleaned.drop(columns=id_cols_present)
    report["dropped_id_cols"] = id_cols_present

    # ── Step 2: Remove duplicates ────────────────────────────────────────
    n_before_dup = len(cleaned)
    cleaned = cleaned.drop_duplicates()
    report["duplicates_removed"] = n_before_dup - len(cleaned)

    # ── Step 3: Drop constant columns ───────────────────────────────────
    constant_cols = [c for c in cleaned.columns if cleaned[c].nunique(dropna=False) <= 1]
    if constant_cols:
        cleaned = cleaned.drop(columns=constant_cols)
    report["dropped_constant_cols"] = constant_cols

    # ── Step 4: Handle missing values ───────────────────────────────────
    nan_per_col_before = cleaned.isna().sum()
    # For numerical → median imputation; for categorical → mode imputation
    for col in cleaned.columns:
        if cleaned[col].isna().sum() == 0:
            continue
        if cleaned[col].dtype in [np.float64, np.int64, float, int]:
            cleaned[col] = cleaned[col].fillna(cleaned[col].median())
        else:
            mode_val = cleaned[col].mode()
            if len(mode_val) > 0:
                cleaned[col] = cleaned[col].fillna(mode_val[0])
    report["nan_imputed"] = int(nan_per_col_before.sum())

    # ── Step 5: Cap outliers (IQR) ───────────────────────────────────────
    num_cols = [c for c in _NUMERICAL if c in cleaned.columns]
    outliers_capped = {}
    for col in num_cols:
        q1 = cleaned[col].quantile(0.25)
        q3 = cleaned[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        n_outliers = int(((cleaned[col] < lower) | (cleaned[col] > upper)).sum())
        if n_outliers > 0:
            cleaned[col] = cleaned[col].clip(lower=lower, upper=upper)
            outliers_capped[col] = n_outliers
    report["outliers_capped"] = outliers_capped
    report["total_outliers_capped"] = sum(outliers_capped.values())

    # ── Step 6: Correct dtypes ───────────────────────────────────────────
    cat_cols = [c for c in cleaned.columns if cleaned[c].dtype == object]
    for col in cat_cols:
        cleaned[col] = cleaned[col].astype("category")
    report["categorical_encoded"] = cat_cols

    # ── After metrics ────────────────────────────────────────────────────
    report["rows_after"] = len(cleaned)
    report["cols_after"] = len(cleaned.columns)
    report["nan_after"] = int(cleaned.isna().sum().sum())

    # ── Human-readable step list ─────────────────────────────────────────
    report["steps"] = [
        f"✅ Suppression des colonnes identifiant : {id_cols_present or 'aucune'}",
        f"✅ Suppression des doublons : {report['duplicates_removed']} ligne(s) supprimée(s)",
        f"✅ Suppression des colonnes constantes : {constant_cols or 'aucune'}",
        f"✅ Traitement des valeurs manquantes : {report['nan_imputed']} valeur(s) imputée(s) (médiane/mode)",
        f"✅ Écrêtage des valeurs aberrantes (IQR ×1.5) : {report['total_outliers_capped']} valeur(s) corrigée(s)",
        f"✅ Encodage des types catégoriels : {len(cat_cols)} colonne(s)",
    ]

    return cleaned, report

"""Plotly chart helpers for the Employee Attrition console.

Every figure uses the console palette declared in :mod:`app.theme`.  The
module never reads artifacts, never modifies data and never introduces a new
feature definition.
"""
from __future__ import annotations

from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy import stats

from app.theme import (
    ACCENT_AMBER,
    ACCENT_CYAN,
    ACCENT_GREEN,
    ACCENT_ROSE,
    BG_PANEL,
    BORDER,
    TEXT_MUTED,
    TEXT_PRIMARY,
)

_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor=BG_PANEL,
    font=dict(family="monospace", size=11, color=TEXT_PRIMARY),
    margin=dict(l=50, r=20, t=40, b=50),
    hoverlabel=dict(bgcolor=BG_PANEL, bordercolor=BORDER, font_size=11),
)


def _finish(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(**_LAYOUT, height=height)
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER)
    return fig


def attrition_donut(df: pd.DataFrame, target: str = "Attrition") -> go.Figure:
    """Donut chart for the No/Yes repartition of the target."""
    counts = df[target].value_counts()
    labels = [str(v) for v in counts.index]
    values = counts.to_numpy()
    colors = [ACCENT_GREEN if label.upper() == "NO" else ACCENT_ROSE for label in labels]
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color=BG_PANEL, width=2)),
            textinfo="label+percent",
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(showlegend=False)
    return _finish(fig)


def department_bar(df: pd.DataFrame, target: str = "Attrition") -> go.Figure:
    """Stacked counts of stays/departures by department."""
    grouped = df.groupby(["Department", target]).size().unstack(fill_value=0)
    fig = go.Figure()
    for value in grouped.columns:
        color = ACCENT_GREEN if str(value).upper() == "NO" else ACCENT_ROSE
        fig.add_trace(
            go.Bar(
                x=[str(v) for v in grouped.index],
                y=grouped[value].to_numpy(),
                name=str(value),
                marker_color=color,
            )
        )
    fig.update_layout(barmode="stack", legend=dict(orientation="h", y=1.1))
    return _finish(fig)


def histogram_with_kde(values: pd.Series, name: str, bins: int = 35) -> go.Figure:
    """Histogram with a smooth density estimate for one numeric variable."""
    series = pd.Series(values)
    clean = series[pd.notna(series)]
    fig = go.Figure(
        go.Histogram(
            x=clean,
            nbinsx=bins,
            marker_color=ACCENT_CYAN,
            opacity=0.75,
            name=name,
        )
    )
    clean_numeric = pd.to_numeric(clean, errors="coerce")
    clean_numeric = clean_numeric[clean_numeric.notna()]
    if len(clean_numeric) > 5 and float(clean_numeric.std()) > 0:
        grid = np.linspace(float(clean_numeric.min()), float(clean_numeric.max()), 160)
        density = stats.gaussian_kde(clean_numeric.to_numpy())(grid)
        scaled = density * len(clean_numeric) * (float(clean_numeric.max()) - float(clean_numeric.min())) / bins
        fig.add_trace(
            go.Scatter(
                x=grid,
                y=scaled,
                mode="lines",
                name="Densité",
                line=dict(color=ACCENT_GREEN, width=2),
            )
        )
    fig.update_layout(showlegend=False)
    return _finish(fig)


def correlation_heatmap(df: pd.DataFrame, columns: Sequence[str]) -> go.Figure:
    """Spearman heatmap; the caller supplies columns already cleared of id/target."""
    excluded = {"EmployeeID", "Attrition"}
    selected = [c for c in columns if c in df.columns and c not in excluded]
    corr = df[selected].corr(method="spearman")
    fig = go.Figure(
        go.Heatmap(
            z=corr.to_numpy(),
            x=list(corr.columns),
            y=list(corr.index),
            colorscale=[[0, ACCENT_ROSE], [0.5, BG_PANEL], [1, ACCENT_CYAN]],
            zmin=-1,
            zmax=1,
            colorbar=dict(title="ρ"),
            hovertemplate="%{y} ↔ %{x} : %{z:.2f}<extra></extra>",
        )
    )
    return _finish(fig, height=420)


def outlier_bar(report: pd.DataFrame) -> go.Figure:
    """Bar chart of the versioned outlier report by method and variable."""
    work = report.copy()
    labels = work["methode"].astype(str) + " · " + work["variable"].astype(str)
    colors = {
        "Z-score": ACCENT_CYAN,
        "IQR": ACCENT_GREEN,
        "Isolation Forest": ACCENT_AMBER,
        "LOF": ACCENT_ROSE,
    }
    marker_colors = [colors.get(str(m), ACCENT_CYAN) for m in work["methode"]]
    fig = go.Figure(
        go.Bar(
            x=labels,
            y=work["n_outliers"].astype(int),
            marker_color=marker_colors,
            hovertemplate="%{x}<br>Occurrences : %{y}<extra></extra>",
        )
    )
    fig.update_layout(xaxis_tickangle=-35, margin=dict(l=50, r=20, t=30, b=130))
    return _finish(fig, height=420)


def metric_comparison_bar(metrics: pd.DataFrame, column: str = "F1-Score") -> go.Figure:
    """Horizontal bar chart comparing models on a selected metric."""
    ordered = metrics.sort_values(column, ascending=True)
    fig = go.Figure(
        go.Bar(
            x=ordered[column].astype(float),
            y=ordered["Modèle"].astype(str),
            orientation="h",
            marker_color=ACCENT_CYAN,
            text=ordered[column].map(lambda v: f"{float(v):.4f}"),
            textposition="outside",
        )
    )
    fig.update_layout(xaxis_range=[0, float(ordered[column].max()) * 1.18 + 0.01])
    return _finish(fig)


def confusion_matrix_heatmap(matrix: Iterable[Iterable[int]], labels: Sequence[str]) -> go.Figure:
    """Display a 2x2 confusion matrix with explicit No/Yes order."""
    array = np.asarray(list(matrix), dtype=int)
    fig = go.Figure(
        go.Heatmap(
            z=array,
            x=[f"Prédit {lab}" for lab in labels],
            y=[f"Réel {lab}" for lab in labels],
            colorscale=[[0, BG_PANEL], [1, ACCENT_CYAN]],
            text=array,
            texttemplate="%{text}",
            showscale=False,
        )
    )
    return _finish(fig, height=320)


def feature_importance_bar(importances: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """Horizontal importance chart sorted from weakest to strongest."""
    work = importances.sort_values("Importance", ascending=True).tail(top_n)
    fig = go.Figure(
        go.Bar(
            x=work["Importance"].astype(float),
            y=work["Variable"].astype(str),
            orientation="h",
            marker_color=ACCENT_GREEN,
            text=work["Importance"].map(lambda v: f"{float(v):.4f}"),
            textposition="outside",
        )
    )
    return _finish(fig)


def probability_bar_chart(probabilities: Sequence[float], labels: Optional[Sequence[str]] = None) -> go.Figure:
    """Bar chart of attrition probabilities with the risk colour scale."""
    values = np.asarray(list(probabilities), dtype=float)
    names = list(labels) if labels is not None else [f"Ligne {i + 1}" for i in range(len(values))]
    colors = [ACCENT_GREEN if v < 30 else ACCENT_AMBER if v < 60 else ACCENT_ROSE for v in values]
    fig = go.Figure(
        go.Bar(x=names, y=values, marker_color=colors, hovertemplate="%{x} : %{y:.1f}%<extra></extra>")
    )
    fig.update_layout(xaxis_tickangle=-30)
    return _finish(fig)


def risk_gauge(probability: float) -> go.Figure:
    """Compatibility wrapper around the shared gauge component."""
    from app.utils import gauge_chart

    return gauge_chart(probability)

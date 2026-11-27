"""Console visual theme for the Employee Attrition Streamlit application.

Call ``apply_theme()`` once near the top of every page, after
``st.set_page_config()``.  Every CSS selector lives in this module so that
the application keeps a single source of styling.
"""
from __future__ import annotations

from typing import Optional

import streamlit as st

# Palette -----------------------------------------------------------------
BG_PAGE = "#0A0E17"
BG_PANEL = "#101826"
BG_PANEL_ALT = "#0D1521"
BORDER = "#1F2C44"
ACCENT_CYAN = "#22D3EE"
ACCENT_GREEN = "#34D399"
ACCENT_AMBER = "#F2A93B"
ACCENT_ROSE = "#E85D75"
TEXT_PRIMARY = "#E6EDF7"
TEXT_MUTED = "#8FA3BF"
ACCENT_CYAN_DIM = "#1AA8C4"

_FONTS = (
    "@import url('https://fonts.googleapis.com/css2?"
    "family=JetBrains+Mono:wght@400;500;600&"
    "family=Inter:wght@400;500;600&display=swap');"
)

_CSS = """
/* ── Base ─────────────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
__FONTS__

:root {
  --bg-page: __BG_PAGE__;
  --bg-panel: __BG_PANEL__;
  --bg-panel-alt: __BG_PANEL_ALT__;
  --border: __BORDER__;
  --cyan: __CYAN__;
  --green: __GREEN__;
  --amber: __AMBER__;
  --rose: __ROSE__;
  --text: __TEXT__;
  --muted: __MUTED__;
  --mono: 'JetBrains Mono', 'Fira Code', ui-monospace, Menlo, Consolas, monospace;
  --sans: 'Inter', system-ui, 'Segoe UI', Roboto, sans-serif;
  --radius: 6px;
  --glow: 0 0 12px rgba(34,211,238,.18);
}

/* ── Page canvas and subtle grid ─────────────────────────────────────── */
[data-testid="stAppViewContainer"] > .main {
  background-color: var(--bg-page);
  background-image:
    linear-gradient(rgba(34,211,238,.035) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34,211,238,.035) 1px, transparent 1px);
  background-size: 40px 40px;
  color: var(--text);
  font-family: var(--sans);
}
[data-testid="stAppViewContainer"] .block-container {
  padding-top: 1.6rem !important;
  padding-bottom: 3rem !important;
  max-width: 1400px;
}
#MainMenu { visibility: hidden !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
header[data-testid="stHeader"] { background: transparent !important; border: none !important; }

/* ── Sidebar ──────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: #080D16 !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 1rem 0.8rem; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: var(--text) !important;
  font-family: var(--mono) !important;
  letter-spacing: .03em;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
  color: var(--muted) !important;
  font-family: var(--sans) !important;
  font-size: 0.82rem;
}
[data-testid="stSidebar"] hr { border-color: var(--border) !important; margin: 0.6rem 0; }
[data-testid="stSidebar"] [data-testid="stRadio"] label {
  display: flex;
  align-items: center;
  padding: 0.42rem 0.75rem;
  margin: 1px 0;
  border-radius: var(--radius);
  cursor: pointer;
  font-family: var(--mono) !important;
  font-size: 0.83rem !important;
  color: var(--muted) !important;
  transition: background .15s;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(34,211,238,.07);
  color: var(--text) !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
  position: absolute; opacity: 0; width: 1px; height: 1px; pointer-events: none;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked),
[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] {
  color: var(--cyan) !important;
  border-left: 3px solid var(--cyan);
  background: rgba(34,211,238,.08);
  padding-left: 0.6rem;
}

.rh-sidebar-header { display: flex; align-items: center; gap: 0.65rem; margin-bottom: 0.2rem; }
.rh-sidebar-icon {
  width: 42px; height: 42px; display: grid; place-items: center;
  border: 1px solid var(--border); border-radius: var(--radius);
  background: var(--bg-panel); font-size: 1.35rem;
}
.rh-sidebar-title {
  font-family: var(--mono) !important; font-size: 1rem !important;
  font-weight: 600; color: var(--text) !important; line-height: 1.2;
}
.rh-sidebar-subtitle {
  font-family: var(--sans) !important; font-size: 0.72rem !important;
  color: var(--muted) !important; margin-top: 0.1rem;
}
.rh-status-panel {
  background: var(--bg-panel); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 0.6rem 0.8rem; margin: 0.6rem 0 0.9rem;
}
.rh-status-caption {
  font-family: var(--mono); font-size: 0.68rem; text-transform: uppercase;
  letter-spacing: .1em; color: var(--muted); margin-bottom: 0.35rem;
}
.rh-status-row {
  display: flex; align-items: center; gap: 0.5rem;
  font-family: var(--mono); font-size: 0.78rem; color: var(--muted); margin: 0.2rem 0;
}
.rh-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; display: inline-block; }
.rh-dot-green { background: #2ecc71; box-shadow: 0 0 6px #2ecc71aa; }
.rh-dot-amber { background: var(--amber); box-shadow: 0 0 6px #f2a93baa; }
.rh-dot-red { background: var(--rose); box-shadow: 0 0 6px #e85d75aa; }
.rh-status-label { color: var(--text); }

/* ── Page headers ─────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] .block-container h1 {
  font-family: var(--mono) !important; font-size: 1.55rem !important;
  font-weight: 600; color: var(--text) !important; letter-spacing: .04em;
  padding-left: 0.9rem; border-left: 3px solid var(--cyan);
  margin-bottom: 0.1rem !important; text-shadow: 0 0 20px rgba(34,211,238,.22);
}
[data-testid="stAppViewContainer"] .block-container h2 {
  font-family: var(--mono) !important; font-size: 1.1rem !important;
  color: var(--text) !important; letter-spacing: .03em; margin-top: 1.4rem !important;
}
[data-testid="stAppViewContainer"] .block-container h3 {
  font-family: var(--mono) !important; font-size: 0.97rem !important;
  color: var(--cyan) !important;
}
[data-testid="stAppViewContainer"] .block-container h4,
[data-testid="stAppViewContainer"] .block-container h5 {
  color: var(--text) !important; font-family: var(--sans) !important;
}
[data-testid="stAppViewContainer"] .block-container p,
[data-testid="stAppViewContainer"] .block-container li {
  color: var(--text) !important;
}
[data-testid="stAppViewContainer"] .block-container [data-testid="stCaptionContainer"] p,
[data-testid="stAppViewContainer"] .block-container small {
  color: var(--muted) !important; font-size: 0.82rem !important;
}
.rh-page-divider {
  height: 1px; margin: 0.35rem 0 1rem 0; border: none;
  background: linear-gradient(90deg, var(--cyan) 0%, rgba(34,211,238,.15) 60%, transparent 100%);
  box-shadow: 0 0 8px rgba(34,211,238,.35);
}

/* ── Section headers and cards ───────────────────────────────────────── */
.section-header-container {
  margin: 1.5rem 0 1rem; padding: 0 0 0.85rem;
  border-bottom: 1px solid var(--border); position: relative;
}
.section-header-container::after {
  content: ""; position: absolute; left: 0; bottom: -1px;
  width: 58px; height: 2px; border-radius: 999px;
  background: linear-gradient(90deg, var(--cyan), transparent);
  box-shadow: 0 0 8px rgba(34,211,238,.4);
}
.section-header-title {
  font-family: var(--mono) !important; font-size: 1.2rem !important;
  color: var(--text) !important; margin: 0; display: flex; gap: 0.5rem;
}
.section-header-subtitle { color: var(--muted) !important; margin-top: 0.25rem; }

.kpi-card,
div[data-testid="stMetric"] {
  background: var(--bg-panel) !important;
  border: 1px solid var(--border) !important;
  border-top: 2px solid var(--cyan) !important;
  border-radius: var(--radius) !important;
  padding: 14px 16px !important;
  transition: box-shadow .2s, transform .2s;
  height: 100%;
}
.kpi-card:hover,
div[data-testid="stMetric"]:hover { box-shadow: var(--glow) !important; transform: translateY(-1px); }
.kpi-title, div[data-testid="stMetricLabel"] p {
  font-family: var(--sans) !important; font-size: 0.8rem !important;
  text-transform: uppercase; letter-spacing: .08em; color: var(--muted) !important;
}
.kpi-value, div[data-testid="stMetricValue"] {
  font-family: var(--mono) !important; font-size: 1.5rem !important;
  font-weight: 600; color: var(--text) !important;
}
.kpi-delta { font-family: var(--mono) !important; font-size: 0.78rem !important; margin-top: 0.35rem; }
.kpi-delta.positive { color: var(--green) !important; }
.kpi-delta.negative { color: var(--rose) !important; }
.kpi-delta.neutral { color: var(--muted) !important; }

.nav-card {
  background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; padding: 1.15rem !important;
  height: 100%; transition: border-color .15s, box-shadow .15s;
}
.nav-card:hover { border-color: var(--cyan) !important; box-shadow: var(--glow) !important; }
.nav-card-icon { font-size: 1.7rem; margin-bottom: 0.5rem; }
.nav-card-title { font-family: var(--mono) !important; color: var(--text) !important; font-size: 1rem !important; }
.nav-card-desc { color: var(--muted) !important; font-size: 0.85rem !important; line-height: 1.5; }

/* ── Alerts, tabs, expanders ─────────────────────────────────────────── */
[data-testid="stAlert"] {
  background: var(--bg-panel) !important; color: var(--text) !important;
  border-radius: var(--radius) !important; border-top: none !important;
  border-right: none !important; border-bottom: none !important;
  border-left: 3px solid var(--cyan) !important; padding: 0.7rem 1rem !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] div { color: var(--text) !important; font-size: 0.875rem !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
  background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
  background: transparent !important; border: none !important;
  border-bottom: 2px solid transparent !important; color: var(--muted) !important;
  font-family: var(--mono) !important; font-size: 0.82rem !important;
  padding: 0.5rem 1rem !important; margin-bottom: -1px;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover {
  color: var(--text) !important; border-bottom-color: var(--cyan) !important;
  background: rgba(34,211,238,.04) !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
  color: var(--cyan) !important; border-bottom: 2px solid var(--cyan) !important;
  background: rgba(34,211,238,.06) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding: 1rem 0 0 0 !important; }
[data-testid="stExpander"] {
  background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; margin-bottom: 0.5rem;
}
[data-testid="stExpander"] summary {
  font-family: var(--mono) !important; font-size: 0.85rem !important;
  color: var(--text) !important; padding: 0.6rem 0.8rem !important;
}
[data-testid="stExpander"] summary:hover { color: var(--cyan) !important; }
[data-testid="stExpanderDetails"] {
  padding: 0.2rem 0.8rem 0.8rem 0.8rem !important; border-top: 1px solid var(--border) !important;
}

/* ── Controls ─────────────────────────────────────────────────────────── */
[data-testid="stBaseButton-primary"], button[kind="primary"] {
  background: linear-gradient(135deg, var(--cyan) 0%, __CYAN_DIM__ 100%) !important;
  color: #070C16 !important; border: none !important; border-radius: var(--radius) !important;
  font-family: var(--mono) !important; font-weight: 600 !important; font-size: 0.85rem !important;
}
[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover {
  filter: brightness(1.1); box-shadow: 0 0 14px rgba(34,211,238,.4) !important;
}
[data-testid="stBaseButton-secondary"], button[kind="secondary"],
[data-testid="stDownloadButton"] button {
  background: transparent !important; border: 1px solid var(--border) !important;
  color: var(--text) !important; border-radius: var(--radius) !important;
  font-family: var(--mono) !important; font-size: 0.84rem !important;
}
[data-testid="stBaseButton-secondary"]:hover,
button[kind="secondary"]:hover,
[data-testid="stDownloadButton"] button:hover {
  border-color: var(--cyan) !important; color: var(--cyan) !important;
  background: rgba(34,211,238,.06) !important;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
  background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; color: var(--text) !important;
  font-family: var(--mono) !important; font-size: 0.85rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--cyan) !important; box-shadow: 0 0 0 2px rgba(34,211,238,.2) !important;
  outline: none !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
  background: var(--bg-panel) !important; border-color: var(--border) !important;
  color: var(--text) !important; font-family: var(--mono) !important;
  font-size: 0.85rem !important; border-radius: var(--radius) !important;
}
[data-testid="stMultiSelect"] [data-testid="stMultiSelectTag"] {
  background: rgba(34,211,238,.15) !important; border: 1px solid var(--cyan) !important;
  color: var(--cyan) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] [role="progressbar"] { background: var(--cyan) !important; }
[data-testid="stSlider"] [data-testid="stSliderThumb"] { background: var(--cyan) !important; border-color: var(--cyan) !important; }
[data-testid="stCheckbox"] input:checked + div,
[data-testid="stToggle"] input:checked + div { background: var(--cyan) !important; border-color: var(--cyan) !important; }
[data-testid="stFileUploadDropzone"] {
  background: var(--bg-panel) !important; border: 1px dashed var(--border) !important;
  border-radius: var(--radius) !important; color: var(--muted) !important;
}
[data-testid="stFileUploadDropzone"]:hover { border-color: var(--cyan) !important; }
[data-testid="stForm"] {
  background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; padding: 1rem !important;
}

/* ── Tables, charts, code ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; overflow: hidden;
}
[data-testid="stDataFrame"] th,
[data-testid="stDataFrame"] [role="columnheader"] {
  background: var(--bg-panel-alt) !important; color: var(--cyan) !important;
  font-family: var(--mono) !important; font-size: 0.76rem !important;
  text-transform: uppercase; letter-spacing: .07em;
  border-bottom: 1px solid var(--border) !important; padding: 6px 10px !important;
}
[data-testid="stDataFrame"] td,
[data-testid="stDataFrame"] [role="gridcell"] {
  background: var(--bg-panel) !important; color: var(--text) !important;
  font-family: var(--mono) !important; font-size: 0.82rem !important;
  border-bottom: 1px solid rgba(31,44,68,.6) !important; padding: 5px 10px !important;
}
[data-testid="stPlotlyChart"] {
  background: transparent !important; border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden;
}
[data-testid="stCodeBlock"] pre,
[data-testid="stCodeBlock"] code {
  background: var(--bg-panel) !important; border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important; color: var(--green) !important;
  font-family: var(--mono) !important; font-size: 0.82rem !important;
}
[data-testid="stAppViewContainer"] hr {
  border: none !important; border-top: 1px solid var(--border) !important; margin: 1.2rem 0 !important;
}

/* ── Risk badge ───────────────────────────────────────────────────────── */
.rh-prediction-row { display: flex; align-items: center; gap: 1rem; margin: 1rem 0 0.5rem; }
.rh-prediction-label {
  font-family: var(--mono); font-size: 0.82rem; color: var(--muted);
  text-transform: uppercase; letter-spacing: .08em;
}
.rh-risk-badge {
  display: inline-flex; align-items: center; gap: 0.45rem;
  padding: 4px 14px 4px 10px; border-radius: 20px;
  border: 1.5px solid currentColor; font-family: var(--mono);
  font-size: 0.9rem; font-weight: 600; letter-spacing: .08em; text-transform: uppercase;
}
.rh-risk-dot {
  width: 8px; height: 8px; border-radius: 50%; background: currentColor; flex-shrink: 0;
  box-shadow: 0 0 6px currentColor;
}
.rh-risk-low { color: var(--green); }
.rh-risk-medium { color: var(--amber); }
.rh-risk-high { color: var(--rose); }

/* ── Footer ───────────────────────────────────────────────────────────── */
.rh-footer {
  border-top: 1px solid var(--border); padding: 0.6rem 0; margin-top: 1rem;
  font-family: var(--mono); font-size: 0.78rem; color: var(--muted);
  text-align: center; letter-spacing: .02em;
}
.rh-footer strong { color: var(--text); }

/* ── Accessibility / small screens ───────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; animation: none !important; }
}
@media (max-width: 960px) {
  [data-testid="stAppViewContainer"] .block-container { padding-left: 0.6rem !important; padding-right: 0.6rem !important; }
  [data-testid="stMetricValue"] { font-size: 1.15rem !important; }
  [data-testid="stAppViewContainer"] .block-container h1 { font-size: 1.2rem !important; }
}
"""


def apply_theme() -> None:
    """Inject the console CSS once per Streamlit run.

    Tokens are replaced with ``str.replace`` so literal CSS braces never
    conflict with Python formatting.
    """
    css = (
        _CSS
        .replace("__FONTS__", _FONTS)
        .replace("__BG_PAGE__", BG_PAGE)
        .replace("__BG_PANEL_ALT__", BG_PANEL_ALT)
        .replace("__BG_PANEL__", BG_PANEL)
        .replace("__BORDER__", BORDER)
        .replace("__CYAN_DIM__", ACCENT_CYAN_DIM)
        .replace("__CYAN__", ACCENT_CYAN)
        .replace("__GREEN__", ACCENT_GREEN)
        .replace("__AMBER__", ACCENT_AMBER)
        .replace("__ROSE__", ACCENT_ROSE)
        .replace("__TEXT__", TEXT_PRIMARY)
        .replace("__MUTED__", TEXT_MUTED)
    )
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def sidebar_header_html(
    dataset_available: bool,
    model_available: bool,
    using_test_artifacts: bool = False,
) -> str:
    """Return the sidebar identity and an honest system-status panel."""
    if using_test_artifacts:
        dot = "rh-dot-red"
        label = "ARTEFACT DE TEST DÉTECTÉ"
        color = ACCENT_ROSE
    elif model_available:
        dot = "rh-dot-green"
        label = "MODÈLE DISPONIBLE"
        color = "#2ecc71"
    elif dataset_available:
        dot = "rh-dot-amber"
        label = "JEU DE DONNÉES DISPONIBLE"
        color = ACCENT_AMBER
    else:
        dot = "rh-dot-amber"
        label = "JEU DE DONNÉES NON CHARGÉ"
        color = ACCENT_AMBER

    return f"""
<div class="rh-sidebar-header">
  <div class="rh-sidebar-icon">💼</div>
  <div>
    <div class="rh-sidebar-title">Attrition RH Intelligence</div>
    <div class="rh-sidebar-subtitle">Console d'analyse des départs</div>
  </div>
</div>
<div class="rh-status-panel">
  <div class="rh-status-caption">État du système</div>
  <div class="rh-status-row">
    <span class="rh-dot {dot}"></span>
    <span class="rh-status-label" style="color:{color};">{label}</span>
  </div>
  <div class="rh-status-row" style="margin-top:0.15rem;">
    <span>Prototype académique · données synthétiques</span>
  </div>
</div>
"""


def page_divider_html() -> str:
    """Return the glowing divider placed under each page title."""
    return '<hr class="rh-page-divider" aria-hidden="true">'


def footer_html(text: str) -> str:
    """Return the styled page footer."""
    return f'<div class="rh-footer">{text}</div>'


def risk_badge_html(
    label: str,
    probabilite: float,
    prediction: Optional[str] = None,
) -> str:
    """Return a pill badge for the predicted risk and the Yes/No outcome."""
    p_pct = probabilite * 100 if probabilite <= 1.0 else probabilite
    normalized = label.strip().lower()
    if normalized.startswith("faible"):
        css_class, sortie = "rh-risk-low", "NO"
    elif normalized.startswith("modér") or normalized.startswith("moder"):
        css_class, sortie = "rh-risk-medium", "NO"
    else:
        css_class, sortie = "rh-risk-high", "YES"
    if prediction:
        sortie = "YES" if str(prediction).lower() in {"yes", "1", "oui"} else "NO"

    return (
        '<div class="rh-prediction-row">'
        '<span class="rh-prediction-label">Risque prédit</span>'
        f'<span class="rh-risk-badge {css_class}">'
        f'<span class="rh-risk-dot"></span>{label.upper()} · {sortie} · {p_pct:.1f}%'
        '</span>'
        '</div>'
    )

"""
TTS Guard — Shared Theme Module
Provides color tokens for Plotly charts and decorative CSS.
Base colors (background, text, sidebar) are handled by .streamlit/config.toml.
"""

import streamlit as st


def is_dark_mode():
    """Check active theme. Config.toml defaults to dark."""
    try:
        return st.get_option("theme.base") != "light"
    except Exception:
        return True


def get_colors():
    """Return color tokens for charts, gradients, and decorative elements."""
    dark = is_dark_mode()
    if dark:
        return {
            "BG": "#0e1117", "BG2": "#1a1f2e",
            "BORDER": "#2a2f3a", "TEXT": "#e0e0e0", "TEXT_MUTED": "#9ca3af",
            "CARD_BG": "#1a1f2e", "METRIC_VAL": "#ff6600", "METRIC_ACCENT": "#ff6600",
            "HEADER_HEAD": "#ff6600", "HEADER_TAIL": "#ff8c3a",
            "SHADOW": "rgba(0,0,0,0.3)", "HOVER_SHADOW": "rgba(255,102,0,0.15)",
            "BTN_HOVER_TEXT": "#0e1117",
            "STATUS_RED": "#ff4444", "STATUS_GREEN": "#34d399",
            "CHART_PRIMARY": "#ff6600",
            "CHART_SECONDARY": "#34d399",
            "CHART_TERTIARY": "#ff4444",
            "CHART_QUATERNARY": "#a78bfa",
            "CHART_SEQUENCE": ["#ff6600", "#34d399", "#ff4444", "#a78bfa", "#60a5fa", "#fbbf24"],
        }
    else:
        return {
            "BG": "#ffffff", "BG2": "#f8f8fa",
            "BORDER": "#e5e5e5", "TEXT": "#222222", "TEXT_MUTED": "#777777",
            "CARD_BG": "#ffffff", "METRIC_VAL": "#012f5d", "METRIC_ACCENT": "#012f5d",
            "HEADER_HEAD": "#012f5d", "HEADER_TAIL": "#ff6600",
            "SHADOW": "rgba(0,0,0,0.05)", "HOVER_SHADOW": "rgba(1,47,93,0.12)",
            "BTN_HOVER_TEXT": "#ffffff",
            "STATUS_RED": "#e60000", "STATUS_GREEN": "#00C853",
            "CHART_PRIMARY": "#012f5d",
            "CHART_SECONDARY": "#00C853",
            "CHART_TERTIARY": "#e60000",
            "CHART_QUATERNARY": "#ff6600",
            "CHART_SEQUENCE": ["#012f5d", "#00C853", "#e60000", "#ff6600", "#1e88e5", "#f57c00"],
        }


def inject_css():
    """Inject only decorative CSS that config.toml cannot handle."""
    c = get_colors()
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Open+Sans:wght@400;600&display=swap');

    /* Typography */
    html, body, [class*="css"] {{
        font-family: 'Open Sans', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Roboto', sans-serif !important;
    }}

    /* Top header gradient bar */
    .stApp > header {{
        background: linear-gradient(90deg, #0a1628, #012f5d 60%, #ff6600) !important;
    }}

    /* Metric card accent styling */
    [data-testid="stMetricValue"] {{
        font-size: 1.8rem; font-weight: 700;
        font-family: 'Roboto', sans-serif !important;
        color: {c['METRIC_VAL']} !important;
    }}
    div[data-testid="stMetric"] {{
        border-left: 4px solid {c['METRIC_ACCENT']};
        border-radius: 8px;
        box-shadow: 0px 2px 10px {c['SHADOW']};
    }}

    /* Gradient section headers */
    .fire-header {{
        background: linear-gradient(90deg, {c['HEADER_HEAD']}, {c['HEADER_TAIL']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-family: 'Roboto', sans-serif !important;
    }}

    /* Hero stat cards (welcome page) */
    .hero-stat {{
        text-align: center; padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 15px {c['SHADOW']};
        transition: all 0.3s ease;
    }}
    .hero-stat:hover {{
        box-shadow: 0px 4px 20px {c['HOVER_SHADOW']};
        border-color: #ff6600;
    }}
    .hero-stat h2 {{
        color: {c['METRIC_VAL']}; margin: 0; font-size: 2.2rem;
        font-family: 'Roboto', sans-serif !important;
    }}
    .hero-stat p {{
        color: {c['TEXT_MUTED']}; margin: 4px 0 0 0; font-size: 0.9rem;
    }}

    /* Navigation cards (welcome page) */
    .nav-card {{
        padding: 18px; border-radius: 10px; text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0px 2px 10px {c['SHADOW']};
    }}
    .nav-card:hover {{
        border-color: #ff6600;
        box-shadow: 0 4px 15px {c['HOVER_SHADOW']};
        transform: translateY(-2px);
    }}
    .nav-card h3 {{
        margin: 8px 0 4px 0; font-size: 1rem;
        font-family: 'Roboto', sans-serif !important;
    }}
    .nav-card p {{
        color: {c['TEXT_MUTED']}; font-size: 0.8rem; margin: 0;
    }}

    /* Orange button styling */
    .stButton > button {{
        border-color: #ff6600; color: #ff6600; transition: all 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: #ff6600; color: {c['BTN_HOVER_TEXT']};
        border-color: #ff6600;
    }}

    /* Progress bar */
    .stProgress > div > div > div {{
        background-color: #ff6600 !important;
    }}

    /* Expander header font */
    .streamlit-expanderHeader {{
        font-family: 'Roboto', sans-serif !important;
    }}

    /* Active tab accent */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: #ff6600 !important;
        border-bottom-color: #ff6600 !important;
    }}

    /* Alert accents */
    .stAlert [data-testid="stNotificationContentWarning"] {{
        border-left-color: #ff6600 !important;
    }}
    .stAlert [data-testid="stNotificationContentError"] {{
        border-left-color: {c['STATUS_RED']} !important;
    }}

    /* DataFrame rounding */
    .stDataFrame {{ border-radius: 8px; }}
</style>
""", unsafe_allow_html=True)


def plotly_layout(height=350, **kwargs):
    """Return Plotly layout kwargs for transparent backgrounds and theme-aware styling."""
    c = get_colors()
    defaults = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": c["TEXT"], "family": "Open Sans, sans-serif"},
        "title_font": {"family": "Roboto, sans-serif", "color": c["TEXT"]},
        "legend": {"font": {"color": c["TEXT_MUTED"]}},
        "xaxis": {"gridcolor": c["BORDER"], "zerolinecolor": c["BORDER"]},
        "yaxis": {"gridcolor": c["BORDER"], "zerolinecolor": c["BORDER"]},
        "margin": {"l": 20, "r": 20, "t": 40, "b": 20},
        "height": height,
    }
    defaults.update(kwargs)
    return defaults

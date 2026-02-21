"""
TTS Guard — Shared Theme Module
Provides color tokens for Plotly charts and purely modern decorative CSS.
"""

import streamlit as st

def is_dark_mode():
    """Check active theme. Config.toml defaults to dark, but modern UI adapts."""
    try:
        return st.get_option("theme.base") != "light"
    except Exception:
        return True

def get_colors():
    """Return modern color tokens."""
    dark = is_dark_mode()
    if dark:
        return {
            "BG": "#0f172a", "BG2": "#1e293b",
            "BORDER": "#334155", "TEXT": "#f8fafc", "TEXT_MUTED": "#94a3b8",
            "CARD_BG": "#1e293b", "METRIC_VAL": "#ef4444", "METRIC_ACCENT": "#ef4444",
            "HEADER_HEAD": "#ef4444", "HEADER_TAIL": "#f97316",
            "SHADOW": "rgba(0,0,0,0.5)", "HOVER_SHADOW": "rgba(239,68,68,0.2)",
            "BTN_HOVER_TEXT": "#ffffff",
            "STATUS_RED": "#ef4444", "STATUS_GREEN": "#10b981",
            "CHART_PRIMARY": "#ef4444",
            "CHART_SECONDARY": "#10b981",
            "CHART_TERTIARY": "#f59e0b",
            "CHART_QUATERNARY": "#8b5cf6",
            "CHART_SEQUENCE": ["#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#3b82f6", "#14b8a6"],
        }
    else:
        return {
            "BG": "#f8fafc", "BG2": "#ffffff",
            "BORDER": "#e2e8f0", "TEXT": "#0f172a", "TEXT_MUTED": "#64748b",
            "CARD_BG": "#ffffff", "METRIC_VAL": "#b91c1c", "METRIC_ACCENT": "#ef4444",
            "HEADER_HEAD": "#b91c1c", "HEADER_TAIL": "#ea580c",
            "SHADOW": "rgba(0,0,0,0.05)", "HOVER_SHADOW": "rgba(239,68,68,0.15)",
            "BTN_HOVER_TEXT": "#ffffff",
            "STATUS_RED": "#ef4444", "STATUS_GREEN": "#10b981",
            "CHART_PRIMARY": "#0f172a",
            "CHART_SECONDARY": "#10b981",
            "CHART_TERTIARY": "#ef4444",
            "CHART_QUATERNARY": "#f97316",
            "CHART_SEQUENCE": ["#0f172a", "#10b981", "#ef4444", "#f97316", "#3b82f6", "#8b5cf6"],
        }

def inject_css():
    """Inject premium, highly modern CSS using native Streamlit variables for safe contrast."""
    c = get_colors()
    st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* Typography */
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 700 !important;
        letter-spacing: -0.025em;
    }}

    /* Top header removal / transparent */
    .stApp > header {{
        background: transparent !important;
    }}

    /* Advanced Metric Cards */
    div[data-testid="stMetric"] {{
        background: var(--secondary-background-color);
        border: 1px solid var(--secondary-background-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }}
    
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);
        border-color: #ef4444;
    }}

    /* Metric Value */
    [data-testid="stMetricValue"] {{
        font-size: 2.25rem !important; 
        font-weight: 800 !important;
        letter-spacing: -0.025em;
        color: #ef4444 !important;
        margin-top: 8px;
    }}

    /* Metric Label */
    [data-testid="stMetricLabel"] {{
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Gradient section headers */
    .fire-header {{
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
        font-size: 3rem !important;
    }}

    /* Hero stat cards (welcome page) */
    .hero-stat {{
        text-align: center; 
        padding: 24px;
        background: var(--secondary-background-color);
        border-radius: 16px;
        box-shadow: 0px 4px 6px -1px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }}
    .hero-stat:hover {{
        box-shadow: 0px 20px 25px -5px rgba(0,0,0,0.15);
        border-color: #ef4444;
        transform: translateY(-4px);
    }}
    .hero-stat h2 {{
        margin: 0; font-size: 2.5rem;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .hero-stat p {{
        margin: 8px 0 0 0; font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Navigation cards (welcome page) */
    .nav-card {{
        padding: 24px; 
        background: var(--secondary-background-color);
        border-radius: 16px; 
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0px 4px 6px -1px rgba(0,0,0,0.1);
        cursor: pointer;
    }}
    .nav-card:hover {{
        border: 1px solid #ef4444;
        box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15);
        transform: translateY(-4px);
    }}
    .nav-card h3 {{
        margin: 8px 0 8px 0; font-size: 1.25rem;
        font-weight: 700 !important;
    }}
    .nav-card p {{
        font-size: 0.9rem; margin: 0;
    }}

    /* Sleek buttons */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s ease;
    }}
    .stButton > button:hover {{
        border-color: #ef4444;
        color: #ef4444;
        transform: translateY(-1px);
    }}
    
    /* Primary buttons */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        color: white;
        border: none;
    }}

    /* DataFrames / Tables */
    .stDataFrame {{
        border-radius: 12px;
        overflow: hidden;
    }}

    /* Progress bar */
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #ef4444 0%, #ea580c 100%) !important;
    }}

</style>
""", unsafe_allow_html=True)

def plotly_layout(height=350, **kwargs):
    """Return Plotly layout kwargs for transparent backgrounds and theme-aware styling."""
    c = get_colors()
    defaults = {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": c["TEXT"], "family": "Inter, sans-serif"},
        "title_font": {"family": "Inter, sans-serif", "color": c["TEXT"], "weight": "bold"},
        "legend": {"font": {"color": c["TEXT_MUTED"]}},
        "xaxis": {"gridcolor": c["BORDER"], "zerolinecolor": c["BORDER"]},
        "yaxis": {"gridcolor": c["BORDER"], "zerolinecolor": c["BORDER"]},
        "margin": {"l": 20, "r": 20, "t": 40, "b": 20},
        "height": height,
    }
    defaults.update(kwargs)
    return defaults

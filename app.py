"""
TTS Guard — Main Entry Point
Welcome page with branding, key stats, guided tour, and sidebar configuration.
"""

import streamlit as st
import os
from datetime import date
from database import init_db, reset_db, has_data, get_active_contracts_count, get_all_clients, get_all_buildings, get_financial_summary
from seed_data import seed

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="TTS Guard",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# FIRE GRADIENT CSS THEME
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* Fire gradient header accent */
    .stApp > header {
        background: linear-gradient(90deg, #D32F2F, #FF6F00) !important;
    }

    /* Metric card styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Sidebar branding */
    [data-testid="stSidebar"] {
        background-color: #FAFAFA;
    }

    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
    }

    /* Custom metric card borders */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 4px solid #D32F2F;
        padding: 12px 16px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }

    /* Section headers */
    .fire-header {
        background: linear-gradient(90deg, #D32F2F, #FF6F00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Status colors */
    .status-overdue { color: #FF4B4B; font-weight: 600; }
    .status-due-soon { color: #FFA500; font-weight: 600; }
    .status-ok { color: #00C853; font-weight: 600; }

    /* Welcome page hero */
    .hero-stat {
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .hero-stat h2 {
        color: #D32F2F;
        margin: 0;
        font-size: 2.2rem;
    }
    .hero-stat p {
        color: #666;
        margin: 4px 0 0 0;
        font-size: 0.9rem;
    }

    /* Navigation cards */
    .nav-card {
        padding: 16px;
        background: white;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        text-align: center;
        transition: all 0.2s;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .nav-card:hover {
        border-color: #D32F2F;
        box-shadow: 0 4px 12px rgba(211,47,47,0.1);
    }
    .nav-card h3 {
        margin: 8px 0 4px 0;
        font-size: 1rem;
    }
    .nav-card p {
        color: #888;
        font-size: 0.8rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# DATABASE INIT
# ---------------------------------------------------------------------------
init_db()
if not has_data():
    seed()

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

with st.sidebar:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=180)
    else:
        st.markdown(
            '<h2 style="background: linear-gradient(90deg, #D32F2F, #FF6F00); '
            '-webkit-background-clip: text; -webkit-text-fill-color: transparent; '
            'margin: 0;">🔥 TTS Guard</h2>',
            unsafe_allow_html=True,
        )

    st.markdown("**Talent Technical Services**")
    st.markdown(f"📅 {date.today().strftime('%B %d, %Y')}")
    st.markdown("📍 Abu Dhabi, UAE")

    st.divider()

    # Demo notes expander
    with st.expander("📋 Demo Notes"):
        st.markdown("""
        **Presenter's Guide:**
        - **Dashboard**: Show 4 inspection metrics + financial health + alert banner
        - **Overdue**: Demonstrate scheduling an overdue inspection
        - **Inspect**: Submit an inspection, download PDF, create complaint ticket
        - **Clients**: Expand a client to show buildings + financials
        - **Reports**: Switch months to show trend data
        - **Financials**: Highlight collection rate and outstanding invoices
        """)

    st.divider()

    # Two-step reset
    if "reset_confirm" not in st.session_state:
        st.session_state.reset_confirm = False

    if not st.session_state.reset_confirm:
        if st.button("🔄 Reset Demo Data", use_container_width=True):
            st.session_state.reset_confirm = True
            st.rerun()
    else:
        st.warning("⚠️ This will erase all data including submitted inspections.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirm", use_container_width=True):
                reset_db()
                seed()
                st.session_state.reset_confirm = False
                st.success("Demo data reset!")
                st.rerun()
        with col2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.reset_confirm = False
                st.rerun()

# ---------------------------------------------------------------------------
# WELCOME PAGE
# ---------------------------------------------------------------------------
st.markdown(
    '<h1 style="background: linear-gradient(90deg, #D32F2F, #FF6F00); '
    '-webkit-background-clip: text; -webkit-text-fill-color: transparent; '
    'margin-bottom: 0;">🔥 TTS Guard</h1>',
    unsafe_allow_html=True,
)
st.markdown("### AMC Management Dashboard — Talent Technical Services")
st.markdown(
    '<p style="color: #666; font-size: 1.05rem; margin-top: -8px;">'
    "Centralized inspection tracking, compliance monitoring, and financial oversight "
    "for fire safety AMC contracts across Abu Dhabi.</p>",
    unsafe_allow_html=True,
)

st.divider()

# Key stats
clients_df = get_all_clients()
buildings_df = get_all_buildings()
contracts_count = get_active_contracts_count()
financials = get_financial_summary()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        f'<div class="hero-stat"><h2>{len(clients_df)}</h2><p>Active Clients</p></div>',
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        f'<div class="hero-stat"><h2>{len(buildings_df)}</h2><p>Buildings Managed</p></div>',
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        f'<div class="hero-stat"><h2>{contracts_count}</h2><p>Active Contracts</p></div>',
        unsafe_allow_html=True,
    )
with col4:
    total_val = financials["total_contract_value"]
    st.markdown(
        f'<div class="hero-stat"><h2>AED {total_val:,.0f}</h2><p>Annual Contract Value</p></div>',
        unsafe_allow_html=True,
    )

st.divider()

# Guided Tour
if "show_tour" not in st.session_state:
    st.session_state.show_tour = False

if st.button("🎯 Take a Tour", use_container_width=False):
    st.session_state.show_tour = not st.session_state.show_tour

if st.session_state.show_tour:
    st.info("""
    **Welcome to TTS Guard! Here's what each section does:**

    1. **📊 Dashboard** — Your command center. See overdue alerts, upcoming inspections, recent complaints, financial health, and client overview all in one place.

    2. **🔴 Overdue** — Buildings that need immediate attention. Schedule inspections with a date and technician right from here.

    3. **📋 Inspect** — Submit inspection results. Check equipment, add notes, download a professional PDF report, and auto-create complaint tickets for failed items.

    4. **👥 Clients** — Complete directory of all clients and their buildings with contact info, equipment counts, and financial summaries.

    5. **📈 Reports** — Monthly compliance reports with charts showing inspections per client and complaint breakdowns.

    6. **💰 Financials** — Revenue dashboard showing collection rates, outstanding payments, client-wise breakdowns, and payment history.

    *Use the sidebar navigation to explore each section. Click "Take a Tour" again to hide this guide.*
    """)

st.divider()

# Navigation cards
st.markdown("### Quick Navigation")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        '<div class="nav-card"><h3>📊 Dashboard</h3>'
        "<p>Metrics, alerts & overview</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="nav-card"><h3>🔴 Overdue</h3>'
        "<p>Schedule overdue inspections</p></div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="nav-card"><h3>📋 Inspect</h3>'
        "<p>Submit inspections & PDF reports</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="nav-card"><h3>👥 Clients</h3>'
        "<p>Client & building directory</p></div>",
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        '<div class="nav-card"><h3>📈 Reports</h3>'
        "<p>Monthly compliance summaries</p></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="nav-card"><h3>💰 Financials</h3>'
        "<p>Revenue & payment tracking</p></div>",
        unsafe_allow_html=True,
    )

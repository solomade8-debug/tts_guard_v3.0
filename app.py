"""
TTS Guard — Main Entry Point
Welcome page with branding, key stats, guided tour, and sidebar configuration.
"""

import streamlit as st
import os
from datetime import date
from database import init_db, reset_db, has_data, get_active_contracts_count, get_all_clients, get_all_buildings, get_financial_summary
from seed_data import seed
from theme import get_colors, inject_css

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
# THEME
# ---------------------------------------------------------------------------
c = get_colors()
inject_css()

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
    # Logo
    logo_bg = "#012f5d"
    if os.path.exists(LOGO_PATH):
        import base64
        with open(LOGO_PATH, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<div style="background-color: {logo_bg}; padding: 16px 20px; '
            f'border-radius: 10px; text-align: center; margin-bottom: 8px;">'
            f'<img src="data:image/png;base64,{logo_b64}" width="180" />'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<h2 style="color: {c["METRIC_VAL"]}; font-family: Roboto, sans-serif; '
            f'font-weight: 700; margin: 0;">TTS Guard</h2>',
            unsafe_allow_html=True,
        )

    st.caption("Talent Technical Services")
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
    '<h1 class="fire-header" style="margin-bottom: 0;">TTS Guard</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    f'<h3 style="color: {c["METRIC_VAL"]}; font-family: Roboto, sans-serif; '
    f'font-weight: 500; margin-top: 0;">AMC Management Dashboard</h3>',
    unsafe_allow_html=True,
)
st.caption(
    "Centralized inspection tracking, compliance monitoring, and financial oversight "
    "for fire safety AMC contracts across Abu Dhabi."
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

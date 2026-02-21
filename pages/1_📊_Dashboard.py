"""
TTS Guard — Dashboard Page
Key metrics, alert banner, financial health, upcoming inspections,
recent complaints, and client overview with interactive charts.
"""

import streamlit as st
import plotly.graph_objects as go
from database import (
    get_active_contracts_count,
    get_overdue_inspections,
    get_upcoming_inspections,
    get_completed_this_month,
    get_recent_complaints,
    get_client_summary,
    get_financial_summary,
)
from theme import get_colors, inject_css, plotly_layout

c = get_colors()
inject_css()

st.markdown(
    '<h1 class="fire-header">📊 Dashboard</h1>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# TOP ROW — 4 Inspection Metric Cards
# ---------------------------------------------------------------------------
contracts_count = get_active_contracts_count()
overdue_df = get_overdue_inspections()
overdue_count = len(overdue_df)
upcoming_df = get_upcoming_inspections(14)
upcoming_count = len(upcoming_df)
completed_df = get_completed_this_month()
completed_count = len(completed_df)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Active Contracts", contracts_count)
with col2:
    st.metric(
        "🔴 Overdue",
        overdue_count,
        delta=f"{overdue_count} need attention" if overdue_count > 0 else "All clear",
        delta_color="inverse" if overdue_count > 0 else "normal",
    )
with col3:
    st.metric("🟡 Due Within 14 Days", upcoming_count)
with col4:
    st.metric("🟢 Completed This Month", completed_count)

# ---------------------------------------------------------------------------
# ALERT BANNER
# ---------------------------------------------------------------------------
if overdue_count > 0:
    st.error(
        f"⚠️ **{overdue_count} inspection{'s' if overdue_count > 1 else ''} overdue** "
        "— Risk of Civil Defence non-compliance"
    )

# ---------------------------------------------------------------------------
# INSPECTION STATUS DISTRIBUTION (stacked horizontal bar)
# ---------------------------------------------------------------------------
ok_count = max(contracts_count - overdue_count - upcoming_count, 0)

fig_status = go.Figure()
fig_status.add_trace(go.Bar(
    y=["Inspections"],
    x=[overdue_count],
    name="Overdue",
    orientation="h",
    marker_color=c["CHART_TERTIARY"],
    hovertemplate="Overdue: %{x}<extra></extra>",
))
fig_status.add_trace(go.Bar(
    y=["Inspections"],
    x=[upcoming_count],
    name="Due Soon",
    orientation="h",
    marker_color=c["CHART_PRIMARY"],
    hovertemplate="Due Soon: %{x}<extra></extra>",
))
fig_status.add_trace(go.Bar(
    y=["Inspections"],
    x=[ok_count],
    name="On Track",
    orientation="h",
    marker_color=c["CHART_SECONDARY"],
    hovertemplate="On Track: %{x}<extra></extra>",
))
fig_status.update_layout(**plotly_layout(
    height=120,
    barmode="stack",
    showlegend=True,
    legend={"orientation": "h", "yanchor": "bottom", "y": 1.02, "xanchor": "right", "x": 1},
    yaxis={"visible": False},
    margin={"l": 0, "r": 0, "t": 30, "b": 0},
))
st.plotly_chart(fig_status, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# FINANCIAL HEALTH SECTION
# ---------------------------------------------------------------------------
st.subheader("💰 Financial Health")

financials = get_financial_summary()

fcol1, fcol2, fcol3, fcol4 = st.columns(4)
with fcol1:
    st.metric(
        "Total Contract Value",
        f"AED {financials['total_contract_value']:,.0f}",
    )
with fcol2:
    st.metric(
        "Collected",
        f"AED {financials['total_collected']:,.0f}",
        delta=f"{financials['collection_pct']:.0f}%",
    )
with fcol3:
    st.metric(
        "Outstanding",
        f"AED {financials['total_outstanding']:,.0f}",
        delta=f"{financials['outstanding_count']} invoices",
        delta_color="inverse",
    )
with fcol4:
    st.metric(
        "Overdue Payments",
        f"AED {financials['total_overdue']:,.0f}",
        delta=f"{financials['overdue_count']} overdue",
        delta_color="inverse",
    )

# Collection rate donut chart
collection_pct = financials["collection_pct"]
collected = financials["total_collected"]
outstanding = financials["total_outstanding"]

fig_donut = go.Figure(data=[go.Pie(
    labels=["Collected", "Outstanding"],
    values=[collected, outstanding],
    hole=0.65,
    marker_colors=[c["CHART_SECONDARY"], c["CHART_TERTIARY"]],
    textinfo="percent+label",
    textfont={"color": c["TEXT"]},
    hovertemplate="<b>%{label}</b><br>AED %{value:,.0f}<br>%{percent}<extra></extra>",
)])
fig_donut.update_layout(**plotly_layout(
    height=300,
    title_text=f"Collection Rate: {collection_pct:.1f}%",
    showlegend=True,
    annotations=[{
        "text": f"{collection_pct:.0f}%",
        "x": 0.5, "y": 0.5, "font_size": 28,
        "font_color": c["CHART_PRIMARY"],
        "showarrow": False,
    }],
))
st.plotly_chart(fig_donut, use_container_width=True)

st.caption("→ View full details on the **💰 Financials** page")

st.divider()

# ---------------------------------------------------------------------------
# TWO COLUMNS: Upcoming Inspections + Recent Complaints
# ---------------------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("📅 Upcoming Inspections")
    if len(upcoming_df) > 0:
        display_df = upcoming_df[
            ["building_name", "client_name", "area", "days_until_next"]
        ].copy()
        display_df.columns = ["Building", "Client", "Area", "Days Remaining"]
        display_df = display_df.sort_values("Days Remaining")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.success("No inspections due within 14 days.")

with right:
    st.subheader("🎫 Recent Complaints")
    complaints_df = get_recent_complaints(5)
    if len(complaints_df) > 0:
        priority_border_map = {
            "high": c["STATUS_RED"],
            "medium": c["CHART_PRIMARY"],
            "low": c["CHART_SECONDARY"],
        }
        for _, comp in complaints_df.iterrows():
            priority_emoji = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢",
            }.get(comp["priority"], "⚪")
            border_color = priority_border_map.get(comp["priority"], c["BORDER"])

            with st.container(border=True):
                st.markdown(
                    f'<div style="border-left: 4px solid {border_color}; padding-left: 8px; color: {c["TEXT"]};">'
                    f"<strong>{comp['ticket_number']}</strong> {priority_emoji} "
                    f"<code>{comp['priority'].upper()}</code>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"{comp['message']}")
                st.caption(
                    f"{comp['client_name']} — {comp['building_name']} · "
                    f"{comp['status'].replace('_', ' ').title()} · {comp['created_at']}"
                )
    else:
        st.info("No recent complaints.")

st.divider()

# ---------------------------------------------------------------------------
# CLIENT OVERVIEW TABLE
# ---------------------------------------------------------------------------
st.subheader("👥 Client Overview")

client_summary = get_client_summary()
if len(client_summary) > 0:
    display_cs = client_summary[
        ["Client", "Buildings", "Equipment", "Annual Value (AED)", "overdue_count"]
    ].copy()

    # Format status column
    display_cs["Status"] = display_cs["overdue_count"].apply(
        lambda x: f"🔴 {x} overdue" if x > 0 else "✅ All clear"
    )
    display_cs["Annual Value (AED)"] = display_cs["Annual Value (AED)"].apply(
        lambda x: f"AED {x:,.0f}"
    )
    display_cs = display_cs.drop(columns=["overdue_count"])
    st.dataframe(display_cs, use_container_width=True, hide_index=True)

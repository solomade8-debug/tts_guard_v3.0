"""
TTS Guard — Reports Page
Monthly compliance reports with interactive Plotly charts (6 months depth).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from database import (
    get_inspections_by_month,
    get_complaints_by_month,
    get_all_clients,
)
from theme import get_colors, inject_css, plotly_layout

c = get_colors()
inject_css()

st.markdown(
    '<h1 class="fire-header">📈 Reports</h1>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# MONTH SELECTOR (last 6 months)
# ---------------------------------------------------------------------------
today = date.today()
month_options = []
for i in range(6):
    m = today.month - i
    y = today.year
    while m <= 0:
        m += 12
        y -= 1
    month_options.append((y, m, date(y, m, 1).strftime("%B %Y")))

selected_month = st.selectbox(
    "Select Month",
    options=month_options,
    format_func=lambda x: x[2],
)

year, month, label = selected_month

st.divider()

# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------
inspections_df = get_inspections_by_month(year, month)
complaints_df = get_complaints_by_month(year, month)

# ---------------------------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------------------------
st.subheader(f"📊 Summary — {label}")

total_inspections = len(inspections_df)
total_equipment = int(inspections_df["items_checked"].sum()) if total_inspections > 0 else 0
total_passed = int(inspections_df["items_passed"].sum()) if total_inspections > 0 else 0
compliance_rate = (total_passed / total_equipment * 100) if total_equipment > 0 else 0

total_complaints = len(complaints_df)
resolved_complaints = len(complaints_df[complaints_df["status"] == "resolved"]) if total_complaints > 0 else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Inspections Completed", total_inspections)
with col2:
    st.metric("Equipment Checked", f"{total_equipment:,}")
with col3:
    st.metric("Compliance Rate", f"{compliance_rate:.1f}%")
with col4:
    st.metric(
        "Complaints",
        f"{resolved_complaints}/{total_complaints} resolved",
    )

# ---------------------------------------------------------------------------
# COMPLIANCE RATE GAUGE
# ---------------------------------------------------------------------------
if total_equipment > 0:
    gauge_color = c["CHART_SECONDARY"] if compliance_rate >= 80 else (
        c["CHART_PRIMARY"] if compliance_rate >= 50 else c["STATUS_RED"]
    )
    fig_compliance = go.Figure(go.Indicator(
        mode="gauge+number",
        value=compliance_rate,
        number={"suffix": "%", "font": {"color": gauge_color, "size": 32}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": c["TEXT_MUTED"]},
            "bar": {"color": gauge_color},
            "bgcolor": c["BORDER"],
            "steps": [
                {"range": [0, 60], "color": "rgba(255,68,68,0.1)"},
                {"range": [60, 80], "color": "rgba(255,102,0,0.1)"},
                {"range": [80, 100], "color": "rgba(52,211,153,0.1)"},
            ],
        },
        title={"text": "Compliance Rate", "font": {"color": c["TEXT_MUTED"]}},
    ))
    fig_compliance.update_layout(**plotly_layout(height=250))
    st.plotly_chart(fig_compliance, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# CHARTS
# ---------------------------------------------------------------------------
chart_left, chart_right = st.columns(2)

with chart_left:
    st.subheader("Inspections by Client")
    if total_inspections > 0:
        by_client = (
            inspections_df.groupby("client_name")
            .size()
            .reset_index(name="Inspections")
        )
        fig_client = go.Figure(data=[go.Bar(
            x=by_client["client_name"],
            y=by_client["Inspections"],
            marker_color=c["CHART_PRIMARY"],
            hovertemplate="<b>%{x}</b><br>Inspections: %{y}<extra></extra>",
        )])
        fig_client.update_layout(**plotly_layout(
            height=350,
            xaxis_title="",
            yaxis_title="Inspections",
        ))
        st.plotly_chart(fig_client, use_container_width=True)
    else:
        st.info(f"No inspections recorded for {label}.")

with chart_right:
    st.subheader("Complaints by Priority")
    if total_complaints > 0:
        by_priority = (
            complaints_df.groupby("priority")
            .size()
            .reset_index(name="Count")
        )
        priority_order = {"high": 0, "medium": 1, "low": 2}
        by_priority["order"] = by_priority["priority"].map(priority_order)
        by_priority = by_priority.sort_values("order").drop(columns=["order"])

        # Semantic colors per priority
        priority_colors = {
            "high": c["STATUS_RED"],
            "medium": c["CHART_PRIMARY"],
            "low": c["CHART_SECONDARY"],
        }
        bar_colors = [priority_colors.get(p, c["CHART_QUATERNARY"]) for p in by_priority["priority"]]

        fig_priority = go.Figure(data=[go.Bar(
            x=by_priority["priority"],
            y=by_priority["Count"],
            marker_color=bar_colors,
            hovertemplate="<b>%{x}</b><br>Count: %{y}<extra></extra>",
        )])
        fig_priority.update_layout(**plotly_layout(
            height=350,
            xaxis_title="",
            yaxis_title="Complaints",
        ))
        st.plotly_chart(fig_priority, use_container_width=True)
    else:
        st.info(f"No complaints recorded for {label}.")

st.divider()

# ---------------------------------------------------------------------------
# INSPECTION DETAIL TABLE
# ---------------------------------------------------------------------------
st.subheader("Inspection Details")
if total_inspections > 0:
    detail_df = inspections_df[
        ["inspection_date", "client_name", "building_name", "technician",
         "items_checked", "items_passed", "items_failed"]
    ].copy()
    detail_df.columns = [
        "Date", "Client", "Building", "Technician",
        "Checked", "Passed", "Failed",
    ]
    st.dataframe(detail_df, use_container_width=True, hide_index=True)
else:
    st.info(f"No inspection data for {label}.")

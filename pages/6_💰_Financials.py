"""
TTS Guard — Financials Page
Revenue tracking, payment status, collection rate, client breakdown,
payment history, and outstanding invoices with interactive Plotly charts.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from database import (
    get_financial_summary,
    get_client_financial_breakdown,
    get_payment_history,
    get_monthly_revenue,
    get_outstanding_invoices,
)
from theme import get_colors, inject_css, plotly_layout

c = get_colors()
inject_css()

st.markdown(
    '<h1 class="fire-header">💰 Financial Overview</h1>',
    unsafe_allow_html=True,
)
st.caption("Revenue tracking and payment status for all AMC contracts")

# ---------------------------------------------------------------------------
# TOP ROW — 4 Financial Metrics
# ---------------------------------------------------------------------------
financials = get_financial_summary()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Total Contract Value",
        f"AED {financials['total_contract_value']:,.0f}",
        help="Sum of all active contract annual values",
    )
with col2:
    st.metric(
        "Collected",
        f"AED {financials['total_collected']:,.0f}",
        delta=f"{financials['collection_pct']:.0f}%",
    )
with col3:
    st.metric(
        "Outstanding",
        f"AED {financials['total_outstanding']:,.0f}",
        delta=f"{financials['outstanding_count']} invoices",
        delta_color="inverse",
    )
with col4:
    st.metric(
        "Overdue Payments",
        f"AED {financials['total_overdue']:,.0f}",
        delta=f"{financials['overdue_count']} overdue",
        delta_color="inverse",
    )

# ---------------------------------------------------------------------------
# COLLECTION BREAKDOWN DONUT
# ---------------------------------------------------------------------------
collection_pct = financials["collection_pct"]
collected = financials["total_collected"]
outstanding_val = financials["total_outstanding"]
overdue_val = financials["total_overdue"]
pending_val = max(outstanding_val - overdue_val, 0)

fig_donut = go.Figure(data=[go.Pie(
    labels=["Collected", "Pending", "Overdue"],
    values=[collected, pending_val, overdue_val],
    hole=0.6,
    marker_colors=[c["CHART_SECONDARY"], c["CHART_PRIMARY"], c["CHART_TERTIARY"]],
    textinfo="percent+label",
    textfont={"color": c["TEXT"]},
    hovertemplate="<b>%{label}</b><br>AED %{value:,.0f}<br>%{percent}<extra></extra>",
)])
fig_donut.update_layout(**plotly_layout(
    height=350,
    title_text=f"Collection Rate: {collection_pct:.1f}%",
    showlegend=True,
    annotations=[{
        "text": f"AED {collected:,.0f}",
        "x": 0.5, "y": 0.5, "font_size": 16,
        "font_color": c["CHART_PRIMARY"],
        "showarrow": False,
    }],
))
st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# CLIENT FINANCIAL SUMMARY TABLE + HORIZONTAL BAR
# ---------------------------------------------------------------------------
st.subheader("📊 Client Financial Summary")

client_fin_raw = get_client_financial_breakdown()
if len(client_fin_raw) > 0:
    # Display copy with formatted currency
    client_fin_display = client_fin_raw.copy()
    for col_name in ["Contract Value (AED)", "Paid (AED)", "Outstanding (AED)"]:
        client_fin_display[col_name] = client_fin_display[col_name].apply(lambda x: f"AED {x:,.0f}")

    # Color-code status
    def style_status(status):
        if status == "Fully Paid":
            return f"🟢 {status}"
        elif status == "Payment Overdue":
            return f"🔴 {status}"
        else:
            return f"🟡 {status}"

    client_fin_display["Status"] = client_fin_display["Status"].apply(style_status)

    st.dataframe(client_fin_display, use_container_width=True, hide_index=True)

    # Stacked horizontal bar — paid vs outstanding per client
    st.subheader("📊 Client Revenue Breakdown")
    fig_hbar = go.Figure()
    fig_hbar.add_trace(go.Bar(
        y=client_fin_raw["Client"],
        x=client_fin_raw["Paid (AED)"],
        name="Paid",
        orientation="h",
        marker_color=c["CHART_SECONDARY"],
        hovertemplate="<b>%{y}</b><br>Paid: AED %{x:,.0f}<extra></extra>",
    ))
    fig_hbar.add_trace(go.Bar(
        y=client_fin_raw["Client"],
        x=client_fin_raw["Outstanding (AED)"],
        name="Outstanding",
        orientation="h",
        marker_color=c["CHART_TERTIARY"],
        hovertemplate="<b>%{y}</b><br>Outstanding: AED %{x:,.0f}<extra></extra>",
    ))
    fig_hbar.update_layout(**plotly_layout(
        height=300,
        barmode="stack",
        xaxis_title="Amount (AED)",
        xaxis_tickformat=",",
        yaxis_title="",
        legend={"orientation": "h", "y": 1.1},
    ))
    st.plotly_chart(fig_hbar, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# MONTHLY COLLECTIONS CHART
# ---------------------------------------------------------------------------
st.subheader("📈 Monthly Collections")

monthly_rev = get_monthly_revenue(6)
if len(monthly_rev) > 0:
    fig_monthly = go.Figure(data=[go.Bar(
        x=monthly_rev["month"],
        y=monthly_rev["total"],
        marker_color=c["CHART_PRIMARY"],
        hovertemplate="<b>%{x}</b><br>AED %{y:,.0f}<extra></extra>",
    )])
    fig_monthly.update_layout(**plotly_layout(
        height=350,
        xaxis_title="Month",
        yaxis_title="Amount (AED)",
        yaxis_tickformat=",",
    ))
    st.plotly_chart(fig_monthly, use_container_width=True)
else:
    st.info("No payment data available for chart.")

st.divider()

# ---------------------------------------------------------------------------
# RECENT PAYMENTS TABLE
# ---------------------------------------------------------------------------
st.subheader("💳 Recent Payments")

payments_df = get_payment_history(20)
if len(payments_df) > 0:
    # Format amount
    payments_df["Amount (AED)"] = payments_df["Amount (AED)"].apply(
        lambda x: f"AED {x:,.0f}"
    )
    # Style status
    payments_df["Status"] = payments_df["Status"].apply(
        lambda s: {
            "received": "✅ Received",
            "pending": "🟡 Pending",
            "overdue": "🔴 Overdue",
            "partial": "🟠 Partial",
        }.get(s, s)
    )
    # Format method
    payments_df["Method"] = payments_df["Method"].apply(
        lambda m: m.replace("_", " ").title() if m else "—"
    )
    st.dataframe(payments_df, use_container_width=True, hide_index=True)

st.divider()

# ---------------------------------------------------------------------------
# OUTSTANDING INVOICES
# ---------------------------------------------------------------------------
with st.expander("📋 View Outstanding Invoices"):
    outstanding_df = get_outstanding_invoices()
    if len(outstanding_df) > 0:
        # Format
        outstanding_df["Contract Value (AED)"] = outstanding_df["Contract Value (AED)"].apply(
            lambda x: f"AED {x:,.0f}"
        )
        outstanding_df["Amount Due (AED)"] = outstanding_df["Amount Due (AED)"].apply(
            lambda x: f"AED {x:,.0f}"
        )
        outstanding_df["Status"] = outstanding_df["Status"].apply(
            lambda s: {
                "pending": "🟡 Pending",
                "overdue": "🔴 Overdue",
            }.get(s, s)
        )
        st.dataframe(outstanding_df, use_container_width=True, hide_index=True)
    else:
        st.success("No outstanding invoices!")

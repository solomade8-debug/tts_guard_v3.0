"""
TTS Guard — Clients Page
Client directory with buildings, equipment, per-client financials and mini charts.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import date
from database import (
    get_all_clients,
    get_buildings_by_client,
    get_client_financial_detail,
    get_overdue_inspections,
)
from theme import get_colors, inject_css, plotly_layout

c = get_colors()
inject_css()

st.markdown(
    '<h1 class="fire-header">👥 Client Directory</h1>',
    unsafe_allow_html=True,
)

clients_df = get_all_clients()
overdue_df = get_overdue_inspections()
today = date.today()

for _, client in clients_df.iterrows():
    client_id = client["id"]
    buildings_df = get_buildings_by_client(client_id)
    financials = get_client_financial_detail(client_id)

    # Count total contract value for header
    total_value = financials["total_value"]

    with st.expander(
        f"**{client['name']}** ({client['short_name']}) — "
        f"{len(buildings_df)} buildings · AED {total_value:,.0f}/year"
    ):
        # Contact info
        st.markdown("**Contact Information**")
        ci1, ci2, ci3 = st.columns(3)
        with ci1:
            st.markdown(f"👤 {client['contact_person']}")
        with ci2:
            st.markdown(f"📞 {client['phone']}")
        with ci3:
            st.markdown(f"✉️ {client['email']}")

        st.divider()

        # Buildings table
        st.markdown("**Buildings**")
        if len(buildings_df) > 0:
            display_data = []
            for _, bld in buildings_df.iterrows():
                # Check overdue status
                is_overdue = len(
                    overdue_df[overdue_df["building_id"] == bld["id"]]
                ) > 0

                # Compute status
                if is_overdue:
                    status = "🔴 Overdue"
                elif bld["last_inspection"]:
                    days_since = (today - date.fromisoformat(bld["last_inspection"])).days
                    interval = 365 / (bld["visits_per_year"] or 4)
                    days_left = int(interval - days_since)
                    if days_left <= 14:
                        status = f"🟡 Due in {days_left}d"
                    else:
                        status = "✅ OK"
                else:
                    status = "🔴 No inspection"

                display_data.append({
                    "Building": bld["name"],
                    "Area": bld["area"],
                    "Equipment": bld["equipment_count"],
                    "Last Inspection": bld["last_inspection"] or "—",
                    "Contract Value": f"AED {bld['annual_value']:,.0f}" if bld["annual_value"] else "—",
                    "Status": status,
                })

            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
            )

        st.divider()

        # Financial summary with mini donut
        st.markdown("**Financial Summary**")
        fin_left, fin_right = st.columns([2, 1])

        with fin_left:
            f1, f2, f3 = st.columns(3)
            with f1:
                st.metric("Contract Value", f"AED {financials['total_value']:,.0f}")
            with f2:
                st.metric("Paid", f"AED {financials['total_paid']:,.0f}")
            with f3:
                outstanding_amt = financials["outstanding"]
                if outstanding_amt > 0:
                    st.metric(
                        "Outstanding",
                        f"AED {outstanding_amt:,.0f}",
                        delta=f"AED {outstanding_amt:,.0f} pending",
                        delta_color="inverse",
                    )
                else:
                    st.metric(
                        "Outstanding",
                        "AED 0",
                        delta="Fully paid",
                        delta_color="normal",
                    )

        with fin_right:
            paid = financials["total_paid"]
            outstanding_amt = financials["outstanding"]
            if paid > 0 or outstanding_amt > 0:
                pct = (paid / (paid + outstanding_amt) * 100) if (paid + outstanding_amt) > 0 else 0
                fig_mini = go.Figure(data=[go.Pie(
                    labels=["Paid", "Outstanding"],
                    values=[paid, outstanding_amt],
                    hole=0.6,
                    marker_colors=[c["CHART_SECONDARY"], c["CHART_TERTIARY"]],
                    textinfo="percent",
                    textfont={"color": c["TEXT"], "size": 10},
                    hovertemplate="<b>%{label}</b><br>AED %{value:,.0f}<extra></extra>",
                )])
                fig_mini.update_layout(**plotly_layout(
                    height=180,
                    showlegend=False,
                    margin={"l": 0, "r": 0, "t": 10, "b": 10},
                    annotations=[{
                        "text": f"{pct:.0f}%",
                        "x": 0.5, "y": 0.5, "font_size": 16,
                        "font_color": c["CHART_PRIMARY"],
                        "showarrow": False,
                    }],
                ))
                st.plotly_chart(fig_mini, use_container_width=True, key=f"donut_{client_id}")

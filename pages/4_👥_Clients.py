"""
TTS Guard — Clients Page
Client directory with buildings, equipment, and per-client financials.
"""

import streamlit as st
from datetime import date
from database import (
    get_all_clients,
    get_buildings_by_client,
    get_client_financial_detail,
    get_overdue_inspections,
)

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
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"👤 {client['contact_person']}")
        with c2:
            st.markdown(f"📞 {client['phone']}")
        with c3:
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

        # Financial summary
        st.markdown("**Financial Summary**")
        f1, f2, f3 = st.columns(3)
        with f1:
            st.metric("Contract Value", f"AED {financials['total_value']:,.0f}")
        with f2:
            st.metric("Paid", f"AED {financials['total_paid']:,.0f}")
        with f3:
            outstanding = financials["outstanding"]
            if outstanding > 0:
                st.metric(
                    "Outstanding",
                    f"AED {outstanding:,.0f}",
                    delta=f"AED {outstanding:,.0f} pending",
                    delta_color="inverse",
                )
            else:
                st.metric(
                    "Outstanding",
                    "AED 0",
                    delta="Fully paid",
                    delta_color="normal",
                )

"""
TTS Guard — Inspection Form Page
Submit inspections with grouped equipment, PDF download, and complaint creation.
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import date
from database import (
    get_all_buildings,
    get_building_details,
    get_equipment_by_building,
    get_equipment_grouped_by_type,
    insert_inspection,
    insert_complaint,
    TECHNICIANS,
)
from pdf_report import generate_inspection_pdf
from theme import get_colors, inject_css, plotly_layout

c = get_colors()
inject_css()

st.markdown(
    '<h1 class="fire-header">📋 Submit Inspection</h1>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# FORM FIELDS
# ---------------------------------------------------------------------------
buildings_df = get_all_buildings()
building_options = {
    f"{row['short_name']} — {row['name']}": row["id"]
    for _, row in buildings_df.iterrows()
}

selected_label = st.selectbox(
    "Select Building",
    options=list(building_options.keys()),
    index=None,
    placeholder="Choose a building...",
)

if selected_label is None:
    st.info("Select a building to begin the inspection.")
    st.stop()

building_id = building_options[selected_label]
building = get_building_details(building_id)

col1, col2 = st.columns(2)
with col1:
    technician = st.selectbox("Technician", TECHNICIANS)
with col2:
    inspection_date = st.date_input("Inspection Date", value=date.today())

st.divider()

# ---------------------------------------------------------------------------
# EQUIPMENT CHECKLIST — Grouped by Type with Expand
# ---------------------------------------------------------------------------
st.subheader("🔍 Equipment Checklist")
st.caption(f"**{building['name']}** — {building['equipment_count']} items")

equipment_df = get_equipment_by_building(building_id)
grouped_df = get_equipment_grouped_by_type(building_id)

# Track pass/fail per item using session state
if "equip_status" not in st.session_state or st.session_state.get("equip_building_id") != building_id:
    st.session_state.equip_status = {
        str(eid): True for eid in equipment_df["id"].tolist()
    }
    st.session_state.equip_building_id = building_id

equip_status = st.session_state.equip_status

# Dynamic counter
total = len(equipment_df)
passed = sum(1 for v in equip_status.values() if v)
failed = total - passed

pcol1, pcol2, pcol3 = st.columns(3)
with pcol1:
    st.metric("Total Items", total)
with pcol2:
    st.metric("✅ Passed", passed)
with pcol3:
    st.metric("⚠️ Failed", failed, delta_color="inverse" if failed > 0 else "off")

# Pass rate gauge (updates in real-time as checkboxes toggle)
pass_rate = (passed / total * 100) if total > 0 else 100
gauge_color = c["CHART_SECONDARY"] if pass_rate >= 80 else (
    c["CHART_PRIMARY"] if pass_rate >= 50 else c["STATUS_RED"]
)

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=pass_rate,
    number={"suffix": "%", "font": {"color": gauge_color, "size": 36}},
    gauge={
        "axis": {"range": [0, 100], "tickcolor": c["TEXT_MUTED"]},
        "bar": {"color": gauge_color},
        "bgcolor": c["BORDER"],
        "steps": [
            {"range": [0, 50], "color": "rgba(255,68,68,0.15)"},
            {"range": [50, 80], "color": "rgba(255,102,0,0.15)"},
            {"range": [80, 100], "color": "rgba(52,211,153,0.15)"},
        ],
        "threshold": {
            "line": {"color": c["STATUS_RED"], "width": 2},
            "thickness": 0.75,
            "value": 80,
        },
    },
    title={"text": "Pass Rate", "font": {"color": c["TEXT_MUTED"], "size": 14}},
))
fig_gauge.update_layout(**plotly_layout(
    height=220,
    margin={"l": 30, "r": 30, "t": 40, "b": 0},
))
st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")

# Grouped equipment with expanders
for _, group in grouped_df.iterrows():
    eq_type = group["type"]
    count = group["count"]
    item_ids = group["item_ids"].split(",")

    # Count passed in this group
    group_passed = sum(1 for eid in item_ids if equip_status.get(eid, True))
    group_failed = count - group_passed

    status_badge = "✅" if group_failed == 0 else f"⚠️ {group_failed} failed"

    with st.expander(f"{eq_type} ({count} items) — {status_badge}"):
        for eid in item_ids:
            equip_row = equipment_df[equipment_df["id"] == int(eid)].iloc[0]
            equip_status[eid] = st.checkbox(
                f"{eq_type} #{eid}",
                value=equip_status.get(eid, True),
                key=f"eq_{eid}",
            )

# Update session state
st.session_state.equip_status = equip_status

# Recalculate after checkboxes
passed = sum(1 for v in equip_status.values() if v)
failed = total - passed

st.divider()

# ---------------------------------------------------------------------------
# NOTES & SUBMIT
# ---------------------------------------------------------------------------
notes = st.text_area(
    "Inspection Notes",
    placeholder="Add any observations or comments about the inspection...",
)

if st.button("✅ Submit Inspection", use_container_width=True, type="primary"):
    # Insert inspection record
    inspection_id = insert_inspection(
        building_id=building_id,
        inspection_date=inspection_date.isoformat(),
        technician=technician,
        items_checked=total,
        items_passed=passed,
        items_failed=failed,
        notes=notes,
    )

    st.success(f"✅ Inspection for **{building['name']}** submitted successfully!")

    st.divider()

    # ---- WhatsApp Preview ----
    st.subheader("💬 WhatsApp Message Preview")
    whatsapp_msg = (
        f"✅ TTS Service Update\n\n"
        f"Dear {building['contact_person']},\n"
        f"TTS completed inspection at {building['name']} today.\n\n"
        f"🔍 Systems checked: {total}\n"
        f"✅ Passed: {passed}\n"
        f"⚠️ Needs attention: {failed}\n\n"
        f"— Talent Technical Services\n"
        f"📞 +971 2 66 78340"
    )
    st.info(whatsapp_msg)
    st.caption("💬 This message will be sent to client via WhatsApp automatically")

    st.divider()

    # ---- PDF Report Download ----
    st.subheader("📄 Inspection Report")

    # Build equipment details for PDF
    equipment_details = []
    for _, eq_row in equipment_df.iterrows():
        eid = str(eq_row["id"])
        status = "Passed" if equip_status.get(eid, True) else "Failed"
        equipment_details.append({
            "type": eq_row["type"],
            "status": status,
        })

    try:
        pdf_bytes = generate_inspection_pdf(
            building_name=building["name"],
            client_name=building["client_name"],
            inspection_date=inspection_date.isoformat(),
            technician=technician,
            items_checked=total,
            items_passed=passed,
            items_failed=failed,
            equipment_details=equipment_details,
            notes=notes or "",
        )

        filename = f"TTS_Inspection_{building['name'].replace(' ', '_')}_{inspection_date.isoformat()}.pdf"
        st.download_button(
            label="📥 Download Inspection Report (PDF)",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True,
        )
    except Exception as e:
        st.error(f"⚠️ PDF generation failed: {e}")
        st.caption("The inspection was saved successfully. PDF report can be regenerated later.")

    # ---- Create Complaint Ticket (if failures) ----
    if failed > 0:
        st.divider()
        st.subheader("🎫 Create Complaint Ticket")
        st.warning(f"⚠️ {failed} items failed inspection — create a follow-up ticket?")

        # Build failure message
        failed_items = []
        for _, eq_row in equipment_df.iterrows():
            eid = str(eq_row["id"])
            if not equip_status.get(eid, True):
                failed_items.append(eq_row["type"])

        # Count by type
        from collections import Counter
        fail_counts = Counter(failed_items)
        fail_msg = "Failed items during inspection: " + ", ".join(
            f"{count}x {etype}" for etype, count in fail_counts.items()
        )

        complaint_msg = st.text_area(
            "Complaint Message",
            value=fail_msg,
            key="complaint_msg",
        )

        cc1, cc2 = st.columns(2)
        with cc1:
            priority = st.selectbox(
                "Priority",
                ["medium", "high", "low"],
                key="complaint_priority",
            )
        with cc2:
            assign_tech = st.selectbox(
                "Assign Technician",
                ["(Unassigned)"] + TECHNICIANS,
                key="complaint_tech",
            )

        if st.button("🎫 Create Ticket", use_container_width=True):
            tech_val = None if assign_tech == "(Unassigned)" else assign_tech
            ticket = insert_complaint(
                client_id=building["client_id"],
                building_id=building_id,
                message=complaint_msg,
                priority=priority,
                assigned_technician=tech_val,
                inspection_id=inspection_id,
            )
            st.success(f"✅ Complaint ticket **{ticket}** created successfully!")

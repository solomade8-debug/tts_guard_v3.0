Build a complete Streamlit multi-page app called "TTS Guard" — an AMC management dashboard for a fire safety company called Talent Technical Services (TTS) in Abu Dhabi, UAE.

This is a DEMO to show the business owner what's possible. It should look professional, work smoothly, and feel like real software — not a student project.

## Tech Stack
- Python 3.11+
- Streamlit (latest)
- SQLite (single file database)
- Pandas

## Project Structure
```
tts-guard/
├── app.py                  # Main entry, page config, sidebar
├── database.py             # SQLite setup + all query functions  
├── seed_data.py            # Realistic sample data
├── requirements.txt        # streamlit, pandas
└── pages/
    ├── 1_📊_Dashboard.py   # Overview with key metrics
    ├── 2_🔴_Overdue.py     # Overdue inspections
    ├── 3_📋_Inspect.py     # Submit inspection form
    ├── 4_👥_Clients.py     # Client & building directory
    └── 5_📈_Reports.py     # Monthly summary reports
```

## Database (SQLite — tts_guard.db)

### clients
- id INTEGER PRIMARY KEY AUTOINCREMENT
- name TEXT (e.g. "First Abu Dhabi Bank")
- short_name TEXT (e.g. "FAB")  
- contact_person TEXT
- phone TEXT
- email TEXT

### buildings  
- id INTEGER PRIMARY KEY AUTOINCREMENT
- client_id INTEGER FK
- name TEXT (e.g. "FAB HQ Tower")
- area TEXT (e.g. "Al Maryah Island")

### contracts
- id INTEGER PRIMARY KEY AUTOINCREMENT
- building_id INTEGER FK
- start_date TEXT
- end_date TEXT
- visits_per_year INTEGER
- annual_value REAL (AED)
- status TEXT DEFAULT 'active'

### equipment
- id INTEGER PRIMARY KEY AUTOINCREMENT
- building_id INTEGER FK
- type TEXT (e.g. "Fire Alarm Panel", "Smoke Detector", "Fire Extinguisher DCP", "Fire Extinguisher CO2", "Sprinkler System", "Emergency Light", "Hose Reel", "Exit Sign", "FM200 System")
- status TEXT DEFAULT 'OK'

### inspections
- id INTEGER PRIMARY KEY AUTOINCREMENT
- building_id INTEGER FK
- inspection_date TEXT
- technician TEXT
- items_checked INTEGER
- items_passed INTEGER
- items_failed INTEGER
- notes TEXT
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

### complaints
- id INTEGER PRIMARY KEY AUTOINCREMENT
- ticket_number TEXT (auto-generate as TTS-2026-XXXX)
- client_id INTEGER FK
- building_id INTEGER FK  
- message TEXT
- priority TEXT (high/medium/low)
- status TEXT (open/assigned/in_progress/resolved)
- created_at TEXT DEFAULT CURRENT_TIMESTAMP

## Seed Data — Make it realistic

8 real TTS clients with real Abu Dhabi locations:

1. **First Abu Dhabi Bank (FAB)** — FAB HQ Tower (Al Maryah Island, 24 equip), FAB Al Wahda Branch (8 equip), FAB Khalifa City Branch (6 equip)
2. **Farnek Services** — Farnek HQ (Musaffah, 18 equip), Staff Accommodation (ICAD, 12 equip)
3. **Khidmah LLC** — Tower A (Al Reem Island, 32 equip), Tower B (Al Reem Island, 28 equip), Community Center (Al Reef, 10 equip)
4. **MPM Properties** — Office Complex (Hamdan Street, 14 equip), Warehouse (Mussafah, 8 equip)
5. **United Real Estate** — Commercial Tower (Corniche Road, 22 equip), Residential Block (Tourist Club, 16 equip)
6. **Al Reef Villas** — Cluster A 50 villas (Al Reef, 50 equip), Cluster B 45 villas (Al Reef, 45 equip)
7. **Reem Island Tower Mgmt** — Reem Heights (Al Reem Island, 38 equip), Reem Plaza Mall (26 equip)
8. **Yas Plaza Hotels** — Hotel Main (Yas Island, 42 equip), Conference Center (20 equip)

Inspection status mix (relative to today Feb 21, 2026):
- 4 buildings: OVERDUE (next inspection was due 5-35 days ago)
- 5 buildings: DUE WITHIN 14 DAYS  
- 9 buildings: COMPLETED in last 20 days

5 technicians: Mohammed Al-Rashid, Suresh Kumar, Ahmed Mansoor, Rajesh Nair, Khalid Ibrahim

Contract values: AED 15,000 - 55,000/year randomly assigned

5 sample complaints with mixed priorities and statuses.

## Pages — What each should show

### app.py
- st.set_page_config(page_title="TTS Guard", page_icon="🔥", layout="wide")
- Sidebar: TTS Guard logo text, "Talent Technical Services", today's date, "Abu Dhabi, UAE"
- Sidebar: "🔄 Reset Demo Data" button that re-seeds database
- Auto-init database on first run

### 1_📊_Dashboard.py — The money page

TOP ROW — 4 metric cards using st.metric:
- Total Active Contracts (number)
- 🔴 Overdue (number, red delta showing "need attention")  
- 🟡 Due Within 14 Days (number)
- 🟢 Completed This Month (number)

ALERT BANNER — if overdue > 0:
- Red st.error box: "⚠️ {X} inspections overdue — Risk of Civil Defence non-compliance"

TWO COLUMNS:
- Left: "Upcoming Inspections" — st.dataframe showing building, client, due date, days remaining, sorted by most urgent
- Right: "Recent Complaints" — show each complaint as st.container with ticket number, priority color, message, client, time

BOTTOM — "Client Overview" table:
- st.dataframe with columns: Client | Buildings | Equipment | Status | Annual Value (AED)
- Status column: show "X overdue" in red or "✅ All clear" in green
- Sort by annual value descending

### 2_🔴_Overdue.py

- Header showing count: "🔴 X Overdue Inspections"
- For each overdue building, show a st.container card with:
  - Building name (large)
  - Client name
  - Area
  - Days overdue (big red number using st.metric with negative delta)
  - Last inspection date
  - Equipment count
  - Contract value
  - "Mark as Scheduled" button — when clicked, shows st.success

Sort by most days overdue first.

### 3_📋_Inspect.py — Submit Inspection

- st.selectbox: Select Building (format: "FAB — FAB HQ Tower")
- st.selectbox: Select Technician
- st.date_input: Inspection Date (default today)

When building is selected, show its equipment:
- Each equipment item as a row with st.checkbox (default checked = passed)
- Count passed/failed dynamically as user checks/unchecks

- st.text_area: Notes
- st.button: "✅ Submit Inspection"

On submit:
- Insert into inspections table
- Show st.success: "Inspection for {building} submitted successfully!"
- Show st.info box with formatted WhatsApp preview message:
```
✅ TTS Service Update

Dear {client_name},
TTS completed inspection at {building} today.

🔍 Systems checked: {count}
✅ Passed: {passed}  
⚠️ Needs attention: {failed}

— Talent Technical Services
📞 +971 2 66 78340
```
- Show caption: "💬 This message will be sent to client via WhatsApp automatically"

### 4_👥_Clients.py

- Show each client as st.expander
- When expanded show:
  - Contact person, phone, email
  - Table of all buildings: Building Name | Area | Equipment Count | Last Inspection | Contract Value | Status
  - Total contract value for this client

### 5_📈_Reports.py

- st.selectbox: Select Month (show last 3 months)
- Show summary metrics:
  - Total inspections completed
  - Total equipment checked  
  - Compliance rate (% completed on time)
  - Total complaints received vs resolved
- Simple bar chart (st.bar_chart): Inspections per client
- Simple chart: Complaints by priority

## Styling

Add custom CSS via st.markdown("""<style>...</style>""", unsafe_allow_html=True):
- Make metric cards look polished
- Color code: Red (#FF4B4B) for overdue, Amber (#FFA500) for due soon, Green (#00C853) for completed
- Clean tables with good spacing
- Professional feel — this needs to look like real business software

## Important Rules
- All dates relative to today (February 21, 2026)
- Currency always in AED
- UAE phone format (+971...)
- App must work 100% offline with seed data
- Database file: tts_guard.db in project root
- requirements.txt: streamlit, pandas
- Run with: streamlit run app.py
- No external APIs needed — everything local
- Make it feel like REAL software, not a tutorial project

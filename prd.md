# TTS Guard — Product Requirements Document

## 1. Executive Summary

**TTS Guard** is an AMC (Annual Maintenance Contract) management dashboard for **Talent Technical Services (TTS)**, a fire safety company based in Abu Dhabi, UAE. The platform provides real-time visibility into inspection schedules, compliance risk, client relationships, and financial performance across all AMC contracts.

**Target Users:** TTS business owner, operations manager, and field technicians.

**Demo Audience:** This demo is built to convince the TTS business owner to invest in developing TTS Guard as a real product. It must look and feel like production software.

**Key Value Proposition:** Centralized tracking of inspections, compliance status, and revenue — replacing manual spreadsheets and WhatsApp-based coordination with a professional dashboard that surfaces overdue inspections, financial outstanding, and client health at a glance.

---

## 2. Market Analysis

### 2.1 Market Opportunity

| Metric | Value | Source |
|--------|-------|--------|
| UAE Fire Protection Systems Market (2025) | USD 4.7 billion | MarketsandMarkets |
| UAE Fire Protection Systems Market (2031 projected) | USD 8.6 billion (CAGR 10.4%) | MarketsandMarkets |
| GCC Fire Safety Equipment Market (2024) | USD 1.91 billion | The Report Cubes |
| GCC Fire Safety Equipment Market (2034 projected) | USD 3.2 billion (CAGR 5.93%) | The Report Cubes |
| Global Fire Prevention Inspection Software (2023) | USD 500 million | Dataintelo |
| Global Fire Prevention Inspection Software (2032 projected) | USD 1.2 billion (CAGR 10.2%) | Dataintelo |
| UAE Facility Management Market (2026 projected) | USD 23.86 billion | Industry reports |

**Critical finding:** No major software solution exists purpose-built for AMC management in the UAE/GCC fire safety context. All existing solutions target NFPA (US) or AS 1851 (Australia) compliance frameworks.

### 2.2 Competitive Landscape

#### Direct Competitors — Fire Safety Inspection Software

| Software | What It Does | Key Features | Pricing | UAE Presence |
|----------|-------------|--------------|---------|-------------|
| **Inspect Point** | NFPA-compliant fire inspection software | AI inspection assistant, NFPA forms, deficiency-to-proposal, scheduling, barcode scanning | Custom enterprise | None |
| **Uptick** | All-in-one fire protection platform (1,000+ companies) | Digital inspection forms, route planning, defect quoting, Xero/QuickBooks integration | Per-user/month | None |
| **ServiceTrade** | Fire protection service management | NFPA forms, inspection agreements, customer portal, deficiency reporting | Custom tiered (Select/Premium/Enterprise) | None |
| **BuildOps** | End-to-end field service for commercial FLS | Asset-oriented CRM, AI mobile app, NFPA checklists, Smart Dispatch AI | Custom enterprise | None |
| **ZenFire** (ZenTrades) | Cloud-based fire inspection CRM | Customizable checklists, NFPA forms, proposal generation, 50+ integrations | From $60/month | None |
| **FirePro365** | Fire CRM on Microsoft Dynamics 365 | Automated scheduling, field mobile app, asset management, Microsoft ecosystem integration | Custom | None (Dynamics has GCC presence) |
| **SafetyCulture** (iAuditor) | General inspection platform (adaptable to fire) | Custom templates, mobile app, photo capture, corrective actions, analytics | Free (10 users) to $24/user/month | Global, no fire-specific UAE customization |
| **Klipboard** | Field service management (fire vertical) | Asset management, overdue alerts, drag-and-drop scheduler, automated communications | From ~$37/month | None (UK-focused) |
| **BuildingReports** | Barcode-scanning inspection suite | FireScan, SprinklerScan, SuppressionScan; NFPA compliant; 13M+ inspections completed | Per-application or suite | None |
| **InspectNTrack** | Mobile fire inspection tracking | Barcode/QR/NFC scanning, recurring schedules, offline capability, extinguisher inventory | $1,500-$2,900/year | None |

#### Adjacent Competitors — UAE-Based Facility Management Software

| Software | Type | Key Features | UAE Presence |
|----------|------|--------------|-------------|
| **Horizon FMS** (Frontline IT) | CAFM/CMMS | Site surveys, asset management, PPM schedules, vendor management, mobile app | **HQ in Dubai** |
| **Facilio** | AI/IoT-driven CMMS | AI work order automation, offline mobile, condition-based maintenance, SLA tracking | **Active in UAE/GCC** |
| **Focus Centra CAFM** | CAFM | Preventive maintenance, work orders, asset tracking, vendor management | **All 7 Emirates** |
| **MRI Evolution** | CAFM | Integrated hard/soft FM, AI and IoT, automation and analytics | **UAE (MEFMA member)** |

**Key observation:** UAE-based FM platforms cover fire equipment as part of general facility management but lack fire-safety-specific workflows, Civil Defence compliance forms, or AMC lifecycle management.

### 2.3 Market Gaps — TTS Guard Opportunity

| # | Gap | Detail | TTS Guard Advantage |
|---|-----|--------|-------------------|
| 1 | **No UAE Civil Defence-native software** | All fire inspection tools use NFPA (US) forms. None support DCD/ADCDA inspection formats or approval workflows. | Built from the ground up for UAE Civil Defence compliance |
| 2 | **AMC lifecycle management unserved** | No tool manages the full AMC cycle: contract creation, equipment scope per building, scheduling, renewal tracking, billing, client notifications. | End-to-end AMC contract and inspection tracking |
| 3 | **No Civil Defence documentation workflow** | UAE fire companies must produce specific documentation for Civil Defence submissions (fitness certificates, NOCs). No software generates or tracks these. | DCD/ADCDA documentation templates (future) |
| 4 | **No Hassantuk integration awareness** | Hassantuk (mandatory connected fire monitoring) is expanding but no software tracks compliance status alongside AMC records. | Hassantuk compliance tracking (future) |
| 5 | **No Arabic/bilingual support** | Every fire inspection tool is English-only and Western-centric. | Bilingual Arabic/English interface (future) |
| 6 | **No affordable SMB pricing** | Most tools charge $30-350/user/month or require enterprise contracts. UAE has many small contractors (5-30 technicians). | SMB-friendly pricing model |
| 7 | **No multi-Emirate compliance tracking** | Each Emirate has slightly different enforcement. No tool helps companies operating across jurisdictions. | Multi-Emirate dashboard (future) |
| 8 | **No UAE business system integration** | No fire tool integrates with Tally accounting (popular in UAE), UAE VAT, WPS, or local ERPs. | UAE ecosystem integration (future) |
| 9 | **No building owner portal** | UAE building owners must demonstrate fire safety compliance to Civil Defence. No dedicated portal exists. | Client-facing portal (future) |
| 10 | **No equipment-to-code mapping** | UAE buildings must maintain equipment per Civil Defence specs tied to building classification. No tool maps this. | Code-driven equipment requirements (future) |

### 2.4 Regulatory Demand Drivers

**UAE Civil Defence AMC Requirements:**
- Annual Maintenance Contracts are **mandatory** for all UAE buildings
- Monthly functionality tests and annual comprehensive testing required
- AMC providers must hold DCD/ADCDA approval to operate
- Annual renewal requires submission of updated inspection records, proof of timely servicing, and clearance of violations

**Hassantuk (Mandatory Fire Monitoring):**
- Commercial buildings: already covered under Hassantuk Commercial (operated by Injazat/Civil Defence)
- Residential (villas/townhouses): mandatory since January 1, 2024 via Hassantuk Homes (operated by e&)
- Real-time smoke/heat detection with emergency dispatch within 120 seconds
- Coverage expanding to additional building types

**Penalties for Non-Compliance:**
- Administrative fines up to AED 50,000
- Temporary shutdown until corrective measures verified
- Possible trade license suspension

**Referenced Standards:**
- NFPA 10 (Portable Fire Extinguishers)
- NFPA 25 (Water-Based Fire Protection Systems)
- NFPA 72 (Fire Alarm Systems)
- NFPA 70E (Electrical Safety)

### 2.5 Industry Trends

1. **Regulatory tightening** — UAE Civil Defence strengthening inspection regimes in 2025-2026
2. **AI adoption** — Abu Dhabi Civil Defence partnering with Advanced Technology Research Council for AI in emergency operations
3. **Hassantuk expansion** — Mandatory coverage growing beyond commercial to residential
4. **Digital transformation** — Shift from paper-based to digital inspection management accelerating, but slow among smaller contractors
5. **Mega-projects driving demand** — Giga-projects across UAE/Saudi creating massive AMC pipeline
6. **Skills gap** — GCC faces estimated shortage of 10,000+ trained fire protection professionals, driving demand for workflow-simplifying software

### 2.6 Strategic Positioning

TTS Guard occupies a **blue-ocean position**: purpose-built for UAE fire safety AMC workflow in a market where all competitors are US/Australia-focused. The competitive moat is deep regional specialization in a geography where global players have no presence and no incentive to localize.

**Competitive positioning matrix:**

```
                    Fire-Safety Specific
                          |
    Inspect Point    BuildOps
    Uptick           ServiceTrade
    ZenFire                         ← TTS Guard (target position)
                          |
    ──────────────────────+──────────────────────
    Global/US Focus       |         UAE/GCC Focus
                          |
    SafetyCulture         Horizon FMS
    Simpro                Facilio
    Klipboard             Focus CAFM
                          |
                    General FM/Field Service
```

---

## 3. Product Overview

### 3.1 Company Context
**Talent Technical Services (TTS)** is a fire safety AMC provider operating in Abu Dhabi, UAE. TTS manages annual maintenance contracts for fire protection systems across commercial buildings, residential complexes, hotels, and office spaces.

### 3.2 Problem Statement
Manual tracking via spreadsheets and WhatsApp leads to:
- Missed inspections risking Civil Defence non-compliance (fines up to AED 50,000)
- No visibility into upcoming vs overdue inspections
- Revenue leakage from untracked payments and expired contracts
- Inefficient client communication
- No consolidated view of business health

### 3.3 Solution
TTS Guard is a centralized dashboard providing:
- Real-time inspection status (overdue/upcoming/completed)
- Client and building management
- Equipment-level inspection tracking
- Financial overview (contract values, payments, outstanding)
- Automated client communication preview (WhatsApp)
- Monthly compliance and performance reports

---

## 4. Technical Architecture

### 4.1 Tech Stack
| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Language | Python 3.11+ | Mature ecosystem, Streamlit compatibility |
| Frontend/Backend | Streamlit (latest) | Rapid prototyping, professional UI, zero frontend code |
| Database | SQLite (single file) | Zero configuration, offline capable, portable |
| Data Processing | Pandas | DataFrames for tables and charts |
| PDF Generation | fpdf2 | Lightweight PDF library for inspection reports |

### 4.2 Deployment
- **Demo mode:** Local execution via `streamlit run app.py`
- **Database:** Single file `tts_guard.db` in project root
- **Dependencies:** `streamlit`, `pandas`, `fpdf2` (in `requirements.txt`)
- **Offline:** 100% offline with seed data, no external APIs

### 4.3 Project Structure
```
TTS_bot/
├── prd.md                      # This document
├── requirements.txt            # streamlit, pandas, fpdf2
├── app.py                      # Entry point: welcome page, sidebar, DB init
├── database.py                 # SQLite schema (7 tables) + query functions
├── seed_data.py                # Realistic demo data (6 months history)
├── pdf_report.py               # PDF inspection report generator
├── assets/
│   └── logo_placeholder.png    # TTS logo (replace with real logo)
└── pages/
    ├── 1_📊_Dashboard.py       # Key metrics, alerts, financial snapshot
    ├── 2_🔴_Overdue.py         # Overdue inspections with scheduling
    ├── 3_📋_Inspect.py         # Submit inspection + PDF + complaint creation
    ├── 4_👥_Clients.py         # Client & building directory with financials
    ├── 5_📈_Reports.py         # Monthly summary reports (6 months)
    └── 6_💰_Financials.py      # Financial tally
```

---

## 5. Database Schema

### 5.1 Entity Relationship (8 tables)

```
clients (1) ──── (N) buildings (1) ──── (1) contracts (1) ──── (N) payments
                      |
                      ├──── (N) equipment
                      |
                      ├──── (N) inspections ──── (N) complaints (via inspection_id)
                      |
                      └──── (N) scheduled_inspections

clients (1) ──── (N) complaints ──── (1) buildings
```

### 5.2 Table Definitions

#### `clients`
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| name | TEXT | NOT NULL (e.g. "First Abu Dhabi Bank") |
| short_name | TEXT | NOT NULL (e.g. "FAB") |
| contact_person | TEXT | |
| phone | TEXT | UAE format (+971...) |
| email | TEXT | |

#### `buildings`
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| client_id | INTEGER | FK → clients(id) |
| name | TEXT | NOT NULL (e.g. "FAB HQ Tower") |
| area | TEXT | (e.g. "Al Maryah Island") |

#### `contracts`
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| building_id | INTEGER | FK → buildings(id) |
| start_date | TEXT | NOT NULL |
| end_date | TEXT | NOT NULL |
| visits_per_year | INTEGER | DEFAULT 4 |
| annual_value | REAL | NOT NULL (AED) |
| status | TEXT | DEFAULT 'active' |

#### `equipment`
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| building_id | INTEGER | FK → buildings(id) |
| type | TEXT | NOT NULL (9 types — see Section 7.1) |
| status | TEXT | DEFAULT 'OK' |

#### `inspections`
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| building_id | INTEGER | FK → buildings(id) |
| inspection_date | TEXT | NOT NULL |
| technician | TEXT | NOT NULL |
| items_checked | INTEGER | DEFAULT 0 |
| items_passed | INTEGER | DEFAULT 0 |
| items_failed | INTEGER | DEFAULT 0 |
| notes | TEXT | |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

#### `complaints`
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| ticket_number | TEXT | NOT NULL UNIQUE (format: TTS-YYYY-XXXX) |
| client_id | INTEGER | FK → clients(id) |
| building_id | INTEGER | FK → buildings(id) |
| message | TEXT | NOT NULL |
| priority | TEXT | CHECK(high/medium/low) DEFAULT 'medium' |
| status | TEXT | CHECK(open/assigned/in_progress/resolved) DEFAULT 'open' |
| assigned_technician | TEXT | (nullable — set when assigned) |
| inspection_id | INTEGER | FK → inspections(id), nullable — links to source inspection if created from failed items |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

#### `scheduled_inspections` (Overdue → Scheduling)
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| building_id | INTEGER | FK → buildings(id) |
| scheduled_date | TEXT | NOT NULL |
| assigned_technician | TEXT | NOT NULL |
| status | TEXT | CHECK(scheduled/completed/cancelled) DEFAULT 'scheduled' |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

#### `payments` (Financial Tally)
| Column | Type | Constraints |
|--------|------|------------|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
| contract_id | INTEGER | FK → contracts(id) |
| payment_date | TEXT | NOT NULL |
| amount | REAL | NOT NULL (AED) |
| method | TEXT | CHECK(bank_transfer/cheque/cash/online) DEFAULT 'bank_transfer' |
| reference_number | TEXT | (cheque number or transfer ref) |
| status | TEXT | CHECK(received/pending/overdue/partial) DEFAULT 'received' |
| notes | TEXT | |
| created_at | TEXT | DEFAULT CURRENT_TIMESTAMP |

---

## 6. Feature Specifications

### 6.1 Welcome Page & App Shell (`app.py`) — P0

**Page Configuration:**
- Title: "TTS Guard"
- Icon: fire emoji
- Layout: wide

**Welcome Page (home/landing):**
- TTS logo (from assets/ — falls back to styled text if missing)
- "TTS Guard" branding with fire gradient styling
- Tagline: "AMC Management Dashboard — Talent Technical Services"
- Key stats row: Total Clients, Total Buildings, Active Contracts, Total Equipment
- "Take a Tour" button — launches guided walkthrough highlighting key features on each page
- Quick navigation cards to each section

**Sidebar (visible on all pages):**
- TTS logo + "TTS Guard" branding with fire icon
- "Talent Technical Services"
- Today's date (dynamic)
- "Abu Dhabi, UAE"
- "Demo Notes" expander — presenter's cheat sheet with bullet points per page
- "Reset Demo Data" button — **two-step confirmation** (first click shows warning, second confirms)

**Auto-initialization:** Database and seed data created on first run.

### 6.2 Dashboard (`1_📊_Dashboard.py`) — P0

**Top Row — 4 Inspection Metric Cards:**
| Metric | Display |
|--------|---------|
| Total Active Contracts | Count |
| Overdue | Count with red delta "need attention" |
| Due Within 14 Days | Count |
| Completed This Month | Count |

**Alert Banner:**
- If overdue > 0: red error box — "X inspections overdue — Risk of Civil Defence non-compliance"

**Financial Health Section (prominent):**
- 4 financial metric cards: Total Contract Value, Collected, Outstanding, Overdue Payments
- Collection rate progress bar with percentage
- Links to full Financials page for detail

**Two Columns:**
- **Left:** "Upcoming Inspections" — dataframe with building, client, due date, days remaining (sorted by most urgent)
- **Right:** "Recent Complaints" — each complaint as container with ticket number, priority color, message, client, timestamp

**Bottom — Client Overview Table:**
- Columns: Client | Buildings | Equipment | Status | Annual Value (AED)
- Status: "X overdue" (red) or "All clear" (green)
- Sorted by annual value descending

### 6.3 Overdue Inspections (`2_🔴_Overdue.py`) — P0

**Header:** "X Overdue Inspections" with count

**For each overdue building (sorted by most days overdue):**
- Building name (large text)
- Client name
- Area
- Days overdue (big red metric with negative delta)
- Last inspection date
- Equipment count
- Contract value
- "Mark as Scheduled" button — on click, shows:
  - Date picker (select planned inspection date)
  - Technician dropdown (select from 5 technicians)
  - "Confirm Schedule" button → persists to database (adds scheduled_date and assigned_technician to building record), removes from overdue list, shows success toast

### 6.4 Inspection Form (`3_📋_Inspect.py`) — P0

**Form Fields:**
- Select Building (format: "FAB — FAB HQ Tower")
- Select Technician
- Inspection Date (default: today)

**Equipment Checklist (shown when building selected):**
- Equipment grouped by type (e.g., "Smoke Detector (6 items)")
- Click to expand each group to see individual items with checkboxes
- Default: all checked (passed)
- Dynamic pass/fail counter at top showing totals

**Submission:**
- Notes text area
- "Submit Inspection" button
- On submit: insert record, show success message

**Post-Submission Actions:**
1. **WhatsApp Preview** — show formatted message in st.info:
   ```
   TTS Service Update

   Dear {client_name},
   TTS completed inspection at {building} today.

   Systems checked: {count}
   Passed: {passed}
   Needs attention: {failed}

   — Talent Technical Services
   +971 2 66 78340
   ```
   Caption: "This message will be sent to client via WhatsApp automatically"

2. **PDF Report Download** — "Download Inspection Report (PDF)" button
   - Generates a professional PDF using fpdf2:
     - TTS branded header (logo if available, else text) + company info
     - Building details, inspection date, technician name
     - Summary: items checked, passed, failed
     - Full equipment checklist with pass/fail status per item
     - Notes section
     - Signatures section (inspector + client representative fields)
     - Civil Defence reference section at bottom (reference number field, compliance certification text)
   - Auto-named: `TTS_Inspection_{building}_{date}.pdf`

3. **Create Complaint Ticket** (shown only if items_failed > 0):
   - Pre-filled message from failed items (e.g., "Failed items during inspection: 2x Smoke Detector, 1x Emergency Light")
   - Priority dropdown (default: medium)
   - Technician assignment dropdown (select from 5 technicians)
   - "Create Ticket" button → inserts complaint with auto-generated ticket number, shows success

### 6.5 Client Directory (`4_👥_Clients.py`) — P1

**For each client (as expander):**
- Contact person, phone, email
- Buildings table: Building Name | Area | Equipment Count | Last Inspection | Contract Value | Status
- Total contract value for client
- Per-client financial summary (paid vs outstanding)

### 6.6 Reports (`5_📈_Reports.py`) — P1

**Controls:**
- Select Month (last 6 months — extended for richer data)

**Summary Metrics:**
- Total inspections completed
- Total equipment checked
- Compliance rate (% completed on time)
- Complaints received vs resolved

**Charts:**
- Bar chart: inspections per client
- Bar chart: complaints by priority

### 6.7 Financial Tally (`6_💰_Financials.py`) — P1

**Top Row — 4 Financial Metrics:**
| Metric | Display |
|--------|---------|
| Total Contract Value | AED amount |
| Collected | AED amount with % delta |
| Outstanding | AED amount with invoice count |
| Overdue Payments | AED amount with overdue count (red) |

**Collection Rate Progress Bar:**
- Visual progress showing collection percentage

**Client Financial Summary Table:**
- Columns: Client | Contract Value (AED) | Paid (AED) | Outstanding (AED) | Status
- Status colors: "Fully Paid" (green), "Partially Paid" (amber), "Payment Overdue" (red)

**Recent Payments:**
- Table: Date | Client | Building | Amount (AED) | Method | Reference | Status

**Monthly Collections Chart:**
- Bar/line chart showing monthly revenue for last 6-12 months

**Outstanding Invoices (Expandable):**
- Table: Client | Building | Contract Value | Amount Due | Due Date | Days Overdue | Status

---

## 7. Data Requirements

### 7.1 Equipment Types (9 types)
Fire Alarm Panel, Smoke Detector, Fire Extinguisher DCP, Fire Extinguisher CO2, Sprinkler System, Emergency Light, Hose Reel, Exit Sign, FM200 System

### 7.2 Clients and Buildings (8 clients, 18 buildings)

| Client | Buildings (Equipment Count) |
|--------|---------------------------|
| First Abu Dhabi Bank (FAB) | FAB HQ Tower, Al Maryah Island (24); Al Wahda Branch (8); Khalifa City Branch (6) |
| Farnek Services | Farnek HQ, Musaffah (18); Staff Accommodation, ICAD (12) |
| Khidmah LLC | Tower A, Al Reem Island (32); Tower B, Al Reem Island (28); Community Center, Al Reef (10) |
| MPM Properties | Office Complex, Hamdan Street (14); Warehouse, Mussafah (8) |
| United Real Estate | Commercial Tower, Corniche Road (22); Residential Block, Tourist Club (16) |
| Al Reef Villas | Cluster A 50 Villas, Al Reef (50); Cluster B 45 Villas, Al Reef (45) |
| Reem Island Tower Mgmt | Reem Heights, Al Reem Island (38); Reem Plaza Mall (26) |
| Yas Plaza Hotels | Hotel Main, Yas Island (42); Conference Center (20) |

**Total: 419 equipment items across 18 buildings**

### 7.3 Inspection Status Distribution (relative to Feb 21, 2026)

| Status | Count | Detail |
|--------|-------|--------|
| OVERDUE | 4 buildings | Next inspection was due 5-35 days ago |
| DUE WITHIN 14 DAYS | 5 buildings | Next inspection due within 14 days |
| COMPLETED RECENTLY | 9 buildings | Inspected within last 20 days |

### 7.4 Technicians
Mohammed Al-Rashid, Suresh Kumar, Ahmed Mansoor, Rajesh Nair, Khalid Ibrahim

### 7.5 Contract Values
AED 15,000 — 55,000/year (proportional to building size)

### 7.6 Complaints
5 sample complaints with mixed priorities (high/medium/low) and statuses (open/assigned/in_progress/resolved)

### 7.7 Payment Data (Financial Tally)

**Billing Terms (mixed — realistic for UAE market):**
| Client Size | Payment Terms | Clients |
|-------------|--------------|---------|
| Large (FAB, Khidmah) | Quarterly (4x/year) | 2 clients |
| Medium (Farnek, URE, RITM, YPH) | Semi-annual (2x/year) | 4 clients |
| Small (MPM, Al Reef Villas) | Annual upfront | 2 clients |

**Payment Status Distribution:**
| Category | Count | Detail |
|----------|-------|--------|
| Fully Paid | 6 contracts | All installments received |
| Partially Paid (next pending) | 5 contracts | Current installments received, next pending |
| Payment Overdue | 4 contracts | One or more installments past due |
| Partial Payment | 3 contracts | 60-80% of an installment received |

**Financial totals:** ~AED 540K total contract value, ~AED 375K collected (69%), ~AED 165K outstanding, ~AED 75K overdue.

**Seed data covers 6 months of payment history** for meaningful monthly collections charts.

---

## 8. UI/UX Requirements

### 8.1 Color System — Fire Gradient Theme
| Color | Hex | Usage |
|-------|-----|-------|
| Primary (Fire Red) | #D32F2F | Headers, primary actions, branding |
| Gradient end (Orange) | #FF6F00 | Gradient accents, hover states |
| Alert Red | #FF4B4B | Overdue, alerts, non-compliance |
| Amber | #FFA500 | Due soon, partial payment, warnings |
| Success Green | #00C853 | Completed, all clear, fully paid |
| Background | #FAFAFA | Page background |
| Text | #212121 | Primary text (charcoal) |

**Theme direction:** White base with warm red-to-orange gradient accents — energetic, distinctly fire safety themed. Reference: ttsuae.com uses clean white/grey; the fire gradient adds identity.

### 8.2 Layout
- Wide mode enabled
- Responsive columns for metric cards
- Clean tables with good spacing
- Professional feel — must look like real business software, not a tutorial project
- Fire gradient applied to headers, sidebar accents, and metric card borders

### 8.3 Custom CSS
Applied via `st.markdown` with `unsafe_allow_html=True`:
- Fire gradient header bars
- Polished metric cards with colored left borders
- Color-coded status indicators
- Clean dataframe styling
- Consistent spacing and borders
- Gradient accent on sidebar branding

---

## 9. Non-Functional Requirements

| Requirement | Detail |
|-------------|--------|
| Offline operation | 100% functional with seed data, no external APIs |
| Single-command startup | `streamlit run app.py` |
| Auto-initialization | Database and seed data created on first run |
| Demo data reset | Sidebar button with two-step confirmation re-seeds all data |
| Currency | All values in AED |
| Phone format | UAE format (+971...) |
| Date handling | **Dynamic** — all dates computed relative to today (not a frozen date). Seed data uses offsets from today so the demo stays fresh regardless of when it's opened. |
| Seed data depth | 6 months of historical inspection and payment data for rich reports and charts |
| Database | SQLite single file (tts_guard.db) in project root |
| Guided tour | "Take a Tour" button on welcome page walks through key features with callouts |
| Logo | Placeholder in assets/ — user will replace with real TTS logo |

---

## 10. Future Roadmap (Out of Scope for Demo)

### Phase 2 — Core Enhancements
- User authentication and role-based access
- WhatsApp API integration (actual message sending)
- PDF report generation for Civil Defence submissions
- Arabic/English bilingual interface

### Phase 3 — Platform Features
- Cloud deployment (Streamlit Cloud or AWS)
- Multi-Emirate compliance tracking (DCD, ADCDA, Sharjah CD)
- Hassantuk compliance status tracking
- Mobile-responsive design enhancements

### Phase 4 — Ecosystem Integration
- Tally accounting integration
- UAE VAT compliance
- Automated email/SMS reminders
- Building owner / property manager portal
- Equipment-to-Civil-Defence-code mapping

### Phase 5 — Intelligence
- AI-powered inspection scheduling optimization
- Predictive maintenance recommendations
- Anomaly detection in equipment failure patterns
- Automated compliance risk scoring

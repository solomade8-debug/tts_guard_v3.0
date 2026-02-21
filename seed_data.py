"""
TTS Guard — Seed Data
Generates realistic demo data with dates as offsets from today.
Covers 6 months of history for rich reports and charts.
"""

import sqlite3
import random
from datetime import date, timedelta
from database import get_connection, TECHNICIANS

random.seed(42)  # Reproducible but realistic

TODAY = date.today()


def seed():
    """Seed the database with all demo data."""
    conn = get_connection()
    cursor = conn.cursor()

    # ----- CLIENTS -----
    clients = [
        ("First Abu Dhabi Bank", "FAB", "Ahmad Al-Mazrouei", "+971 2 610 1111", "ahmad.m@fab.ae"),
        ("Farnek Services", "Farnek", "Hassan Al-Hosani", "+971 2 555 7890", "hassan@farnek.com"),
        ("Khidmah LLC", "Khidmah", "Sara Al-Ketbi", "+971 2 446 2345", "sara.k@khidmah.com"),
        ("MPM Properties", "MPM", "Omar Rashed", "+971 2 633 4567", "omar.r@mpm.ae"),
        ("United Real Estate", "URE", "Fatima Al-Ali", "+971 2 621 8901", "fatima@ure.ae"),
        ("Al Reef Villas", "ARV", "Khalid Al-Mansoori", "+971 2 557 2345", "khalid@alreef.ae"),
        ("Reem Island Tower Mgmt", "RITM", "Noura Al-Shamsi", "+971 2 444 6789", "noura@reemtowers.ae"),
        ("Yas Plaza Hotels", "YPH", "Rashid Al-Dhaheri", "+971 2 496 1234", "rashid@yasplaza.ae"),
    ]
    cursor.executemany(
        "INSERT INTO clients (name, short_name, contact_person, phone, email) VALUES (?,?,?,?,?)",
        clients,
    )

    # ----- BUILDINGS -----
    # (client_index_1based, name, area, equip_count)
    buildings_spec = [
        (1, "FAB HQ Tower", "Al Maryah Island", 24),
        (1, "FAB Al Wahda Branch", "Al Wahda", 8),
        (1, "FAB Khalifa City Branch", "Khalifa City", 6),
        (2, "Farnek HQ", "Musaffah", 18),
        (2, "Staff Accommodation", "ICAD", 12),
        (3, "Tower A", "Al Reem Island", 32),
        (3, "Tower B", "Al Reem Island", 28),
        (3, "Community Center", "Al Reef", 10),
        (4, "Office Complex", "Hamdan Street", 14),
        (4, "Warehouse", "Mussafah", 8),
        (5, "Commercial Tower", "Corniche Road", 22),
        (5, "Residential Block", "Tourist Club", 16),
        (6, "Cluster A - 50 Villas", "Al Reef", 50),
        (6, "Cluster B - 45 Villas", "Al Reef", 45),
        (7, "Reem Heights", "Al Reem Island", 38),
        (7, "Reem Plaza Mall", "Al Reem Island", 26),
        (8, "Hotel Main", "Yas Island", 42),
        (8, "Conference Center", "Yas Island", 20),
    ]

    building_ids = []
    for client_idx, bname, area, _ in buildings_spec:
        cursor.execute(
            "INSERT INTO buildings (client_id, name, area) VALUES (?,?,?)",
            (client_idx, bname, area),
        )
        building_ids.append(cursor.lastrowid)

    # ----- CONTRACTS -----
    # Payment terms: Large clients quarterly, medium semi-annual, small annual
    # Client 1 (FAB) = quarterly, Client 3 (Khidmah) = quarterly
    # Client 2,5,7,8 = semi-annual
    # Client 4,6 = annual
    client_payment_terms = {
        1: "quarterly", 3: "quarterly",
        2: "semi_annual", 5: "semi_annual", 7: "semi_annual", 8: "semi_annual",
        4: "annual", 6: "annual",
    }

    # Annual values proportional to equipment count
    def calc_annual_value(equip_count):
        if equip_count <= 12:
            return random.randint(15, 22) * 1000
        elif equip_count <= 28:
            return random.randint(25, 35) * 1000
        else:
            return random.randint(38, 55) * 1000

    contract_ids = []
    for i, (client_idx, bname, area, equip_count) in enumerate(buildings_spec):
        start = TODAY - timedelta(days=random.randint(200, 300))
        end = start + timedelta(days=365)
        annual_value = calc_annual_value(equip_count)
        payment_terms = client_payment_terms[client_idx]
        cursor.execute(
            """INSERT INTO contracts
               (building_id, start_date, end_date, visits_per_year,
                annual_value, payment_terms, status)
               VALUES (?,?,?,?,?,?,?)""",
            (building_ids[i], start.isoformat(), end.isoformat(), 4,
             annual_value, payment_terms, "active"),
        )
        contract_ids.append(cursor.lastrowid)

    # ----- EQUIPMENT -----
    equipment_types = [
        "Fire Alarm Panel", "Smoke Detector", "Fire Extinguisher DCP",
        "Fire Extinguisher CO2", "Sprinkler System", "Emergency Light",
        "Hose Reel", "Exit Sign", "FM200 System",
    ]

    # Distribution weights (larger buildings get more variety)
    def distribute_equipment(count):
        """Generate a realistic equipment mix for a given count."""
        items = []
        # Always at least 1 fire alarm panel
        items.append("Fire Alarm Panel")
        remaining = count - 1
        # Weighted distribution
        weights = {
            "Smoke Detector": 0.25,
            "Fire Extinguisher DCP": 0.15,
            "Fire Extinguisher CO2": 0.08,
            "Sprinkler System": 0.05,
            "Emergency Light": 0.18,
            "Hose Reel": 0.08,
            "Exit Sign": 0.15,
            "FM200 System": 0.06,
        }
        types_list = list(weights.keys())
        type_weights = list(weights.values())
        for _ in range(remaining):
            chosen = random.choices(types_list, weights=type_weights, k=1)[0]
            items.append(chosen)
        return items

    for i, (_, _, _, equip_count) in enumerate(buildings_spec):
        items = distribute_equipment(equip_count)
        for eq_type in items:
            cursor.execute(
                "INSERT INTO equipment (building_id, type, status) VALUES (?,?,?)",
                (building_ids[i], eq_type, "OK"),
            )

    # ----- INSPECTIONS (6 months of history + status targeting) -----
    #
    # With visits_per_year=4, next inspection due every ~91 days.
    #
    # Target status distribution:
    #   4 buildings OVERDUE (last inspection > 91 days ago, no schedule)
    #   5 buildings DUE WITHIN 14 DAYS (next due within 14 days)
    #   9 buildings COMPLETED RECENTLY (inspected within last 20 days)
    #
    # Building indices (0-based): 0-17
    #   Overdue: indices 1, 4, 9, 11    (FAB Wahda, Farnek Staff, MPM Warehouse, URE Residential)
    #   Due soon: indices 3, 7, 10, 14, 16  (Farnek HQ, Khidmah Community, URE Commercial, Reem Heights, Hotel Main)
    #   Completed: indices 0, 2, 5, 6, 8, 12, 13, 15, 17

    overdue_indices = [1, 4, 9, 11]
    due_soon_indices = [3, 7, 10, 14, 16]
    completed_indices = [0, 2, 5, 6, 8, 12, 13, 15, 17]

    def gen_inspection(building_idx, inspection_date, equip_count):
        """Generate a single inspection record."""
        tech = random.choice(TECHNICIANS)
        items_checked = equip_count
        # 90-100% pass rate
        fail_rate = random.uniform(0, 0.10)
        items_failed = int(equip_count * fail_rate)
        items_passed = items_checked - items_failed
        notes_options = [
            "All systems functioning normally.",
            "Minor issues noted, follow-up recommended.",
            "Equipment in good condition. Batteries replaced on smoke detectors.",
            "Sprinkler pressure tested. All readings within range.",
            "Fire extinguishers serviced. New tags attached.",
            "Emergency lights tested. Two units need bulb replacement.",
            "Exit signs illumination checked. All operational.",
            "Fire alarm panel tested. Zone 3 sensor cleaned.",
            "Full system check completed. No issues found.",
            "Hose reels tested. Water pressure satisfactory.",
        ]
        notes = random.choice(notes_options)
        return (
            building_ids[building_idx],
            inspection_date.isoformat(),
            tech,
            items_checked, items_passed, items_failed,
            notes,
        )

    # Generate 6 months of historical inspections for all buildings
    # Each building gets ~2 historical inspections (quarterly = every 91 days)
    all_inspections = []

    for idx in range(18):
        equip_count = buildings_spec[idx][3]

        if idx in overdue_indices:
            # Last inspection was 95-130 days ago (overdue by 5-35 days)
            days_ago = random.randint(95, 130)
            last_date = TODAY - timedelta(days=days_ago)
            all_inspections.append(gen_inspection(idx, last_date, equip_count))
            # Also add one ~6 months ago
            older = last_date - timedelta(days=random.randint(85, 100))
            all_inspections.append(gen_inspection(idx, older, equip_count))

        elif idx in due_soon_indices:
            # Last inspection was 78-88 days ago (due in 3-13 days)
            days_ago = random.randint(78, 88)
            last_date = TODAY - timedelta(days=days_ago)
            all_inspections.append(gen_inspection(idx, last_date, equip_count))
            # Also add one ~6 months ago
            older = last_date - timedelta(days=random.randint(85, 100))
            all_inspections.append(gen_inspection(idx, older, equip_count))

        else:  # completed recently
            # Last inspection was 1-20 days ago
            days_ago = random.randint(1, 20)
            last_date = TODAY - timedelta(days=days_ago)
            all_inspections.append(gen_inspection(idx, last_date, equip_count))
            # Also add one ~3 months ago
            mid = last_date - timedelta(days=random.randint(85, 100))
            all_inspections.append(gen_inspection(idx, mid, equip_count))
            # And one ~6 months ago
            older = mid - timedelta(days=random.randint(85, 100))
            all_inspections.append(gen_inspection(idx, older, equip_count))

    cursor.executemany(
        """INSERT INTO inspections
           (building_id, inspection_date, technician,
            items_checked, items_passed, items_failed, notes)
           VALUES (?,?,?,?,?,?,?)""",
        all_inspections,
    )

    # ----- COMPLAINTS -----
    complaints = [
        (
            f"TTS-{TODAY.year}-0001", 3, building_ids[5],
            "Fire alarm panel showing fault code E-14 on 3rd floor. Panel beeping intermittently.",
            "high", "open", None, None,
            (TODAY - timedelta(days=2)).isoformat(),
        ),
        (
            f"TTS-{TODAY.year}-0002", 1, building_ids[0],
            "Two emergency lights on parking level B2 not functioning during monthly test.",
            "medium", "assigned", "Suresh Kumar", None,
            (TODAY - timedelta(days=5)).isoformat(),
        ),
        (
            f"TTS-{TODAY.year}-0003", 8, building_ids[16],
            "Kitchen hood suppression system requires inspection after minor grease fire incident.",
            "high", "in_progress", "Mohammed Al-Rashid", None,
            (TODAY - timedelta(days=8)).isoformat(),
        ),
        (
            f"TTS-{TODAY.year}-0004", 6, building_ids[12],
            "Annual fire extinguisher servicing reminder for villas 12-25.",
            "low", "resolved", "Ahmed Mansoor", None,
            (TODAY - timedelta(days=15)).isoformat(),
        ),
        (
            f"TTS-{TODAY.year}-0005", 7, building_ids[14],
            "Sprinkler system pressure gauge reading below normal on floors 15-18.",
            "medium", "open", None, None,
            (TODAY - timedelta(days=3)).isoformat(),
        ),
    ]
    cursor.executemany(
        """INSERT INTO complaints
           (ticket_number, client_id, building_id, message,
            priority, status, assigned_technician, inspection_id, created_at)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        complaints,
    )

    # ----- PAYMENTS (6 months of history, mixed terms) -----
    #
    # Payment schedule per client type:
    #   Quarterly: 4 payments/year, each = annual_value / 4
    #   Semi-annual: 2 payments/year, each = annual_value / 2
    #   Annual: 1 payment/year = annual_value
    #
    # Status distribution:
    #   6 contracts fully paid
    #   5 contracts partially paid (current installments received, next pending)
    #   4 contracts have overdue payments
    #   3 contracts have partial payments (60-80%)

    # Assign payment status categories to buildings
    # Fully paid: 0(FAB HQ), 2(FAB Khalifa), 5(Khidmah A), 6(Khidmah B), 16(Hotel), 17(Conference)
    # Partially paid: 3(Farnek HQ), 10(URE Commercial), 12(Al Reef A), 14(Reem Heights), 15(Reem Mall)
    # Overdue: 1(FAB Wahda), 4(Farnek Staff), 9(MPM Warehouse), 11(URE Residential)
    # Partial amount: 7(Khidmah Community), 8(MPM Office), 13(Al Reef B)

    fully_paid = {0, 2, 5, 6, 16, 17}
    partially_paid = {3, 10, 12, 14, 15}
    overdue_payment = {1, 4, 9, 11}
    partial_amount = {7, 8, 13}

    payment_methods = ["bank_transfer", "cheque", "bank_transfer", "online"]

    def gen_ref(client_short, year, month):
        return f"{client_short}-TRF-{year}-{month:02d}"

    for i, (client_idx, bname, area, equip_count) in enumerate(buildings_spec):
        contract_id = contract_ids[i]
        # Get contract details
        cursor.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
        contract = dict(cursor.fetchone())
        annual_value = contract["annual_value"]
        payment_terms = contract["payment_terms"]
        client_short = clients[client_idx - 1][1]

        if payment_terms == "quarterly":
            installment = annual_value / 4
            # Generate payments going back 6 months
            payment_dates = []
            base = TODAY - timedelta(days=180)
            for q in range(3):  # 3 quarters in 6 months
                pdate = base + timedelta(days=q * 91)
                if pdate <= TODAY:
                    payment_dates.append(pdate)

        elif payment_terms == "semi_annual":
            installment = annual_value / 2
            payment_dates = [
                TODAY - timedelta(days=150),
                TODAY - timedelta(days=30) if i not in overdue_payment else TODAY - timedelta(days=60),
            ]

        else:  # annual
            installment = annual_value
            payment_dates = [TODAY - timedelta(days=120)]

        for j, pdate in enumerate(payment_dates):
            method = random.choice(payment_methods)
            ref = gen_ref(client_short, pdate.year, pdate.month)

            if i in fully_paid:
                cursor.execute(
                    """INSERT INTO payments
                       (contract_id, payment_date, amount, method,
                        reference_number, status)
                       VALUES (?,?,?,?,?,?)""",
                    (contract_id, pdate.isoformat(), installment,
                     method, ref, "received"),
                )

            elif i in partially_paid:
                if j < len(payment_dates) - 1:
                    # Earlier payments received
                    cursor.execute(
                        """INSERT INTO payments
                           (contract_id, payment_date, amount, method,
                            reference_number, status)
                           VALUES (?,?,?,?,?,?)""",
                        (contract_id, pdate.isoformat(), installment,
                         method, ref, "received"),
                    )
                else:
                    # Latest payment pending
                    cursor.execute(
                        """INSERT INTO payments
                           (contract_id, payment_date, amount, method,
                            reference_number, status)
                           VALUES (?,?,?,?,?,?)""",
                        (contract_id, pdate.isoformat(), installment,
                         method, ref, "pending"),
                    )

            elif i in overdue_payment:
                if j < len(payment_dates) - 1:
                    cursor.execute(
                        """INSERT INTO payments
                           (contract_id, payment_date, amount, method,
                            reference_number, status)
                           VALUES (?,?,?,?,?,?)""",
                        (contract_id, pdate.isoformat(), installment,
                         method, ref, "received"),
                    )
                else:
                    # Latest payment overdue
                    cursor.execute(
                        """INSERT INTO payments
                           (contract_id, payment_date, amount, method,
                            reference_number, status)
                           VALUES (?,?,?,?,?,?)""",
                        (contract_id, pdate.isoformat(), installment,
                         method, ref, "overdue"),
                    )

            else:  # partial_amount
                # Pay 60-80% of the first installment
                partial_pct = random.uniform(0.6, 0.8)
                paid_amount = round(installment * partial_pct, 2)
                cursor.execute(
                    """INSERT INTO payments
                       (contract_id, payment_date, amount, method,
                        reference_number, status, notes)
                       VALUES (?,?,?,?,?,?,?)""",
                    (contract_id, pdate.isoformat(), paid_amount,
                     method, ref, "partial",
                     f"Partial payment ({partial_pct:.0%} of AED {installment:,.0f})"),
                )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    from database import init_db, reset_db
    reset_db()
    seed()
    print("Seed data loaded successfully!")

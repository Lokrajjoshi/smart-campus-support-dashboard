"""Create a reproducible, realistic synthetic campus-support dataset."""

from datetime import datetime, timedelta
from pathlib import Path
import random

import pandas as pd


SERVICES = {
    "Wi-Fi / IT": ["Wi-Fi access", "Account login", "Lab computer", "Email", "Software access"],
    "Academic / LMS": ["Course material", "Attendance entry", "Assignment upload", "LMS access"],
    "Library": ["Book renewal", "Digital resource", "Fine query", "Library account"],
    "Hostel": ["Room maintenance", "Water", "Electricity", "Access card"],
    "Transport": ["Bus timing", "Route", "Bus pass", "Vehicle tracking"],
    "Fees": ["Payment status", "Receipt", "Scholarship", "Fee portal"],
    "Classroom Facilities": ["Projector", "Air conditioning", "Furniture", "Audio system"],
    "Administration": ["Certificate", "Letter request", "Record correction", "Approval"],
    "ID Card": ["Lost card", "Damaged card", "Access issue", "New card"],
    "Examination Support": ["Hall ticket", "Exam schedule", "Result query", "Registration"],
}

DEPARTMENT = {
    "Wi-Fi / IT": "IT Services", "Academic / LMS": "Academic Office",
    "Library": "Library Services", "Hostel": "Hostel Office",
    "Transport": "Transport Office", "Fees": "Finance Office",
    "Classroom Facilities": "Campus Facilities", "Administration": "Administration",
    "ID Card": "Security & ID Office", "Examination Support": "Examination Office",
}

DESCRIPTIONS = {
    "Wi-Fi / IT": "Unable to use a required campus technology service.",
    "Academic / LMS": "Academic portal information or access needs support.",
    "Library": "Library service request is blocking study activity.",
    "Hostel": "Hostel facility or access issue requires attention.",
    "Transport": "Campus transport information or pass needs correction.",
    "Fees": "Fee transaction or receipt requires verification.",
    "Classroom Facilities": "A classroom facility is not functioning correctly.",
    "Administration": "An administrative request needs processing or correction.",
    "ID Card": "Student ID card or campus access needs support.",
    "Examination Support": "Examination registration or information needs support.",
}


def generate_cases(count: int = 400, seed: int = 20261120) -> pd.DataFrame:
    random.seed(seed)
    end = datetime(2026, 11, 20, 18, 0)
    rows = []

    for index in range(1, count + 1):
        service = random.choices(list(SERVICES), weights=[18, 15, 9, 8, 7, 9, 8, 9, 7, 10])[0]
        category = random.choice(SERVICES[service])
        priority = random.choices(["Low", "Medium", "High", "Critical"], [22, 48, 24, 6])[0]
        created_at = end - timedelta(hours=random.randint(12, 24 * 150), minutes=random.randint(0, 59))
        status = random.choices(["Open", "In Progress", "Resolved", "Closed"], [8, 12, 55, 25])[0]

        waiting_hours = round(max(0.3, random.lognormvariate(2.1, 0.85)), 1)
        if priority == "Critical":
            waiting_hours = round(waiting_hours * 0.45, 1)

        resolution_hours = None
        resolved_at = None
        if status in {"Resolved", "Closed"}:
            resolution_hours = round(waiting_hours + random.lognormvariate(2.6, 0.8), 1)
            resolved_at = created_at + timedelta(hours=resolution_hours)
            if resolved_at > end:
                resolved_at = end
                resolution_hours = round((resolved_at - created_at).total_seconds() / 3600, 1)

        handoffs = random.choices([0, 1, 2, 3, 4], [45, 31, 15, 7, 2])[0]
        follow_ups = random.choices([0, 1, 2, 3, 4], [47, 29, 15, 7, 2])[0]
        reopened = status in {"Resolved", "Closed"} and random.random() < (0.05 + 0.04 * min(handoffs, 3))

        satisfaction = None
        if status in {"Resolved", "Closed"} and random.random() < 0.84:
            quality = 5 - (waiting_hours > 24) - (handoffs >= 2) - (follow_ups >= 2) - reopened
            satisfaction = max(1, min(5, int(round(random.gauss(quality, 0.8)))))

        rows.append({
            "case_id": f"SCS-{index:04d}",
            "created_at": created_at.isoformat(sep=" ", timespec="minutes"),
            "resolved_at": resolved_at.isoformat(sep=" ", timespec="minutes") if resolved_at else None,
            "service": service,
            "department": DEPARTMENT[service],
            "category": category,
            "priority": priority,
            "status": status,
            "title": f"{category} support needed",
            "description": DESCRIPTIONS[service],
            "waiting_hours": waiting_hours,
            "resolution_hours": resolution_hours,
            "follow_ups": follow_ups,
            "handoffs": handoffs,
            "reopened": reopened,
            "satisfaction": satisfaction,
            "source": "Synthetic baseline",
        })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    output = Path(__file__).parent / "data" / "synthetic_cases.csv"
    output.parent.mkdir(exist_ok=True)
    generate_cases().to_csv(output, index=False)
    print(f"Created {output} with 400 synthetic cases")

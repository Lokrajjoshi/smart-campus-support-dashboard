"""SQLite persistence and validation for campus support cases."""

from datetime import datetime
from pathlib import Path
import sqlite3

import pandas as pd

from data_generator import DEPARTMENT, SERVICES, generate_cases


ROOT = Path(__file__).parent
DB_PATH = ROOT / "data" / "campus_support.db"
CSV_PATH = ROOT / "data" / "synthetic_cases.csv"

COLUMNS = [
    "case_id", "created_at", "resolved_at", "service", "department", "category",
    "priority", "status", "title", "description", "waiting_hours", "resolution_hours",
    "follow_ups", "handoffs", "reopened", "satisfaction", "source",
]


def connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    con.execute("PRAGMA journal_mode=WAL")
    return con


def initialise_database(db_path: Path = DB_PATH) -> None:
    """Create the table and load baseline data only when the table is empty."""
    con = connection(db_path)
    con.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            resolved_at TEXT,
            service TEXT NOT NULL,
            department TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('Low','Medium','High','Critical')),
            status TEXT NOT NULL CHECK(status IN ('Open','In Progress','Resolved','Closed')),
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            waiting_hours REAL NOT NULL CHECK(waiting_hours >= 0),
            resolution_hours REAL,
            follow_ups INTEGER NOT NULL CHECK(follow_ups >= 0),
            handoffs INTEGER NOT NULL CHECK(handoffs >= 0),
            reopened INTEGER NOT NULL CHECK(reopened IN (0,1)),
            satisfaction INTEGER CHECK(satisfaction BETWEEN 1 AND 5),
            source TEXT NOT NULL
        )
    """)
    count = con.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    if count == 0:
        frame = generate_cases()
        frame.to_csv(CSV_PATH, index=False)
        frame.to_sql("cases", con, if_exists="append", index=False)
    con.commit()
    con.close()


def load_cases(db_path: Path = DB_PATH) -> pd.DataFrame:
    initialise_database(db_path)
    con = connection(db_path)
    frame = pd.read_sql_query("SELECT * FROM cases ORDER BY created_at DESC", con)
    con.close()
    frame["reopened"] = frame["reopened"].astype(bool)
    return frame


def add_case(case: dict, db_path: Path = DB_PATH) -> str:
    """Validate and insert one new case; return its generated case ID."""
    required = ["service", "category", "priority", "title", "description"]
    missing = [field for field in required if not str(case.get(field, "")).strip()]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    if case["service"] not in SERVICES:
        raise ValueError("Unknown service")
    if case["category"] not in SERVICES[case["service"]]:
        raise ValueError("Category does not belong to the selected service")
    if case["priority"] not in {"Low", "Medium", "High", "Critical"}:
        raise ValueError("Unknown priority")

    initialise_database(db_path)
    con = connection(db_path)
    number = con.execute("SELECT COALESCE(MAX(CAST(SUBSTR(case_id, 5) AS INTEGER)), 0) + 1 FROM cases").fetchone()[0]
    case_id = f"SCS-{number:04d}"
    row = {
        "case_id": case_id,
        "created_at": datetime.now().isoformat(sep=" ", timespec="minutes"),
        "resolved_at": None,
        "service": case["service"],
        "department": DEPARTMENT[case["service"]],
        "category": case["category"],
        "priority": case["priority"],
        "status": "Open",
        "title": str(case["title"]).strip(),
        "description": str(case["description"]).strip(),
        "waiting_hours": 0.0,
        "resolution_hours": None,
        "follow_ups": 0,
        "handoffs": 0,
        "reopened": 0,
        "satisfaction": None,
        "source": "User submitted in app",
    }
    placeholders = ",".join("?" for _ in COLUMNS)
    con.execute(f"INSERT INTO cases ({','.join(COLUMNS)}) VALUES ({placeholders})", [row[c] for c in COLUMNS])
    con.commit()
    con.close()
    return case_id

import sqlite3

from data_generator import generate_cases
from database import add_case, initialise_database, load_cases


def test_generator_is_reproducible_and_valid():
    first = generate_cases(20)
    second = generate_cases(20)
    assert first.equals(second)
    assert first.case_id.is_unique
    assert set(first.status) <= {"Open", "In Progress", "Resolved", "Closed"}
    unresolved = ~first.status.isin(["Resolved", "Closed"])
    assert first.loc[unresolved, "resolution_hours"].isna().all()
    assert first.loc[unresolved, "satisfaction"].isna().all()


def test_generated_snapshot_respects_ticket_lifecycle():
    frame = generate_cases(400)
    resolved = frame.status.isin(["Resolved", "Closed"])
    assert frame.loc[resolved, "resolved_at"].notna().all()
    assert frame.loc[resolved, "resolution_hours"].notna().all()
    assert (frame.loc[resolved, "resolution_hours"] >= frame.loc[resolved, "waiting_hours"]).all()
    assert not frame.loc[~resolved, "reopened"].any()


def test_new_case_persists(tmp_path):
    path = tmp_path / "test.db"
    initialise_database(path)
    before = len(load_cases(path))
    case_id = add_case({"service": "Library", "category": "Book renewal", "priority": "Medium", "title": "Renewal blocked", "description": "The renewal option is unavailable."}, path)
    after = load_cases(path)
    assert len(after) == before + 1
    saved = after[after.case_id == case_id].iloc[0]
    assert saved.status == "Open" and saved.source == "User submitted in app"


def test_database_rejects_invalid_category(tmp_path):
    path = tmp_path / "test.db"
    try:
        add_case({"service": "Library", "category": "Bus pass", "priority": "Low", "title": "Wrong", "description": "Wrong mapping"}, path)
        assert False, "Expected validation error"
    except ValueError as error:
        assert "does not belong" in str(error)

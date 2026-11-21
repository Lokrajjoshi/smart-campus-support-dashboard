import pandas as pd

from risk import add_risk_columns, score_experience_risk


def base_case(**changes):
    case = {"status": "Closed", "waiting_hours": 2, "resolution_hours": 5,
            "follow_ups": 0, "handoffs": 0, "reopened": False, "satisfaction": 5}
    case.update(changes)
    return case


def test_low_risk_case():
    score, level, _ = score_experience_risk(base_case())
    assert score == 0 and level == "Low"


def test_unresolved_and_missing_satisfaction():
    score, level, reasons = score_experience_risk(base_case(status="Open", satisfaction=None))
    assert score == 25 and level == "Medium"
    assert all("satisfaction" not in reason for reason in reasons)


def test_high_risk_resolved_case_is_explainable():
    score, level, reasons = score_experience_risk(base_case(waiting_hours=60, resolution_hours=100, follow_ups=3, handoffs=3, reopened=True, satisfaction=1))
    assert score == 100 and level == "High"
    assert len(reasons) == 6


def test_dataframe_columns_added():
    result = add_risk_columns(pd.DataFrame([base_case()]))
    assert {"risk_score", "risk_level", "risk_reasons"}.issubset(result.columns)

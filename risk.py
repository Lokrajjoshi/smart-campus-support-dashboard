"""Explainable student-experience risk scoring.

The rule is intentionally transparent and easy to audit. It measures
experience risk, not whether a support team member did a good or bad job.
"""

import pandas as pd


def score_experience_risk(case: dict | pd.Series) -> tuple[int, str, list[str]]:
    """Return (score, level, reasons) for one support case.

    Maximum score is capped at 100. Missing satisfaction is not treated as a
    negative rating; unresolved cases get their own explicit risk points.
    """
    score = 0
    reasons: list[str] = []

    status = str(case.get("status", ""))
    waiting = float(case.get("waiting_hours", 0) or 0)
    resolution = case.get("resolution_hours")
    follow_ups = int(case.get("follow_ups", 0) or 0)
    handoffs = int(case.get("handoffs", 0) or 0)
    reopened = bool(case.get("reopened", False))
    satisfaction = case.get("satisfaction")

    if status not in {"Resolved", "Closed"}:
        score += 25
        reasons.append("case is still unresolved (+25)")

    if waiting > 48:
        score += 20
        reasons.append("waiting time is over 48 hours (+20)")
    elif waiting > 24:
        score += 12
        reasons.append("waiting time is over 24 hours (+12)")
    elif waiting > 8:
        score += 5
        reasons.append("waiting time is over 8 hours (+5)")

    if pd.notna(resolution) and float(resolution) > 72:
        score += 15
        reasons.append("resolution time is over 72 hours (+15)")
    elif pd.notna(resolution) and float(resolution) > 24:
        score += 8
        reasons.append("resolution time is over 24 hours (+8)")

    if handoffs >= 3:
        score += 15
        reasons.append("three or more handoffs (+15)")
    elif handoffs == 2:
        score += 8
        reasons.append("two handoffs (+8)")
    elif handoffs == 1:
        score += 3
        reasons.append("one handoff (+3)")

    if follow_ups >= 3:
        score += 15
        reasons.append("three or more student follow-ups (+15)")
    elif follow_ups == 2:
        score += 9
        reasons.append("two student follow-ups (+9)")
    elif follow_ups == 1:
        score += 4
        reasons.append("one student follow-up (+4)")

    if reopened:
        score += 15
        reasons.append("case was reopened (+15)")

    if pd.notna(satisfaction):
        rating = int(satisfaction)
        if rating <= 2:
            score += 20
            reasons.append("satisfaction is 1-2 out of 5 (+20)")
        elif rating == 3:
            score += 8
            reasons.append("satisfaction is 3 out of 5 (+8)")
    elif status in {"Resolved", "Closed"}:
        reasons.append("satisfaction not submitted (+0)")

    score = min(score, 100)
    level = "Low" if score < 25 else "Medium" if score < 50 else "High"
    if not reasons:
        reasons.append("no experience-risk signals detected")
    return score, level, reasons


def add_risk_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add risk_score, risk_level and risk_reasons to a DataFrame copy."""
    result = df.copy()
    scored = result.apply(score_experience_risk, axis=1)
    result["risk_score"] = [item[0] for item in scored]
    result["risk_level"] = [item[1] for item in scored]
    result["risk_reasons"] = ["; ".join(item[2]) for item in scored]
    return result

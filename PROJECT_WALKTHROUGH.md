# Project Walkthrough

## 30-second introduction

**Smart Campus Support & Student Experience Dashboard** examines a gap that normal support dashboards often miss: a ticket can be marked resolved while the student still has a poor experience. The application analyses waiting time, handoffs, follow-ups, reopened cases and satisfaction, then assigns an explainable experience-risk level. New cases are validated, stored in SQLite and immediately reflected in the dashboard.

## Key design decisions

### Why this problem?

Campus services affect daily student life, but resolution status alone hides delays and repeated effort. The project therefore separates the operational outcome—whether a case closed—from the quality of the student's experience.

### What is distinctive?

A resolved ticket can still have Medium or High experience risk when it took too long, moved between departments, required repeated follow-ups, reopened or received a low satisfaction rating. The score shows its reasons rather than hiding them inside a black-box model.

### What does live updating mean?

It means live response to user actions. A submitted case is validated, written to SQLite and included when Streamlit reruns the KPIs, filters and charts. The project does not claim access to a university live feed.

### Why Streamlit?

Streamlit turns Python data-analysis code into an interactive web application with forms, filters, metrics and charts while keeping the implementation readable.

### Why SQLite?

CSV provides a reproducible baseline, while SQLite provides structured persistence, validation constraints and safe insertion of new cases without requiring an external database server.

## Risk logic

The rule uses transparent points. Unresolved status, long waiting and resolution time, handoffs, follow-ups, reopening and low satisfaction add points. Scores below 25 are Low, 25–49 are Medium and 50 or more are High. The total is capped at 100.

Missing satisfaction adds no points because absence of a survey is not proof of dissatisfaction. An unresolved case independently receives 25 points because its outcome remains uncertain.

## Data quality and privacy

The baseline contains 400 reproducible synthetic campus cases. It is clearly labelled and includes no names, student IDs, emails or phone numbers. Unresolved cases cannot contain resolution time or satisfaction; resolved and closed cases contain resolution details. SQLite constraints and form validation protect service-category and lifecycle consistency.

## Verification summary

Automated tests cover reproducible generation, lifecycle consistency, risk boundaries, missing satisfaction, service-category validation and database persistence. Manual application checks cover all six pages, filtering, empty results and the full case-submission flow. Exact executed evidence is recorded in `TESTING.md`.

## Limitations and future scope

The synthetic baseline demonstrates the analytical method rather than measuring a real university. SQLite on free hosting may also reset when the service restarts. With permission and anonymisation, a future version could use approved service data, track service-level targets and compare student experience before and after process improvements.

## Recall chain

**Status → Wait → Handoffs → Follow-ups → Reopen → Satisfaction → Risk**

This chain explains why resolved does not necessarily mean a good experience.

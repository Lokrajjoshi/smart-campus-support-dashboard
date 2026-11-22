# Test Evidence

Latest verification: 23 November 2026.

## Automated results

Command:

```bash
pytest -q
```

Result: **8 passed**.

The automated suite verifies:

1. the synthetic generator is reproducible;
2. case IDs are unique;
3. only valid case statuses are generated;
4. unresolved cases have no resolution time or satisfaction value;
5. resolved/closed snapshots contain consistent lifecycle fields;
6. reopened flags are not assigned to unresolved snapshots;
7. low-, medium- and high-risk scoring boundaries;
8. missing satisfaction does not become a negative rating;
9. a valid new case persists in SQLite; and
10. an invalid service/category combination is rejected.

## Streamlit application test

The application was run through Streamlit's application-testing framework.

- Exceptions: **0**
- Navigation pages checked: **6**
- Metrics detected: **16** across the app
- Plotly charts detected: **10**
- Data tables detected: **3**

The enhanced interface was also checked for reliable light-mode contrast, sidebar rendering, six labelled navigation pages, chart theming and responsive card layout. Read-only reopened values are displayed as Yes/No text rather than misleading checkbox controls.

The final navigation redesign was checked page by page: Overview, Ticket Explorer, Service Analytics, Experience Analytics, Raise New Case and About & Method all rendered with zero Streamlit exceptions. The pure-CSS Experience Pulse and card-depth effects do not change the analytical logic or database behaviour.

The Ticket Explorer was additionally checked with:

- a Wi-Fi / IT service filter, which returned only Wi-Fi / IT cases;
- a search string that matches no case, which displayed the expected empty-result warning.

Observed clean-baseline metrics:

- Total cases: 400
- Open / in progress: 89
- Resolution rate: 77.8%
- High experience risk: 7
- Poor despite resolved: 12

## Case-submission flow test

The form was filled with a non-identifying demonstration case and submitted through the Streamlit test interface.

- Submission without the privacy confirmation was blocked.
- Submission after privacy confirmation was accepted.

- Before submission: 400 rows
- After submission: 401 rows
- Generated ID: SCS-0401
- Stored status: Open
- Stored source: User submitted in app
- Visible confirmation: `Case SCS-0401 was saved. All KPIs and charts now include it.`
- Streamlit exceptions: 0

The redesigned form was re-tested after the interface upgrade and again persisted the case successfully.

After verification, the temporary test insertion was removed by restoring the clean baseline database. The delivered database contains 400 cases.

## Visual check

The running application was opened in Chromium at 1050 x 1004 and visually checked on:

- Overview
- Experience Analytics
- Raise New Case

The hero, KPI cards, navigation, charts and form were readable without overlap or clipping in the checked viewport. The live local test URL is not a public deployment URL and is therefore not included as a submission link.

## Repository checks

- Python syntax compilation: passed
- `git diff --check`: passed
- Streamlit secrets file: excluded by `.gitignore`
- Private student data in the synthetic baseline: none
- Public deployment test: pending

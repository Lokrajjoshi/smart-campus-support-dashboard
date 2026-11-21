# Smart Campus Support & Student Experience Dashboard

**Register number:** 2647136  
**Course:** MCA Python Programming (MCA411-2), CIA 3  
**Final submission deadline in the supplied brief:** 29 November 2026

## Core question

Why can students have a poor support experience even when their ticket is marked resolved?

**Core message:** Resolution tells us whether the issue was closed; student experience tells us how well it was resolved.

## What the application does

- Shows overview KPIs and the number of poor experiences among resolved cases.
- Provides a searchable and filterable ticket explorer.
- Compares campus services by volume, resolution, speed, satisfaction and risk.
- Analyses waiting, handoffs, follow-ups, reopened cases and satisfaction.
- Gives every case a transparent Low/Medium/High Student Experience Risk score.
- Accepts new cases, validates them, persists them in SQLite and updates the app.

Covered services: Wi-Fi/IT, Academic/LMS, Library, Hostel, Transport, Fees, Classroom Facilities, Administration, ID Card and Examination Support.

## Data ethics and limitations

The baseline is a reproducible **synthetic dataset of 400 campus support cases**. It is not real CHRIST University operational data. It contains no student names, IDs, emails or phone numbers. The application asks users not to enter personal data.

“Real-time” means live updates after a user submits a case: SQLite stores the record and the app reruns so its KPIs, explorer and charts include the new case. The project does **not** claim access to a university live feed.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The database and CSV baseline are created automatically in `data/` on first run. To recreate only the CSV baseline:

```bash
python data_generator.py
```

## Run tests

```bash
pytest -q
```

Tests check reproducible generation, valid status-dependent fields, risk boundaries, missing satisfaction, invalid service/category combinations and real database persistence.

See `TESTING.md` for the verified results and `VIVA_PREPARATION.md` for concise presentation answers.

## Risk rule

The rule is deliberately understandable and defendable:

| Signal | Points |
|---|---:|
| Case is unresolved | +25 |
| Waiting >8 / >24 / >48 hours | +5 / +12 / +20 |
| Resolution >24 / >72 hours | +8 / +15 |
| 1 / 2 / 3+ handoffs | +3 / +8 / +15 |
| 1 / 2 / 3+ follow-ups | +4 / +9 / +15 |
| Reopened | +15 |
| Satisfaction 3 / satisfaction 1-2 | +8 / +20 |

Low = 0-24, Medium = 25-49, High = 50-100. Missing satisfaction adds zero points rather than being treated as a bad rating. An unresolved case receives +25 independently.

## Repository structure

```text
app.py                 Streamlit interface and analytics
database.py            SQLite schema, loading, validation and insertion
data_generator.py      documented reproducible synthetic data generator
risk.py                explainable risk-scoring rule
data/                   generated CSV and persistent SQLite database
tests/                  automated tests
requirements.txt       pinned dependencies
```

## Deployment (after GitHub upload)

1. Push this folder to a GitHub repository.
2. Sign in to Streamlit Community Cloud and select **Create app**.
3. Select the repository, branch and `app.py`.
4. Deploy, test the public URL and only then submit that verified URL.

No GitHub repository or deployed URL is claimed until those actions have actually succeeded.

### Free-hosting persistence note

SQLite persists case submissions while the running app instance retains its filesystem. A free Streamlit Community Cloud app may recreate its filesystem after a restart, so long-term production persistence would require an approved external database. This limitation does not change the demonstrated live insert-and-update flow.

## Research connection

This dashboard is a distinct CIA 3 project. Its rationale is an applied extension of CarePulse research into why technically resolved IT support tickets may still frustrate users.

# Smart Campus Support & Student Experience Dashboard

## Core question

Why can students have a poor support experience even when their ticket is marked resolved?

**Core message:** Resolution tells us whether the issue was closed; student experience tells us how well it was resolved.

## What the application does

- Shows overview KPIs and the number of poor experiences among resolved cases.
- Uses a responsive, student-friendly interface with reliable light-mode contrast.
- Provides live system status, quick service insights and interactive chart tooltips.
- Uses the left sidebar as true six-page navigation instead of decorative content.
- Includes lightweight CSS animation and 3D hover depth with no extra JavaScript framework.
- Provides a searchable and filterable ticket explorer.
- Compares campus services by volume, resolution, speed, satisfaction and risk.
- Analyses waiting, handoffs, follow-ups, reopened cases and satisfaction.
- Gives every case a transparent Low/Medium/High Student Experience Risk score.
- Accepts new cases, validates them, persists them in SQLite and updates the app.
- Shows reopened status as clear Yes/No text so read-only tables are not mistaken for editable forms.

Covered services: Wi-Fi/IT, Academic/LMS, Library, Hostel, Transport, Fees, Classroom Facilities, Administration, ID Card and Examination Support.

## Data ethics and limitations

The baseline is a reproducible **synthetic dataset of 400 campus support cases**. It is not real university operational data. It contains no student names, IDs, emails or phone numbers. The application asks users not to enter personal data.

“Real-time” means live updates after a user submits a case: SQLite stores the record and the app reruns so its KPIs, explorer and charts include the new case. The project does **not** claim access to a university live feed.

Each dataset row is a current ticket snapshot. The allowed lifecycle is `Open → In Progress → Resolved → Closed`; a reopened resolved case returns to active handling before it can be resolved again. The application validates lifecycle-dependent fields: unresolved cases have no resolution time or satisfaction, while resolved/closed cases have resolution details. A full event-history or staff administration system is intentionally outside this dashboard's scope.

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

Tests check reproducible generation, lifecycle-consistent fields, risk boundaries, missing satisfaction, invalid service/category combinations and real database persistence.

See `TESTING.md` for verified results and `PROJECT_WALKTHROUGH.md` for concise technical explanations.

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

This dashboard is a distinct support-experience analytics project. Its rationale is an applied extension of CarePulse research into why technically resolved IT support tickets may still frustrate users.

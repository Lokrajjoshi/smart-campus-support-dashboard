# Concise Viva Preparation

## 30-second introduction

My project is **Smart Campus Support & Student Experience Dashboard**. Normal support dashboards mainly count open and resolved tickets. My project asks a different question: why can a student still have a poor experience when a ticket is marked resolved? It analyses waiting time, handoffs, follow-ups, reopened cases and satisfaction, and gives an explainable experience-risk level. A new case is validated, saved in SQLite and immediately reflected in the dashboard.

## Likely questions and short answers

### Why did you select this topic?

Campus services affect daily student life, but resolution status alone hides delays and repeated effort. The topic is useful, directly related to the university environment and extends my CarePulse research idea without copying it.

### What is innovative here?

The dashboard separates **ticket outcome** from **student experience**. A resolved ticket can still be high risk when it took too long, moved between departments, needed many follow-ups, reopened or received a low rating.

### What does real-time mean in your project?

It means live response to user actions. A submitted case is validated, written to SQLite and included when Streamlit reruns the KPIs, filters and charts. I do not claim a live CHRIST University data feed.

### Why use Streamlit?

It converts Python data-analysis code into an interactive web application with forms, filters, metrics and charts using simple, explainable Python.

### Why use SQLite?

CSV is suitable for the reproducible baseline, while SQLite gives structured persistence, validation constraints and safe insertion of new cases.

### How is risk calculated?

It is a transparent point rule. Unresolved status, long wait and resolution time, handoffs, follow-ups, reopening and low satisfaction add points. Under 25 is Low, 25-49 is Medium and 50 or more is High. The score is capped at 100.

### What happens when satisfaction is missing?

Missing satisfaction adds zero points because absence of a survey is not proof of dissatisfaction. An unresolved case independently gets 25 points because its outcome is uncertain.

### Is the data real?

No. It is a reproducible synthetic dataset of 400 realistic campus cases. It is clearly labelled and contains no names, student IDs, emails or phone numbers.

### How did you ensure data consistency?

The generator allows only valid statuses and fields. Unresolved cases cannot have resolution time or satisfaction. SQLite uses constraints, and the form validates required fields and service-category mappings.

### How did you test it?

Seven automated tests pass. I also ran the Streamlit app with zero exceptions and submitted a case through the form, confirming the database row count changed from 400 to 401 and the success message appeared.

### What is one limitation?

The baseline is synthetic, so the patterns demonstrate the method rather than measuring the actual university. SQLite on free cloud hosting may also reset if the service restarts; a production version would use an approved managed database.

### What is future scope?

With permission and anonymisation, the same design could use real service data, track service-level targets and compare experience before and after process improvements.

## Fixed recall chain

**Status → Wait → Handoffs → Follow-ups → Reopen → Satisfaction → Risk**

Use this chain whenever explaining why resolved does not necessarily mean a good experience.

"""Smart Campus Support & Student Experience Dashboard."""

from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

from data_generator import SERVICES
from database import add_case, load_cases
from risk import add_risk_columns, score_experience_risk


st.set_page_config(page_title="Smart Campus Support", page_icon="🎓", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
  :root {color-scheme: light;}
  .stApp, [data-testid="stAppViewContainer"] {background:linear-gradient(180deg,#eef5ff 0,#f8fafc 420px,#f8fafc 100%);color:#172033;}
  [data-testid="stHeader"] {background:rgba(248,250,252,.92);}
  [data-testid="stSidebar"] {background:linear-gradient(180deg,#0f2454 0%,#173b7a 58%,#0e7490 100%);border-right:0;}
  [data-testid="stSidebar"] * {color:#f8fbff !important;}
  [data-testid="stSidebar"] button {border-color:rgba(255,255,255,.30) !important;}
  .block-container {padding-top:1.45rem;padding-bottom:3rem;max-width:1500px;}
  h1,h2,h3 {letter-spacing:-.025em;color:#172033;} p,label,.stCaption {color:#475569;}
  .hero {position:relative;overflow:hidden;padding:2rem 2.1rem;border-radius:26px;color:white;background:linear-gradient(120deg,#112451 0%,#2456d8 45%,#0891b2 100%);background-size:180% 180%;box-shadow:0 18px 48px rgba(22,57,133,.24);margin-bottom:1.05rem;animation:gradientMove 10s ease infinite;}
  .hero:after {content:"";position:absolute;width:320px;height:320px;border-radius:50%;right:-95px;top:-165px;background:rgba(255,255,255,.12);}
  .hero h1 {color:white;margin:0;font-size:clamp(1.8rem,3vw,2.75rem);line-height:1.08;}.hero p {color:#eaf2ff;margin:.7rem 0 1.05rem;font-size:1rem;}
  .hero-badge {display:inline-block;margin:0 .45rem .25rem 0;padding:.32rem .72rem;border-radius:999px;border:1px solid rgba(255,255,255,.35);background:rgba(255,255,255,.13);color:white;font-size:.78rem;font-weight:700;}
  .hero-grid {display:grid;grid-template-columns:minmax(0,1.5fr) minmax(230px,.55fr);align-items:center;gap:1.4rem;position:relative;z-index:2;}
  .pulse-scene {height:220px;position:relative;display:flex;align-items:center;justify-content:center;perspective:700px;}
  .pulse-core {position:absolute;width:74px;height:74px;border-radius:24px;background:linear-gradient(145deg,#fff,#7dd3fc);box-shadow:0 0 35px rgba(125,211,252,.75),inset 0 0 15px rgba(37,99,235,.28);transform:rotate(45deg);animation:coreFloat 3.4s ease-in-out infinite;}
  .pulse-core:after {content:"CX";position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#173b7a;font-size:1.05rem;font-weight:900;transform:rotate(-45deg);}
  .orbit {position:absolute;border:1.5px solid rgba(255,255,255,.48);border-radius:50%;transform-style:preserve-3d;}
  .orbit.one {width:140px;height:140px;transform:rotateX(67deg) rotateZ(12deg);animation:orbitOne 9s linear infinite;}
  .orbit.two {width:190px;height:190px;transform:rotateX(68deg) rotateZ(72deg);animation:orbitTwo 12s linear infinite reverse;}
  .orbit-dot {position:absolute;width:13px;height:13px;border-radius:50%;background:#fbbf24;box-shadow:0 0 18px #fbbf24;top:19px;left:45px;animation:dotPulse 1.8s ease-in-out infinite;}
  .pulse-label {position:absolute;bottom:3px;color:#e0f2fe;font-size:.73rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;}
  @keyframes gradientMove {0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
  @keyframes coreFloat {0%,100%{transform:rotate(45deg) translateY(0)}50%{transform:rotate(45deg) translate(-7px,7px)}}
  @keyframes orbitOne {to{transform:rotateX(67deg) rotateZ(372deg)}}
  @keyframes orbitTwo {to{transform:rotateX(68deg) rotateZ(432deg)}}
  @keyframes dotPulse {0%,100%{transform:scale(.8);opacity:.65}50%{transform:scale(1.25);opacity:1}}
  .question-grid {display:grid;grid-template-columns:1fr 1fr;gap:.8rem;margin:.4rem 0 1rem;}
  .question-card {background:white;border:1px solid #dce7f5;padding:1rem 1.15rem;border-radius:16px;box-shadow:0 6px 22px rgba(30,64,175,.07);color:#334155;}
  .question-card strong {display:block;color:#173b7a;margin-bottom:.25rem;}.question-card.answer {border-left:5px solid #0ea5a8;}
  .section-heading {margin:1.25rem 0 .7rem;}.section-heading h2 {font-size:1.32rem;margin:0;color:#172033;}.section-heading p {margin:.18rem 0 0;font-size:.9rem;color:#64748b;}
  div[data-testid="stMetric"] {background:white;padding:1rem 1.05rem;border-radius:17px;box-shadow:0 7px 24px rgba(22,54,112,.08);border:1px solid #e0e9f5;min-height:118px;transition:transform .25s ease,box-shadow .25s ease;transform-style:preserve-3d;}
  div[data-testid="stMetric"]:hover {transform:perspective(700px) translateY(-5px) rotateX(2deg) rotateY(-2deg);box-shadow:0 16px 34px rgba(22,54,112,.15);}
  div[data-testid="stMetric"] label,div[data-testid="stMetric"] [data-testid="stMetricLabel"] * {color:#64748b !important;font-weight:700 !important;}
  div[data-testid="stMetric"] [data-testid="stMetricValue"] * {color:#172033 !important;} div[data-testid="stMetricDelta"] * {color:#0f766e !important;}
  .mini-card {height:100%;background:white;border:1px solid #e0e9f5;border-radius:17px;padding:1rem 1.05rem;box-shadow:0 7px 24px rgba(22,54,112,.07);}
  .mini-card .icon {font-size:1.35rem}.mini-card .label {font-size:.78rem;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.04em}.mini-card .value {font-size:1.08rem;color:#172033;font-weight:800;margin-top:.25rem}.mini-card .note {font-size:.78rem;color:#64748b;margin-top:.18rem}
  .risk-card {background:white;border:1px solid #e0e9f5;border-radius:18px;padding:1.1rem 1.2rem;box-shadow:0 7px 24px rgba(22,54,112,.07)}.risk-low {border-left:6px solid #22c55e}.risk-medium {border-left:6px solid #f59e0b}.risk-high {border-left:6px solid #ef4444}
  .step-card {background:#eff6ff;border:1px solid #bfdbfe;border-radius:16px;padding:1rem 1.1rem;color:#1e3a5f;margin-bottom:.6rem}.step-number {display:inline-flex;align-items:center;justify-content:center;width:25px;height:25px;border-radius:50%;background:#2563eb;color:white;font-weight:800;margin-right:.45rem}
  [data-testid="stSidebar"] [role="radiogroup"] {gap:.38rem;}
  [data-testid="stSidebar"] [role="radiogroup"] label {background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.10);border-radius:12px;padding:.58rem .65rem;transition:.2s;}
  [data-testid="stSidebar"] [role="radiogroup"] label:hover {background:rgba(255,255,255,.16);transform:translateX(4px);}
  [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {background:linear-gradient(90deg,rgba(59,130,246,.55),rgba(14,165,233,.28));border-color:rgba(255,255,255,.36);box-shadow:0 7px 20px rgba(0,0,0,.14);}
  [data-testid="stSidebar"] .stButton button {background:rgba(255,255,255,.13) !important;color:white !important;border:1px solid rgba(255,255,255,.28) !important;}
  [data-testid="stSidebar"] .stButton button:hover {background:rgba(255,255,255,.23) !important;transform:translateY(-1px);}
  [data-testid="stDataFrame"],[data-testid="stPlotlyChart"] {background:white;border-radius:18px;border:1px solid #e0e9f5;box-shadow:0 7px 24px rgba(22,54,112,.07);overflow:hidden}
  [data-testid="stForm"] {background:white;border:1px solid #dce7f5;border-radius:20px;padding:1.25rem;box-shadow:0 8px 28px rgba(22,54,112,.08)}
  [data-baseweb="input"]>div,[data-baseweb="select"]>div,textarea {background:white !important;color:#172033 !important} input,textarea {color:#172033 !important;-webkit-text-fill-color:#172033 !important}
  [data-testid="stExpander"] {background:white;border-radius:15px;border:1px solid #e0e9f5}.stAlert {border-radius:15px} footer {visibility:hidden}
  @media(max-width:900px){.question-grid,.hero-grid{grid-template-columns:1fr}.pulse-scene{height:150px}.hero{padding:1.4rem}.block-container{padding-left:1rem;padding-right:1rem}}
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3)
def get_data() -> pd.DataFrame:
    return add_risk_columns(load_cases())


def section_heading(icon: str, title: str, subtitle: str) -> None:
    st.markdown(f"<div class='section-heading'><h2>{icon} {title}</h2><p>{subtitle}</p></div>", unsafe_allow_html=True)


def table_for_display(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a table copy with clear text instead of read-only checkboxes."""
    display = frame.copy()
    if "reopened" in display.columns:
        display["reopened"] = display["reopened"].map({True: "Yes", False: "No"})
    return display


def polish_chart(figure, height: int = 390):
    """Give every Plotly chart the same clear light theme."""
    figure.update_layout(template="plotly_white", height=height, margin=dict(l=25,r=25,t=65,b=30), paper_bgcolor="#ffffff", plot_bgcolor="#ffffff", font=dict(color="#334155",family="Arial"), title_font=dict(color="#172033",size=17), legend_title_text="", hoverlabel=dict(bgcolor="white",font_color="#172033"))
    figure.update_xaxes(gridcolor="#edf2f7",zerolinecolor="#edf2f7")
    figure.update_yaxes(gridcolor="#edf2f7",zerolinecolor="#edf2f7")
    return figure


def filter_cases(frame: pd.DataFrame, key: str) -> pd.DataFrame:
    with st.expander("🔎 Search and filter cases", expanded=True):
        a,b,c = st.columns(3)
        services = a.multiselect("Campus service", sorted(frame.service.unique()), key=f"{key}_service")
        statuses = b.multiselect("Current status", sorted(frame.status.unique()), key=f"{key}_status")
        risks = c.multiselect("Experience risk", ["Low","Medium","High"], key=f"{key}_risk")
        search = st.text_input("Search by case ID, title, category or description", placeholder="Example: Wi-Fi, SCS-0042, hall ticket...", key=f"{key}_search")
    result = frame.copy()
    if services: result = result[result.service.isin(services)]
    if statuses: result = result[result.status.isin(statuses)]
    if risks: result = result[result.risk_level.isin(risks)]
    if search:
        combined = result[["case_id","title","category","description"]].fillna("").agg(" ".join,axis=1)
        result = result[combined.str.contains(search,case=False,regex=False)]
    return result


df = get_data()
resolved_mask = df.status.isin(["Resolved","Closed"])
poor_resolved = df[resolved_mask & ((df.satisfaction <= 2) | (df.risk_level == "High"))]

with st.sidebar:
    st.markdown("## 🎓 Campus Support")
    st.caption("Student Experience Intelligence")
    st.markdown("---")
    st.markdown("### Navigate")
    page = st.radio(
        "Dashboard navigation",
        [
            "🏠 Overview",
            "🔎 Ticket Explorer",
            "🏢 Service Analytics",
            "💙 Experience Analytics",
            "➕ Raise New Case",
            "ℹ️ About & Method",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("### Dataset status")
    st.write(f"**{len(df):,}** cases loaded")
    st.write(f"**{df.service.nunique()}** campus services")
    st.write(f"Last refreshed **{datetime.now().strftime('%d %b %Y, %I:%M %p')}**")
    if st.button("↻ Refresh dashboard", width="stretch"):
        get_data.clear()
        st.rerun()
    st.markdown("---")
    st.markdown("### Risk legend")
    st.markdown("🟢 **Low:** 0–24 points")
    st.markdown("🟠 **Medium:** 25–49 points")
    st.markdown("🔴 **High:** 50–100 points")
    st.markdown("---")
    st.caption("Synthetic demonstration data — not CHRIST University operational data.")

st.markdown("""
<div class="hero"><div class="hero-grid">
  <div>
    <span class="hero-badge">LIVE USER-ACTION UPDATES</span><span class="hero-badge">PRIVACY-AWARE</span><span class="hero-badge">EXPLAINABLE RISK</span>
    <h1>Smart Campus Support &<br>Student Experience Dashboard</h1>
    <p>See beyond ticket closure and understand how students actually experienced campus support.</p>
    <span class="hero-badge">2647136</span><span class="hero-badge">MCA Python Programming CIA 3</span>
  </div>
  <div class="pulse-scene" aria-label="Animated student experience pulse">
    <div class="orbit one"><span class="orbit-dot"></span></div><div class="orbit two"></div><div class="pulse-core"></div><div class="pulse-label">Experience Pulse</div>
  </div>
</div>
</div>
<div class="question-grid">
  <div class="question-card"><strong>❓ Core question</strong>Why can students have a poor support experience even when their ticket is marked resolved?</div>
  <div class="question-card answer"><strong>💡 Central insight</strong>Resolution tells us whether the issue was closed; student experience tells us how well it was resolved.</div>
</div>
""", unsafe_allow_html=True)

if "created_case" in st.session_state:
    st.success(f"✅ Case {st.session_state.pop('created_case')} was saved. All KPIs and charts now include it.")

if page == "🏠 Overview":
    section_heading(
        "📊",
        "Campus support at a glance",
        "Live summary of the current case dataset",
    )
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total cases", f"{len(df):,}", "Live dataset")
    k2.metric("Open / in progress", int((~resolved_mask).sum()), "Needs attention")
    k3.metric("Resolution rate", f"{resolved_mask.mean():.1%}", "Resolved + closed")
    k4.metric(
        "High experience risk",
        int((df.risk_level == "High").sum()),
        "Priority review",
    )
    k5.metric("Poor despite resolved", len(poor_resolved), "Hidden experience gap")

    busiest = df.service.value_counts().idxmax()
    slowest = df.groupby("service").resolution_hours.median().idxmax()
    highest_risk_service = df.groupby("service").risk_score.mean().idxmax()
    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "🔥", "Busiest service", busiest, f"{int((df.service == busiest).sum())} cases"),
        (c2, "⏱️", "Slowest median resolution", slowest, f"{df[df.service == slowest].resolution_hours.median():.1f} hours"),
        (c3, "⚠️", "Highest average risk", highest_risk_service, f"{df[df.service == highest_risk_service].risk_score.mean():.1f} points"),
        (c4, "⭐", "Average satisfaction", f"{df.satisfaction.mean():.2f} / 5", "Rated resolved cases"),
    ]
    for col, icon, label, value, note in cards:
        col.markdown(
            f"<div class='mini-card'><div class='icon'>{icon}</div>"
            f"<div class='label'>{label}</div><div class='value'>{value}</div>"
            f"<div class='note'>{note}</div></div>",
            unsafe_allow_html=True,
        )

    section_heading("📈", "Trends and risk mix", "Hover over charts to inspect exact values")
    left, right = st.columns([1.35, 1])
    monthly = (
        df.assign(month=pd.to_datetime(df.created_at).dt.to_period("M").astype(str))
        .groupby(["month", "status"])
        .size()
        .reset_index(name="cases")
    )
    trend = px.area(
        monthly,
        x="month",
        y="cases",
        color="status",
        markers=True,
        title="Cases over time by current status",
        color_discrete_map={
            "Closed": "#0f766e",
            "Resolved": "#2563eb",
            "In Progress": "#f59e0b",
            "Open": "#ef4444",
        },
    )
    left.plotly_chart(polish_chart(trend), width="stretch")
    risk_counts = (
        df.risk_level.value_counts()
        .reindex(["Low", "Medium", "High"], fill_value=0)
        .reset_index()
    )
    donut = px.pie(
        risk_counts,
        names="risk_level",
        values="count",
        hole=0.63,
        title="Student experience risk distribution",
        color="risk_level",
        color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"},
    )
    donut.update_traces(textposition="inside", textinfo="percent+label")
    right.plotly_chart(polish_chart(donut), width="stretch")

    p1, p2 = st.columns(2)
    priority_counts = (
        df.priority.value_counts()
        .reindex(["Low", "Medium", "High", "Critical"], fill_value=0)
        .reset_index()
    )
    priority_chart = px.bar(
        priority_counts,
        x="priority",
        y="count",
        color="priority",
        title="Case load by priority",
        color_discrete_map={
            "Low": "#60a5fa",
            "Medium": "#fbbf24",
            "High": "#fb7185",
            "Critical": "#b91c1c",
        },
    )
    priority_chart.update_layout(showlegend=False)
    p1.plotly_chart(polish_chart(priority_chart, 330), width="stretch")
    service_risk = df.groupby("service").risk_score.mean().sort_values().reset_index()
    risk_bar = px.bar(
        service_risk,
        x="risk_score",
        y="service",
        orientation="h",
        title="Average experience risk by service",
        color="risk_score",
        color_continuous_scale=["#bfdbfe", "#f59e0b", "#ef4444"],
    )
    risk_bar.update_coloraxes(showscale=False)
    p2.plotly_chart(polish_chart(risk_bar, 330), width="stretch")

    section_heading(
        "🚩",
        "Resolved, but still a poor experience",
        "Cases where operational closure hides student frustration",
    )
    poor_columns = [
        "case_id",
        "service",
        "status",
        "waiting_hours",
        "handoffs",
        "follow_ups",
        "reopened",
        "satisfaction",
        "risk_level",
        "risk_reasons",
    ]
    poor_display = table_for_display(poor_resolved[poor_columns].head(12))
    st.dataframe(
        poor_display,
        width="stretch",
        hide_index=True,
        column_config={
            "case_id": "Case ID",
            "waiting_hours": st.column_config.NumberColumn("Wait (h)", format="%.1f"),
            "reopened": "Reopened?",
            "satisfaction": st.column_config.NumberColumn("Rating", format="%d ⭐"),
            "risk_level": "Risk",
        },
    )

elif page == "🔎 Ticket Explorer":
    section_heading(
        "🔎",
        "Ticket Explorer",
        "Search, filter and understand individual campus support cases",
    )
    shown = filter_cases(df, "explorer")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Matching cases", len(shown))
    m2.metric(
        "Unresolved",
        int((~shown.status.isin(["Resolved", "Closed"])).sum()),
    )
    m3.metric("High risk", int((shown.risk_level == "High").sum()))
    m4.metric("Reopened", int(shown.reopened.sum()))
    columns = [
        "case_id",
        "created_at",
        "service",
        "category",
        "priority",
        "status",
        "waiting_hours",
        "resolution_hours",
        "follow_ups",
        "handoffs",
        "reopened",
        "satisfaction",
        "risk_score",
        "risk_level",
    ]
    st.dataframe(
        table_for_display(shown[columns]),
        width="stretch",
        hide_index=True,
        column_config={
            "case_id": "Case ID",
            "created_at": "Created",
            "waiting_hours": st.column_config.NumberColumn("Wait (h)", format="%.1f"),
            "resolution_hours": st.column_config.NumberColumn("Resolution (h)", format="%.1f"),
            "reopened": "Reopened?",
            "risk_score": st.column_config.ProgressColumn(
                "Risk score", min_value=0, max_value=100, format="%d"
            ),
        },
    )
    options = shown.case_id.tolist()
    if options:
        section_heading(
            "🧭", "Explain one case", "Every risk level is supported by visible reasons"
        )
        selected = st.selectbox("Select a case ID", options)
        row = shown[shown.case_id == selected].iloc[0]
        score, level, reasons = score_experience_risk(row)
        st.markdown(
            f"<div class='risk-card risk-{level.lower()}'>"
            f"<b>{selected} · {row.title}</b><br>"
            f"<span style='font-size:1.35rem;font-weight:800;color:#172033'>"
            f"{level} risk — {score}/100</span><br>"
            f"<span style='color:#64748b'>{' • '.join(reasons)}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.warning("No cases match those filters. Remove one or more filters to continue.")

elif page == "🏢 Service Analytics":
    section_heading(
        "🏢",
        "Service performance",
        "Compare demand, speed, satisfaction and experience risk across campus services",
    )
    by_service = (
        df.groupby("service")
        .agg(
            cases=("case_id", "count"),
            resolution_rate=(
                "status",
                lambda status: status.isin(["Resolved", "Closed"]).mean(),
            ),
            median_resolution_hours=("resolution_hours", "median"),
            average_satisfaction=("satisfaction", "mean"),
            average_risk=("risk_score", "mean"),
            high_risk_cases=("risk_level", lambda risk: (risk == "High").sum()),
        )
        .reset_index()
    )
    top = by_service.sort_values("cases", ascending=False).iloc[0]
    best = by_service.sort_values("average_satisfaction", ascending=False).iloc[0]
    fastest = by_service.sort_values("median_resolution_hours").iloc[0]

    s1, s2, s3 = st.columns(3)
    s1.metric("Highest demand", top.service, f"{int(top.cases)} cases")
    s2.metric("Highest satisfaction", best.service, f"{best.average_satisfaction:.2f} / 5")
    s3.metric(
        "Fastest median resolution",
        fastest.service,
        f"{fastest.median_resolution_hours:.1f} hours",
    )

    c1, c2 = st.columns(2)
    demand = px.bar(
        by_service.sort_values("cases"),
        x="cases",
        y="service",
        orientation="h",
        title="Demand by campus service",
        color="cases",
        color_continuous_scale=["#bfdbfe", "#2563eb"],
    )
    demand.update_coloraxes(showscale=False)
    c1.plotly_chart(polish_chart(demand), width="stretch")
    comparison = px.scatter(
        by_service,
        x="median_resolution_hours",
        y="average_satisfaction",
        size="cases",
        color="average_risk",
        hover_name="service",
        title="Speed, satisfaction and risk",
        color_continuous_scale=["#22c55e", "#f59e0b", "#ef4444"],
        labels={
            "median_resolution_hours": "Median resolution hours",
            "average_satisfaction": "Average satisfaction",
        },
    )
    c2.plotly_chart(polish_chart(comparison), width="stretch")
    st.dataframe(
        by_service.style.format(
            {
                "resolution_rate": "{:.1%}",
                "median_resolution_hours": "{:.1f}",
                "average_satisfaction": "{:.2f}",
                "average_risk": "{:.1f}",
            }
        ),
        width="stretch",
        hide_index=True,
    )

elif page == "💙 Experience Analytics":
    section_heading(
        "💙",
        "Student experience signals",
        "Measure the effort and friction hidden behind ticket status",
    )
    resolved = df[resolved_mask].copy()
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Median waiting", f"{df.waiting_hours.median():.1f} h", "Before support starts")
    e2.metric("Cases with handoffs", f"{(df.handoffs > 0).mean():.1%}", "Moved between teams")
    e3.metric("Cases with follow-ups", f"{(df.follow_ups > 0).mean():.1%}", "Student chased progress")
    e4.metric("Reopened resolved cases", f"{resolved.reopened.mean():.1%}", "Issue returned")

    c1, c2 = st.columns(2)
    wait_risk = px.box(
        df,
        x="risk_level",
        y="waiting_hours",
        color="risk_level",
        category_orders={"risk_level": ["Low", "Medium", "High"]},
        log_y=True,
        title="Waiting time grows with experience risk",
        color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"},
        labels={
            "risk_level": "Experience risk",
            "waiting_hours": "Waiting hours (log scale)",
        },
    )
    c1.plotly_chart(polish_chart(wait_risk), width="stretch")
    rated_resolved = resolved.dropna(subset=["satisfaction"])
    satisfaction = px.histogram(
        rated_resolved,
        x="satisfaction",
        color="reopened",
        barmode="group",
        nbins=5,
        title="Satisfaction: reopened vs not reopened",
        color_discrete_map={False: "#2563eb", True: "#ef4444"},
        labels={"satisfaction": "Satisfaction (1–5)", "count": "Cases"},
    )
    c2.plotly_chart(polish_chart(satisfaction), width="stretch")

    c3, c4 = st.columns(2)
    effort = df.assign(student_effort=df.follow_ups + df.handoffs)
    effort_chart = px.scatter(
        effort,
        x="student_effort",
        y="risk_score",
        color="risk_level",
        size="waiting_hours",
        hover_data=["case_id", "service", "status"],
        title="More effort usually means higher risk",
        color_discrete_map={"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"},
        labels={"student_effort": "Handoffs + follow-ups", "risk_score": "Risk score"},
    )
    c3.plotly_chart(polish_chart(effort_chart, 360), width="stretch")
    friction = pd.DataFrame(
        {
            "Signal": ["Long wait (>24h)", "Any handoff", "Any follow-up", "Reopened"],
            "Cases": [
                (df.waiting_hours > 24).sum(),
                (df.handoffs > 0).sum(),
                (df.follow_ups > 0).sum(),
                df.reopened.sum(),
            ],
        }
    )
    friction_chart = px.bar(
        friction,
        x="Cases",
        y="Signal",
        orientation="h",
        title="Most common experience-friction signals",
        color="Cases",
        color_continuous_scale=["#bfdbfe", "#1d4ed8"],
    )
    friction_chart.update_coloraxes(showscale=False)
    c4.plotly_chart(polish_chart(friction_chart, 360), width="stretch")
    st.info("💡 Missing satisfaction adds no negative points. An unresolved case independently receives +25 because its outcome is still uncertain.")

elif page == "➕ Raise New Case":
    section_heading(
        "➕",
        "Raise a new campus support case",
        "Submit a demonstration case and watch the dashboard update immediately",
    )
    form_col, guide_col = st.columns([1.45, 0.75])
    with guide_col:
        st.markdown("### How it works")
        st.markdown("<div class='step-card'><span class='step-number'>1</span><b>Choose the service</b><br>Select the campus team that should handle the issue.</div>",unsafe_allow_html=True)
        st.markdown("<div class='step-card'><span class='step-number'>2</span><b>Describe the problem</b><br>Give a short, clear description without private information.</div>",unsafe_allow_html=True)
        st.markdown("<div class='step-card'><span class='step-number'>3</span><b>Live dashboard update</b><br>SQLite stores the case and all metrics refresh.</div>",unsafe_allow_html=True)
        st.warning("🔒 Do not enter names, student IDs, email addresses or phone numbers.")
    with form_col:
        service = st.selectbox(
            "Campus service *",
            list(SERVICES),
            help="Select the service responsible for the issue",
        )
        with st.form("new_case", clear_on_submit=True):
            category = st.selectbox("Issue category *", SERVICES[service])
            priority = st.select_slider(
                "Priority *",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium",
            )
            title = st.text_input(
                "Short title *",
                max_chars=100,
                placeholder="Example: Wi-Fi disconnecting in computer lab",
            )
            description = st.text_area(
                "Describe the issue *",
                max_chars=600,
                height=150,
                placeholder="Explain what happened, where it happened and how it affected you...",
            )
            consent = st.checkbox("I confirm that I have not entered private student data")
            submitted = st.form_submit_button(
                "Submit support case →", type="primary", width="stretch"
            )
        if submitted:
            if not consent:
                st.error("Please confirm the privacy statement before submitting.")
            else:
                try:
                    new_id = add_case(
                        {
                            "service": service,
                            "category": category,
                            "priority": priority,
                            "title": title,
                            "description": description,
                        }
                    )
                    get_data.clear()
                    st.session_state["created_case"] = new_id
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))

elif page == "ℹ️ About & Method":
    section_heading(
        "ℹ️", "About the project", "Method, data ethics and explainable decision logic"
    )
    a1, a2, a3 = st.columns(3)
    a1.markdown(
        "<div class='mini-card'><div class='icon'>🎯</div>"
        "<div class='label'>Purpose</div><div class='value'>Look beyond closure</div>"
        "<div class='note'>Measure how well support was experienced, not only whether it ended.</div></div>",
        unsafe_allow_html=True,
    )
    a2.markdown(
        "<div class='mini-card'><div class='icon'>⚡</div>"
        "<div class='label'>Real-time meaning</div>"
        "<div class='value'>Live user-action updates</div>"
        "<div class='note'>Form submissions persist in SQLite and immediately refresh analysis.</div></div>",
        unsafe_allow_html=True,
    )
    a3.markdown(
        "<div class='mini-card'><div class='icon'>🛡️</div>"
        "<div class='label'>Data ethics</div><div class='value'>Synthetic and private</div>"
        "<div class='note'>400 reproducible cases with no personal student information.</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("### Experience-risk rule")
    r1, r2, r3 = st.columns(3)
    r1.success("🟢 **Low risk: 0–24**\n\nFew or no experience-friction signals")
    r2.warning("🟠 **Medium risk: 25–49**\n\nSome delay, effort or uncertainty")
    r3.error("🔴 **High risk: 50–100**\n\nMultiple serious experience problems")
    with st.expander("View the complete scoring rule", expanded=True):
        st.code(
            "Unresolved +25 | wait >8/+5, >24/+12, >48/+20 | resolution >24/+8, >72/+15\n"
            "Handoffs 1/+3, 2/+8, 3+/+15 | follow-ups 1/+4, 2/+9, 3+/+15\n"
            "Reopened +15 | satisfaction 3/+8, 1–2/+20 | Low <25, Medium 25–49, High 50+",
            language="text",
        )
    with st.expander("Research connection"):
        st.write("This CIA application is an applied extension of the CarePulse research rationale about why technically resolved support tickets may still frustrate users. It remains a distinct MCA Python project.")
    with st.expander("Important limitation"):
        st.write("The baseline is synthetic and demonstrates the analytical method; it does not measure actual CHRIST University performance. A production system would require approved, anonymised university data and durable managed storage.")


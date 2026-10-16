import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

# Page setup
st.set_page_config(
    page_title="CareFlow Analytics",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 CareFlow Healthcare Analytics")
st.caption("Patient pathways, waiting times and workflow bottlenecks")
st.info("This dashboard uses synthetic data, not real hospital records.")

# Data folder
DATA_DIR = Path(__file__).parent / "Data"


def load_csv(filename):
    path = DATA_DIR / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()
events = load_csv("synthetic_event_log.csv")
elapsed = load_csv("patient_elapsed_times.csv")
waiting = load_csv("waiting_time_summary.csv")
bottlenecks = load_csv("bottleneck_summary.csv")

# Overview
st.header("📊 Project Overview")
if events.empty:
    st.warning("Patient event data is missing or empty.")
else:
    patient_cases = events["case_id"].nunique()
    total_events = len(events)
    unique_activities = events["activity"].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Patient Cases", patient_cases)
    col2.metric("Total Events", total_events)
    col3.metric("Unique Activities", unique_activities)
    
    case_col = next(
        (c for c in ["case_id", "patient_id", "case"]
         if c in events.columns),
        None
    )
    activity_col = next(
        (c for c in ["activity", "Activity", "event"]
         if c in events.columns),
        None
    )

    cases = events[case_col].nunique() if case_col else 0
    event_count = len(events)
    activities = (
        events[activity_col].nunique()
        if activity_col else 0
    )

    a, b, c = st.columns(3)
    a.metric("Patient Cases", f"{cases:,}")
    b.metric("Total Events", f"{event_count:,}")
    c.metric("Unique Activities", f"{activities:,}")

    if activity_col:
        st.subheader("Patient Activity Frequency")
        activity_counts = (
            events[activity_col]
            .value_counts()
            .rename_axis("Activity")
            .reset_index(name="Event Count")
        )

        fig = px.bar(
            activity_counts,
            x="Activity",
            y="Event Count",
            title="Number of Events per Activity",
            text="Event Count"
        )
        st.plotly_chart(fig, width="stretch")

# Waiting-time analysis
st.header("⏱️ Waiting-Time Analysis")

if waiting.empty:
    st.warning("Waiting-time CSV is missing or empty.")
else:
    st.write("Waiting-time data preview")
    st.dataframe(waiting, width="stretch")

    # Interactive activity filter
    if "activity" in waiting.columns:
        activities = ["All Activities"] + sorted(
            waiting["activity"].dropna().unique().tolist()
        )

        selected_activity = st.selectbox(
            "Filter by Patient Activity",
            activities
        )

        if selected_activity == "All Activities":
            filtered_waiting = waiting
        else:
            filtered_waiting = waiting[
                waiting["activity"] == selected_activity
            ]

        if not waiting.empty:
         st.subheader("Waiting-Time Summary")

    numeric_cols = waiting.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_cols:
        selected_metric = st.selectbox(
            "Select waiting-time metric",
            numeric_cols,
            key="waiting_summary_metric"
        )

        average_wait = waiting[selected_metric].mean()
        maximum_wait = waiting[selected_metric].max()

        col1, col2 = st.columns(2)

        col1.metric(
            "Average " + selected_metric,
            f"{average_wait:.2f}"
        )

        col2.metric(
            "Maximum " + selected_metric,
            f"{maximum_wait:.2f}"
        )

# Bottleneck analysis
st.header("🚦 Workflow Bottlenecks")

if bottlenecks.empty:
    st.warning("Bottleneck summary CSV is missing or empty.")
else:
    st.dataframe(bottlenecks, width="stretch")

    numeric_cols = bottlenecks.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_cols:
        metric = st.selectbox(
            "Bottleneck metric",
            numeric_cols,
            key="bottleneck_metric"
        )

        fig = px.bar(
            bottlenecks,
            x=bottlenecks.columns[0],
            y=metric,
            title=f"Bottleneck Analysis: {metric}",
            color=metric
        )
        st.plotly_chart(fig, width="stretch")

# Elapsed time data
with st.expander("Patient Elapsed-Time Data"):
    if elapsed.empty:
        st.warning("Elapsed-time CSV is missing or empty.")
    else:
        st.dataframe(elapsed, width="stretch")

st.success("CareFlow dashboard loaded.")
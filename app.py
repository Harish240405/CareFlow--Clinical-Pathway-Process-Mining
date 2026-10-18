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

# Load Week 2 analysis data
# Load Week 2 analysis data
events = load_csv("synthetic_event_log.csv")
elapsed = load_csv("pathway_journey_summary.csv")
transitions = load_csv("pathway_transition_summary.csv")
waiting = load_csv("waiting_time_summary.csv")
bottlenecks = load_csv("bottleneck_summary.csv")

# Patient journey duration insights
if not elapsed.empty:
    duration_col = next(
        (
            col for col in [
                "elapsed_minutes",
                "total_minutes",
                "duration_minutes",
                "elapsed_time_minutes"
            ]
            if col in elapsed.columns
        ),
        None
    )

    if duration_col:
        durations = pd.to_numeric(
            elapsed[duration_col],
            errors="coerce"
        ).dropna()

        if not durations.empty:
            st.header("Patient Journey Duration")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Average Journey",
                f"{durations.mean():.1f} minutes"
            )

            col2.metric(
                "Longest Journey",
                f"{durations.max():.1f} minutes"
            )

            col3.metric(
                "Shortest Journey",
                f"{durations.min():.1f} minutes"
            )
    else:
        st.info(
            "Journey duration column not found. "
            "We will match it to your CSV columns next."
        )

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

    
    activity_col = next(
       (c for c in ["activity", "Activity", "event"]
         if c in events.columns),
        None
    )

# Top 5 longest waiting-time transitions
st.subheader("Top 5 Longest Waiting-Time Transitions")

if transitions.empty:
    st.warning("Transition data is empty.")
else:
    required_cols = {
        "previous_activity",
        "next_activity",
        "average_minutes"
    }

    if required_cols.issubset(transitions.columns):
        top_waiting = (
            transitions.sort_values(
                "average_minutes",
                ascending=False
            )
            .head(5)
            .copy()
        )

        top_waiting["Transition"] = (
            top_waiting["previous_activity"].fillna("Unknown").astype(str)
            + " → "
            + top_waiting["next_activity"].fillna("Unknown").astype(str)
        )

        fig = px.bar(
            top_waiting,
            x="average_minutes",
            y="Transition",
            orientation="h",
            text="average_minutes",
            title="Top 5 Transitions by Average Waiting Time",
            labels={
                "average_minutes": "Average Time (minutes)",
                "Transition": "Activity Transition"
            }
        )

        fig.update_traces(
            texttemplate="%{text:.1f} min",
            textposition="outside"
        )
        fig.update_layout(
            yaxis={"categoryorder": "total ascending"}
        )

        st.plotly_chart(fig, width="stretch")
    else:
        st.warning("Required transition columns are missing.")

    

# Waiting-time analysis
st.header("⏱️ Waiting-Time Analysis")

if waiting.empty:
    st.warning("Waiting-time summary CSV is missing or empty.")
else:
    st.subheader("Waiting-Time Summary")

    # Interactive activity filter
    if "activity" in waiting.columns:
        activities = ["All Activities"] + sorted(
            waiting["activity"].dropna().unique().tolist()
        )

        selected_activity = st.selectbox(
            "Filter by Patient Activity",
            activities,
            key="waiting_activity_filter"
        )

        if selected_activity == "All Activities":
            filtered_waiting = waiting.copy()
        else:
            filtered_waiting = waiting[
                waiting["activity"] == selected_activity
            ].copy()
    else:
        filtered_waiting = waiting.copy()
        st.warning("The activity column is missing from the waiting-time data.")

    # Display the filtered data
    st.dataframe(filtered_waiting, width="stretch")

    # Calculate metrics using the filtered data
    metric_cols = [
        col for col in [
            "average_minutes",
            "median_minutes",
            "maximum_minutes"
        ]
        if col in filtered_waiting.columns
    ]

    if metric_cols and not filtered_waiting.empty:
        col1, col2, col3 = st.columns(3)

        average_values = pd.to_numeric(
            filtered_waiting["average_minutes"], errors="coerce"
        ) if "average_minutes" in metric_cols else pd.Series(dtype=float)

        median_values = pd.to_numeric(
            filtered_waiting["median_minutes"], errors="coerce"
        ) if "median_minutes" in metric_cols else pd.Series(dtype=float)

        maximum_values = pd.to_numeric(
            filtered_waiting["maximum_minutes"], errors="coerce"
        ) if "maximum_minutes" in metric_cols else pd.Series(dtype=float)

        if "average_minutes" in metric_cols:
            col1.metric(
                "Average Waiting Time",
                f"{average_values.mean():.1f} min"
                if average_values.notna().any() else "N/A"
            )

        if "median_minutes" in metric_cols:
            col2.metric(
                "Median Waiting Time",
                f"{median_values.median():.1f} min"
                if median_values.notna().any() else "N/A"
            )

        if "maximum_minutes" in metric_cols:
            col3.metric(
                "Maximum Waiting Time",
                f"{maximum_values.max():.1f} min"
                if maximum_values.notna().any() else "N/A"
            )

    # Chart of average waiting time by activity
    if (
        "activity" in filtered_waiting.columns
        and "average_minutes" in filtered_waiting.columns
        and not filtered_waiting.empty
    ):
        fig_waiting = px.bar(
            filtered_waiting,
            x="activity",
            y="average_minutes",
            title="Average Waiting Time by Activity",
            labels={
                "activity": "Activity",
                "average_minutes": "Average Waiting Time (minutes)"
            },
            text="average_minutes"
        )

        fig_waiting.update_traces(
            texttemplate="%{text:.1f} min",
            textposition="outside"
        )
        fig_waiting.update_layout(xaxis_tickangle=-35)

        st.plotly_chart(fig_waiting, width="stretch")


# Workflow Bottleneck Analysis
st.header("🚦 Workflow Bottlenecks")
st.caption(
    "Identify transitions with longer waiting times using synthetic patient data."
)

if bottlenecks.empty:
    st.warning(
        "Bottleneck summary is missing or empty. "
        "Check Data/bottleneck_summary.csv."
    )
else:
    bottlenecks.columns = bottlenecks.columns.str.strip().str.lower()

    required = {"transition", "mean", "median", "max"}

    if required.issubset(bottlenecks.columns):
        bottlenecks["mean"] = pd.to_numeric(
            bottlenecks["mean"], errors="coerce"
        )
        bottlenecks["median"] = pd.to_numeric(
            bottlenecks["median"], errors="coerce"
        )
        bottlenecks["max"] = pd.to_numeric(
            bottlenecks["max"], errors="coerce"
        )

        valid = bottlenecks.dropna(subset=["mean", "median", "max"])

        if not valid.empty:
            slowest = valid.loc[valid["mean"].idxmax()]
            highest = valid.loc[valid["max"].idxmax()]

            col1, col2 = st.columns(2)

            col1.metric(
                "Slowest Average Transition",
                f"{slowest['mean']:.1f} minutes"
            )
            col1.caption(str(slowest["transition"]))

            col2.metric(
                "Highest Maximum Transition Time",
                f"{highest['max']:.1f} minutes"
            )
            col2.caption(str(highest["transition"]))

            st.subheader("Compare Transition Waiting Times")

            metric_choice = st.multiselect(
                "Choose metrics",
                ["mean", "median", "max"],
                default=["mean", "median"],
                format_func=lambda x: {
                    "mean": "Average",
                    "median": "Median",
                    "max": "Maximum"
                }[x],
                key="bottleneck_metrics"
            )

            if metric_choice:
                chart_data = valid.melt(
                    id_vars=["transition"],
                    value_vars=metric_choice,
                    var_name="Metric",
                    value_name="Minutes"
                )

                chart_data["Metric"] = chart_data["Metric"].map({
                    "mean": "Average",
                    "median": "Median",
                    "max": "Maximum"
                })

                fig = px.bar(
                    chart_data,
                    x="Minutes",
                    y="transition",
                    color="Metric",
                    barmode="group",
                    orientation="h",
                    title="Waiting Time by Patient Transition",
                    labels={
                        "Minutes": "Time (minutes)",
                        "transition": "Patient Transition"
                    }
                )

                fig.update_layout(
                    yaxis={"categoryorder": "total ascending"}
                )

                st.plotly_chart(fig, width="stretch")

            with st.expander("View Bottleneck Data"):
                st.dataframe(
                    valid.sort_values("mean", ascending=False),
                    width="stretch"
                )
        else:
            st.warning("No valid bottleneck measurements are available.")
    else:
        st.warning("The bottleneck CSV has unexpected column names.")


# Elapsed time data
with st.expander("Patient Elapsed-Time Data"):
    if elapsed.empty:
        st.warning("Elapsed-time CSV is missing or empty.")
    else:
        st.dataframe(elapsed, width="stretch")

st.success("CareFlow dashboard loaded.")
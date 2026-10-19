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


# Patient Group Filters
st.header("🔎 Patient Group Filters")

filter_col1, filter_col2 = st.columns(2)

# Department filter options
with filter_col1:
    if "department" in events.columns:
        department_options = sorted(
            events["department"].dropna().astype(str).unique()
        )

        selected_departments = st.multiselect(
            "Filter by Department",
            department_options,
            default=department_options,
            key="department_filter",
        )
    else:
        selected_departments = None

# Triage filter options
with filter_col2:
    if "triage_level" in events.columns:
        triage_options = sorted(
            events["triage_level"].dropna().astype(str).unique()
        )

        selected_triage = st.multiselect(
            "Filter by Triage Level",
            triage_options,
            default=triage_options,
            key="triage_filter",
        )
    else:
        selected_triage = None

# Identify cases that match the selected filters
matching_mask = pd.Series(True, index=events.index)

if selected_departments is not None:
    matching_mask &= (
        events["department"].astype(str).isin(selected_departments)
    )

if selected_triage is not None:
    matching_mask &= (
        events["triage_level"].astype(str).isin(selected_triage)
    )

matching_case_ids = events.loc[
    matching_mask, "case_id"
].dropna().unique()

# Keep the COMPLETE journey for each matching case
filtered_events = events[
    events["case_id"].isin(matching_case_ids)
].copy()

# Display filter results
metric_col1, metric_col2 = st.columns(2)

with metric_col1:
    st.metric(
        "Matching Patient Cases",
        filtered_events["case_id"].nunique()
    )

with metric_col2:
    st.metric(
        "Events in Matching Cases",
        len(filtered_events)
    )

st.caption(
    "Filters select patient cases with at least one event matching "
    "the selected department and triage levels. All events belonging "
    "to matching cases are retained so their complete pathways remain "
    "available. Other dashboard charts and metrics are not yet connected "
    "to these filters."
)

with st.expander("View filtered event data"):
    st.dataframe(
        filtered_events,
        hide_index=True,
        width="stretch",
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


# Patient Pathway Visualization
st.header("🧭 Patient Pathway Visualization")
st.caption(
    "Explore the activity sequence followed by individual "
    "synthetic patient cases."
)

required_columns = {"case_id", "event_number", "activity"}
if not events.empty and required_columns.issubset(events.columns):
    pathway_data = filtered_events.copy()

    pathway_data["event_number"] = pd.to_numeric(
        pathway_data["event_number"], errors="coerce"
    )

    pathway_data = pathway_data.dropna(
        subset=["case_id", "event_number", "activity"]
    ).sort_values(["case_id", "event_number"])

    patient_ids = sorted(pathway_data["case_id"].unique())

    if not patient_ids:
        st.info("No patient cases match the selected filters.")
    else:
        selected_patient = st.selectbox(
            "Choose a patient pathway",
            ["Most Common Pathway"] + patient_ids,
            key="patient_pathway_select",
        )

        if selected_patient == "Most Common Pathway":
            if not transitions.empty and {
                "previous_activity",
                "next_activity",
                "transition_count",
            }.issubset(transitions.columns):
                # Calculate transitions from filtered patient journeys.
                flow = pathway_data.sort_values(
                    ["case_id", "event_number"]
                ).copy()
                flow["next_activity"] = (
                    flow.groupby("case_id")["activity"].shift(-1)
                )
                flow = flow.dropna(subset=["activity", "next_activity"])
                flow = (
                    flow.groupby(["activity", "next_activity"])
                    .size()
                    .reset_index(name="transition_count")
                )
                flow = flow.rename(
                    columns={"activity": "previous_activity"}
                ).nlargest(10, "transition_count")

                fig_path = px.bar(
                    flow.sort_values("transition_count"),
                    x="transition_count",
                    y="previous_activity",
                    color="next_activity",
                    orientation="h",
                    barmode="group",
                    title="Most Frequent Activity Transitions",
                    labels={
                        "transition_count": "Number of Transitions",
                        "previous_activity": "Previous Activity",
                        "next_activity": "Next Activity",
                    },
                )
                st.plotly_chart(fig_path, width="stretch")
            else:
                st.info("Transition frequency data is unavailable.")
        else:
            patient_flow = pathway_data[
                pathway_data["case_id"] == selected_patient
            ].sort_values("event_number")
            patient_flow = patient_flow.drop_duplicates(
                subset=["event_number", "activity"]
            )

            st.write(f"**Patient case:** {selected_patient}")
            st.write(f"**Activities recorded:** {len(patient_flow)}")

            journey = " → ".join(
                patient_flow["activity"].astype(str).tolist()
            )
            st.markdown("### Patient Journey")
            st.info(journey)

            display_columns = [
                column
                for column in [
                    "event_number",
                    "timestamp",
                    "activity",
                    "department",
                    "triage_level",
                ]
                if column in patient_flow.columns
            ]
            st.dataframe(
                patient_flow[display_columns],
                hide_index=True,
                width="stretch",
            )

else:
    st.warning(
        "Patient pathway data is unavailable or required columns are missing."
    )


# Activity Frequency Analysis
st.header("📊 Activity Frequency Analysis")
st.caption(
    "Explore how often each activity appears in the synthetic event log."
)

if not events.empty and "activity" in events.columns:
  activity_counts = (
    filtered_events["activity"]
    .value_counts()
    .reset_index()
)
  
  activity_counts.columns = ["Activity", "Event Count"]
  fig_activity = px.bar(
        activity_counts.sort_values("Event Count"),
        x="Event Count",
        y="Activity",
        orientation="h",
        title="Frequency of Patient Activities",
        labels={
            "Event Count": "Number of Events",
            "Activity": "Hospital Activity",
        },
        text="Event Count",
    )  
  st.plotly_chart(fig_activity, width="stretch")

  with st.expander("View activity frequency data"):
        st.dataframe(
            activity_counts,
            hide_index=True,
            width="stretch",
        )
else:
    st.info("Activity frequency data is unavailable.")

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

    


# Waiting-Time Analysis
st.header("⏱️ Waiting-Time Analysis")
st.caption(
    "Elapsed time between consecutive recorded activities for "
    "patient cases matching the selected filters."
)

required_wait_columns = {
    "case_id", "event_number", "timestamp", "activity"
}

if not required_wait_columns.issubset(filtered_events.columns):
    st.warning(
        "Waiting-time analysis requires case_id, event_number, "
        "timestamp, and activity columns."
    )
else:
    # Prepare matching patient event records
    wait_events = filtered_events[
        ["case_id", "event_number", "timestamp", "activity"]
    ].copy()

    wait_events["event_number"] = pd.to_numeric(
        wait_events["event_number"], errors="coerce"
    )

    wait_events["timestamp"] = pd.to_datetime(
        wait_events["timestamp"], errors="coerce"
    )

    wait_events = wait_events.dropna(
        subset=["case_id", "event_number", "timestamp", "activity"]
    )

    wait_events = wait_events.sort_values(
        ["case_id", "event_number", "timestamp"]
    )

    # Calculate elapsed minutes since the previous event
    wait_events["previous_activity"] = (
        wait_events.groupby("case_id")["activity"].shift(1)
    )

    wait_events["previous_timestamp"] = (
        wait_events.groupby("case_id")["timestamp"].shift(1)
    )

    wait_events["time_minutes"] = (
        wait_events["timestamp"] - wait_events["previous_timestamp"]
    ).dt.total_seconds() / 60

    # Exclude first events and invalid negative time intervals
    wait_events = wait_events[
        wait_events["previous_timestamp"].notna()
        & wait_events["time_minutes"].ge(0)
    ].copy()

    if wait_events.empty:
        st.info(
            "No valid consecutive-event time intervals are available "
            "for the selected patient group."
        )
    else:
        # Summarize elapsed time by the activity reached
        waiting_summary = (
            wait_events.groupby("activity")["time_minutes"]
            .agg(
                average_minutes="mean",
                median_minutes="median",
                maximum_minutes="max",
                number_of_cases="count",
            )
            .reset_index()
            .sort_values("average_minutes", ascending=False)
        )

        # Overall interval metrics
        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Average Elapsed Time",
            f"{wait_events['time_minutes'].mean():.1f} min"
        )

        metric2.metric(
            "Median Elapsed Time",
            f"{wait_events['time_minutes'].median():.1f} min"
        )

        metric3.metric(
            "Maximum Elapsed Time",
            f"{wait_events['time_minutes'].max():.1f} min"
        )

        st.caption(
            "Elapsed time is measured from one recorded event to the "
            "next within each case. These values may include workflow "
            "time between activities and should not be interpreted as "
            "a direct measurement of staff waiting time."
        )

        # Filter the summary by activity
        activity_options = ["All Activities"] + sorted(
            waiting_summary["activity"].astype(str).unique().tolist()
        )

        selected_wait_activity = st.selectbox(
            "Filter waiting-time results by activity",
            activity_options,
            key="filtered_wait_activity",
        )

        if selected_wait_activity == "All Activities":
            displayed_waiting = waiting_summary.copy()
        else:
            displayed_waiting = waiting_summary[
                waiting_summary["activity"].astype(str)
                == selected_wait_activity
            ].copy()

        st.subheader("Elapsed-Time Summary by Activity")

        st.dataframe(
            displayed_waiting.round(2),
            hide_index=True,
            width="stretch",
        )

        # Plot average elapsed time
        fig_waiting = px.bar(
            displayed_waiting.sort_values("average_minutes"),
            x="average_minutes",
            y="activity",
            orientation="h",
            text="average_minutes",
            title="Average Elapsed Time by Activity",
            labels={
                "average_minutes": "Average Elapsed Time (minutes)",
                "activity": "Activity Reached",
            },
        )

        fig_waiting.update_traces(
            texttemplate="%{text:.1f} min",
            textposition="outside",
        )

        st.plotly_chart(fig_waiting, width="stretch")

        with st.expander("View calculated event intervals"):
            st.dataframe(
                wait_events[
                    [
                        "case_id",
                        "previous_activity",
                        "activity",
                        "previous_timestamp",
                        "timestamp",
                        "time_minutes",
                    ]
                ].round({"time_minutes": 2}),
                hide_index=True,
                width="stretch",
            )



# Workflow Bottleneck Analysis
st.header("🚦 Workflow Bottlenecks")
st.caption(
    "Explore longer elapsed-time intervals between consecutive "
    "activities in the selected synthetic patient group."
)

if "wait_events" in locals() and not wait_events.empty:
    bottleneck_data = (
        wait_events.groupby(
            ["previous_activity", "activity"]
        )["time_minutes"]
        .agg(
            mean="mean",
            median="median",
            maximum="max",
            interval_count="count",
        )
        .reset_index()
    )

    bottleneck_data["transition"] = (
        bottleneck_data["previous_activity"].astype(str)
        + " → "
        + bottleneck_data["activity"].astype(str)
    )

    bottleneck_data = bottleneck_data.sort_values(
        "mean", ascending=False
    )

    st.subheader("Longest Average Elapsed-Time Transitions")

    st.dataframe(
        bottleneck_data[
            ["transition", "mean", "median", "maximum", "interval_count"]
        ].round(2),
        hide_index=True,
        width="stretch",
    )

    if not bottleneck_data.empty:
        slowest = bottleneck_data.iloc[0]

        st.metric(
            "Longest Average Transition",
            f"{slowest['mean']:.1f} minutes",
        )
        st.write(f"**Transition:** {slowest['transition']}")

        fig_bottleneck = px.bar(
            bottleneck_data.head(10).sort_values("mean"),
            x="mean",
            y="transition",
            orientation="h",
            text="mean",
            title="Top 10 Transitions by Average Elapsed Time",
            labels={
                "mean": "Average Elapsed Time (minutes)",
                "transition": "Activity Transition",
            },
        )

        fig_bottleneck.update_traces(
            texttemplate="%{text:.1f} min",
            textposition="outside",
        )

        st.plotly_chart(fig_bottleneck, width="stretch")

    st.caption(
        "These are exploratory workflow intervals from synthetic data. "
        "Longer elapsed times do not establish the cause of a delay."
    )
else:
    st.info(
        "No valid event intervals are available for bottleneck analysis."
    )


# Actionable Bottleneck Insights
st.header("💡 Actionable Bottleneck Insights")

if not bottlenecks.empty and {
    "transition", "mean", "median", "max"
}.issubset(bottlenecks.columns):

    insight_data = bottlenecks.copy()

    for column in ["mean", "median", "max"]:
        insight_data[column] = pd.to_numeric(
            insight_data[column], errors="coerce"
        )

    insight_data = insight_data.dropna(subset=["mean"])
    insight_data = insight_data.sort_values(
        "mean", ascending=False
    )

    if not insight_data.empty:
        top = insight_data.iloc[0]

        st.metric(
            "Highest average waiting-time transition",
            str(top["transition"]),
            f'{top["mean"]:.1f} minutes average',
        )

        st.write("### Recommended areas for further investigation")

        for _, row in insight_data.head(3).iterrows():
            st.markdown(
                f"**{row['transition']}**"
            )
            st.write(
                f"Average: {row['mean']:.1f} minutes | "
                f"Median: {row['median']:.1f} minutes | "
                f"Maximum: {row['max']:.1f} minutes"
            )
            st.write(
                "Investigation idea: review the workflow handoff, "
                "staffing or resource availability, and whether "
                "delays are concentrated in particular cases."
            )
    else:
        st.info("No valid bottleneck measurements are available.")
else:
    st.info("Bottleneck summary data is unavailable.")

# Elapsed time data
with st.expander("Patient Elapsed-Time Data"):
    if elapsed.empty:
        st.warning("Elapsed-time CSV is missing or empty.")
    else:
        st.dataframe(elapsed, width="stretch")

st.success("CareFlow dashboard loaded.")
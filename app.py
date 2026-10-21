
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="CareFlow Analytics",
    page_icon="🏥",
    layout="wide"
)

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"

# Dashboard title
st.title("🏥 CareFlow Healthcare Analytics")
st.caption(
    "Patient pathways, waiting times and workflow bottlenecks"
)
st.info("This dashboard uses synthetic data, not real hospital records.")

# CSV loading function
def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        st.warning(f"Data file not found: {filename}")
        return pd.DataFrame()

    try:
        data = pd.read_csv(path)
        data.columns = data.columns.astype(str).str.strip()
        return data

    except (pd.errors.EmptyDataError,
            pd.errors.ParserError,
            UnicodeDecodeError,
            OSError) as error:
        st.error(f"Could not read {filename}: {error}")
        return pd.DataFrame()

# Load data BEFORE using it anywhere
events = load_csv("synthetic_event_log.csv")
elapsed = load_csv("pathway_journey_summary.csv")
transitions = load_csv("pathway_transition_summary.csv")
waiting = load_csv("waiting_time_summary.csv")
bottlenecks = load_csv("bottleneck_summary.csv")


# Executive Summary
st.header("📋 Executive Summary")

if not events.empty:
    total_patients = (
        events["case_id"].nunique()
        if "case_id" in events.columns
        else 0
    )

    st.subheader("Project Snapshot")

    col1, col2 = st.columns(2)
    col1.metric("Synthetic Patients", f"{total_patients:,}")
    col2.metric("Recorded Events", f"{len(events):,}")

    st.markdown("### Project Purpose")
    st.write(
        "CareFlow analyzes synthetic patient event logs to explore "
        "patient pathways, elapsed times between activities, and "
        "potential workflow bottlenecks."
    )

    st.caption(
        "All records are synthetic. Findings are exploratory and "
        "do not establish the causes of delays in a real hospital."
    )


# Data folder
DATA_DIR = Path(__file__).resolve().parent / "Data"




def load_csv(filename):
    """Load a CSV safely and report missing or invalid files."""
    path = DATA_DIR / filename

    if not path.exists():
        st.warning(f"Data file not found: {filename}")
        return pd.DataFrame()

    try:
        if path.stat().st_size == 0:
            st.warning(f"Data file is empty: {filename}")
            return pd.DataFrame()

        data = pd.read_csv(path)

        if data.empty:
            st.info(f"No records found in: {filename}")

        # Normalize column names to remove accidental whitespace
        data.columns = data.columns.astype(str).str.strip()

        return data

    except pd.errors.EmptyDataError:
        st.warning(f"Data file contains no readable data: {filename}")
    except pd.errors.ParserError:
        st.error(f"Could not parse CSV file: {filename}")
    except UnicodeDecodeError:
        st.error(f"Text encoding problem in CSV file: {filename}")
    except OSError as error:
        st.error(f"Could not read {filename}: {error}")

    return pd.DataFrame()

# CareFlow Overview KPI Cards
st.header("📌 CareFlow Overview")

total_patients = (
    events["case_id"].nunique()
    if not events.empty and "case_id" in events.columns
    else 0
)

total_events = len(events)

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

if not elapsed.empty and duration_col:
    journey_durations = pd.to_numeric(
        elapsed[duration_col], errors="coerce"
    ).dropna()
else:
    journey_durations = pd.Series(dtype=float)

avg_journey = (
    f"{journey_durations.mean():.1f} min"
    if not journey_durations.empty
    else "N/A"
)

longest_journey = (
    f"{journey_durations.max():.1f} min"
    if not journey_durations.empty
    else "N/A"
)

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Patients", f"{total_patients:,}")
k2.metric("Recorded Events", f"{total_events:,}")
k3.metric("Average Journey", avg_journey)
k4.metric("Longest Journey", longest_journey)


# Patient Group Filters
st.header("🔎 Patient Group Filters")

filter_col1, filter_col2 = st.columns(2)


# Patient Journey Duration
st.header("⏱️ Patient Journey Duration")

if not elapsed.empty:
    duration_col = next(
        (
            col for col in [
                "elapsed_minutes",
                "total_minutes",
                "duration_minutes",
                "elapsed_time_minutes",
            ]
            if col in elapsed.columns
        ),
        None,
    )

    if duration_col is not None:
        durations = pd.to_numeric(
            elapsed[duration_col],
            errors="coerce",
        ).dropna()

        if not durations.empty:
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Average Journey",
                f"{durations.mean():.1f} minutes",
            )
            col2.metric(
                "Longest Journey",
                f"{durations.max():.1f} minutes",
            )
            col3.metric(
                "Shortest Journey",
                f"{durations.min():.1f} minutes",
            )

            fig_duration = px.histogram(
                x=durations,
                nbins=20,
                title="Patient Journey Duration Distribution",
                labels={
                    "x": "Journey Duration (minutes)",
                    "count": "Number of Patients",
                },
            )

            st.plotly_chart(
                fig_duration,
                width="stretch",
            )
        else:
            st.warning("No valid journey durations found.")
    else:
        st.warning(
            "Duration column not found in pathway_journey_summary.csv."
        )
else:
    st.warning("Patient journey summary data is unavailable.")


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
                            flow.sort_values(
                                "transition_count",
                                ascending=True
                            ).tail(15),
                            x="transition_count",
                            y="previous_activity",
                            color="next_activity",
                            orientation="h",
                            barmode="stack",
                            title="Most Frequent Activity Transitions",
                            labels={
                                "transition_count": "Number of Transitions",
                                "previous_activity": "Previous Activity",
                                "next_activity": "Next Activity",
                            },
                            hover_data=["next_activity", "transition_count"],
                        )
        
                    
                        fig_path.update_layout(
                            height=650,
                            autosize=True,
                            margin=dict(
                                l=30,
                                r=20,
                                t=140,
                                b=60
                            ),
                            title=dict(
                                text="Most Frequent Activity Transitions",
                                x=0.02,
                                y=0.98
                            ),
                            legend=dict(
                                title_text="Next Activity",
                                orientation="h",
                                yanchor="bottom",
                                y=1.12,
                                xanchor="left",
                                x=0.02,
                                entrywidth=130,
                                entrywidthmode="pixels"
                            ),
                            xaxis_title="Number of Transitions",
                            yaxis_title="Previous Activity",
                            bargap=0.25,
                        )
        
                        fig_path.update_yaxes(
                            automargin=True
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
        .rename_axis("Activity")
        .reset_index(name="Event Count")
    )

    activity_counts = activity_counts.sort_values("Event Count", ascending=True)

    fig_activity = px.bar(
        activity_counts,
        x="Event Count",
        y="Activity",
        orientation="h",
        color="Activity",
        color_discrete_sequence=px.colors.qualitative.Set2,
        title="Activity Frequency"
    )

    fig_activity.update_layout(
        height=520,
        margin=dict(l=40, r=30, t=60, b=50),
        xaxis_title="Number of Events",
        yaxis_title="Hospital Activity",
    )

    fig_activity.update_yaxes(automargin=True)
    fig_activity.update_xaxes(rangemode="tozero")

    st.plotly_chart(fig_activity, width="stretch")

    with st.expander("View activity frequency data"):
        st.dataframe(
            activity_counts,
            hide_index=True,
            width="stretch",
        )
else:
    st.info("Activity frequency data is unavailable.")


# Patient Outcome Analysis
st.header("🏥 Patient Outcome Analysis")
st.caption(
    "Explore the final recorded outcomes of synthetic patient cases."
)

if (
    not filtered_events.empty
    and {"case_id", "event_number", "activity"}.issubset(
        filtered_events.columns
    )
):
    outcome_data = filtered_events[
        ["case_id", "event_number", "activity"]
    ].copy()

    outcome_data["event_number"] = pd.to_numeric(
        outcome_data["event_number"], errors="coerce"
    )

    outcome_data = outcome_data.dropna(
        subset=["case_id", "event_number", "activity"]
    )

    # Find the last recorded activity for each patient
    outcome_data = outcome_data.sort_values(
        ["case_id", "event_number"]
    )

    final_events = outcome_data.groupby(
        "case_id", as_index=False
    ).tail(1)

    final_events = final_events[
        final_events["activity"].isin(["Admission", "Discharge"])
    ]

    outcome_counts = (
        final_events.groupby("activity")["case_id"]
        .nunique()
        .reindex(["Discharge", "Admission"], fill_value=0)
        .reset_index(name="Patients")
    )

    total_outcomes = outcome_counts["Patients"].sum()

    if total_outcomes > 0:
        col1, col2, col3 = st.columns(3)

        discharged = int(
            outcome_counts.loc[
                outcome_counts["activity"] == "Discharge",
                "Patients"
            ].iloc[0]
        )

        admitted = int(
            outcome_counts.loc[
                outcome_counts["activity"] == "Admission",
                "Patients"
            ].iloc[0]
        )

        col1.metric("Patients Discharged", f"{discharged:,}")
        col2.metric("Patients Admitted", f"{admitted:,}")
        col3.metric("Cases with Recorded Outcomes", f"{total_outcomes:,}")

        outcome_counts["Percentage"] = (
            outcome_counts["Patients"] / total_outcomes * 100
        )

        fig_outcomes = px.pie(
            outcome_counts,
            names="activity",
            values="Patients",
            hole=0.45,
            title="Final Recorded Patient Outcomes",
        )

        fig_outcomes.update_traces(
            textposition="inside",
            texttemplate="%{label}<br>%{value} (%{percent})",
        )

        st.plotly_chart(fig_outcomes, width="stretch")

        st.dataframe(
            outcome_counts.rename(
                columns={
                    "activity": "Final Outcome",
                    "Patients": "Number of Patients",
                    "Percentage": "Percentage (%)",
                }
            ).round(2),
            hide_index=True,
            width="stretch",
        )

        st.caption(
            "Outcomes are inferred from each case's final recorded activity. "
            "Cases without a final Admission or Discharge event are excluded."
        )
    else:
        st.info("No final Admission or Discharge outcomes were found.")
else:
    st.info("Patient outcome data is unavailable or missing required columns.")



# Waiting-Time Analysis
st.header("⏱️ Waiting-Time Analysis")
st.caption(
    "Compare average elapsed time between consecutive activities. "
    "These intervals are not proof of the cause of a delay."
)

if not waiting.empty:
    required = {
        "previous_activity",
        "activity",
        "average_minutes",
        "number_of_cases",
    }

    if required.issubset(waiting.columns):
        wait_chart = waiting.copy()

        wait_chart["average_minutes"] = pd.to_numeric(
            wait_chart["average_minutes"], errors="coerce"
        )
        wait_chart["number_of_cases"] = pd.to_numeric(
            wait_chart["number_of_cases"], errors="coerce"
        )

        wait_chart = wait_chart.dropna(
            subset=["average_minutes", "number_of_cases"]
        )

        wait_chart["transition"] = (
            wait_chart["previous_activity"].astype(str)
            + " → "
            + wait_chart["activity"].astype(str)
        )

        wait_chart = wait_chart.sort_values(
            "average_minutes", ascending=True
        )

        fig_wait = px.bar(
            wait_chart,
            x="average_minutes",
            y="transition",
            orientation="h",
            color="average_minutes",
            hover_data=["number_of_cases"],
            text="average_minutes",
            title="Average Elapsed Time by Transition",
            labels={
                "average_minutes": "Average elapsed time (minutes)",
                "transition": "Activity transition",
                "number_of_cases": "Number of cases",
            },
            color_continuous_scale="Blues",
        )

        fig_wait.update_traces(
            texttemplate="%{text:.1f} min",
            textposition="outside",
            cliponaxis=False,
        )

        fig_wait.update_layout(
            height=420,
            margin=dict(l=20, r=60, t=70, b=40),
            coloraxis_showscale=False,
            yaxis_title="",
        )

        st.plotly_chart(
            fig_wait,
            width="stretch",
            config={"responsive": True},
        )

        st.subheader("Waiting-Time Details")

        display_cols = [
            "previous_activity",
            "activity",
            "average_minutes",
            "median_minutes",
            "maximum_minutes",
            "number_of_cases",
        ]

        available_cols = [
            col for col in display_cols if col in wait_chart.columns
        ]

        st.dataframe(
            wait_chart[available_cols].sort_values(
                "average_minutes", ascending=False
            ),
            width="stretch",
            hide_index=True,
        )
    else:
        st.warning("The waiting-time summary is missing required columns.")
else:
    st.info("No waiting-time summary data is available.")

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
st.header(" Workflow Bottlenecks")
st.caption(
    "Explore elapsed-time intervals between consecutive activities "
    "for the selected synthetic patient group."
)

if "wait_events" in locals() and not wait_events.empty:
    bottleneck_data = (
        wait_events.groupby(["previous_activity", "activity"])["time_minutes"]
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

    bottleneck_data = bottleneck_data.dropna(
        subset=["mean", "median", "maximum"]
    )

    bottleneck_data = bottleneck_data.sort_values("mean", ascending=False)

    st.subheader("Longest Average Elapsed-Time Transitions")

    display_bottlenecks = bottleneck_data[
        ["transition", "mean", "median", "maximum", "interval_count"]
    ].rename(
        columns={
            "transition": "Activity Transition",
            "mean": "Average (min)",
            "median": "Median (min)",
            "maximum": "Maximum (min)",
            "interval_count": "Recorded Intervals",
        }
    )

    st.dataframe(
        display_bottlenecks.round(2),
        hide_index=True,
        width="stretch",
        height=420,
        column_config={
            "Activity Transition": st.column_config.TextColumn(
                "Activity Transition",
                width="large",
            ),
            "Average (min)": st.column_config.NumberColumn(
                "Average (min)",
                format="%.2f",
            ),
            "Median (min)": st.column_config.NumberColumn(
                "Median (min)",
                format="%.2f",
            ),
            "Maximum (min)": st.column_config.NumberColumn(
                "Maximum (min)",
                format="%.2f",
            ),
            "Recorded Intervals": st.column_config.NumberColumn(
                "Recorded Intervals",
                format="%d",
            ),
        },
    )

    if not bottleneck_data.empty:
        slowest = bottleneck_data.iloc[0]

        col1, col2 = st.columns(2)

        col1.metric(
            "Longest Average Interval",
            f"{slowest['mean']:.1f} min",
        )

        col2.metric(
            "Recorded Intervals",
            int(slowest["interval_count"]),
        )

        st.write(f"**Transition:** {slowest['transition']}")

        chart_data = bottleneck_data.head(10).sort_values("mean", ascending=True)

        fig_bottleneck = px.bar(
            chart_data,
            x="mean",
            y="transition",
            orientation="h",
            text="mean",
            hover_data=["median", "maximum", "interval_count"],
            title="Top Transitions by Average Elapsed Time",
            labels={
                "mean": "Average Elapsed Time (minutes)",
                "transition": "Activity Transition",
                "median": "Median (minutes)",
                "maximum": "Maximum (minutes)",
                "interval_count": "Recorded Intervals",
            },
        )

        fig_bottleneck.update_traces(
            texttemplate="%{text:.1f} min",
            textposition="outside",
            cliponaxis=False,
        )

        fig_bottleneck.update_layout(
            height=450,
            margin=dict(l=20, r=70, t=70, b=40),
            yaxis_title="",
        )

        st.plotly_chart(
            fig_bottleneck,
            width="stretch",
            config={"responsive": True},
        )

        st.caption(
            "These are exploratory intervals from synthetic data. "
            "Small interval counts indicate limited evidence. "
            "Elapsed time alone does not establish the cause of a delay."
        )
    else:
        st.info("No valid bottleneck measurements are available.")
else:
    st.info(
        "No valid event intervals are available for bottleneck analysis."
    )


# Actionable Bottleneck Insights
st.header("💡 Actionable Bottleneck Insights")

if "bottleneck_data" in locals() and not bottleneck_data.empty:
    st.write("### Recommended areas for further investigation")

    for _, row in bottleneck_data.head(3).iterrows():
        st.markdown(f"**{row['transition']}**")

        st.write(
            f"Average: {row['mean']:.1f} minutes | "
            f"Median: {row['median']:.1f} minutes | "
            f"Maximum: {row['maximum']:.1f} minutes | "
            f"Recorded intervals: {int(row['interval_count'])}"
        )

        st.write(
            "Investigation idea: review the workflow handoff, "
            "resource availability, and whether delays are concentrated "
            "in particular cases. Validate findings against a larger "
            "sample before recommending process changes."
        )
else:
    st.info(
        "Bottleneck insights will appear when valid event intervals "
        "are available for the selected patient group."
    )

# Elapsed time data
with st.expander("Patient Elapsed-Time Data"):
    if elapsed.empty:
        st.warning("Elapsed-time CSV is missing or empty.")
    else:
        st.dataframe(elapsed, width="stretch")

st.success("CareFlow dashboard loaded.")
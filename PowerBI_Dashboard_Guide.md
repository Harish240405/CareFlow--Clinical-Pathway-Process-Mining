# CareFlow Power BI Dashboard Guide

## 1. Overview

CareFlow includes a Power BI report for exploring synthetic hospital
patient pathways, journey durations, activity frequencies, and waiting times.

Report file: `CareFlow_Analytics.pbix`

The report complements the existing Python and Streamlit dashboard.

## 2. Data Sources

The Power BI report uses these CSV datasets:

- `synthetic_event_log.csv`
- `pathway_journey_summary.csv`
- `bottleneck_summary.csv`

The files are stored in the project's `Data` directory.

### Synthetic Event Log

Contains patient case identifiers, event numbers, timestamps,
activities, departments, and triage levels.

### Patient Journey Summary

Contains each case's first event, last event, event count,
and total elapsed journey time in minutes.

### Bottleneck Summary

Contains workflow transitions and their mean, median,
and maximum observed waiting times.

## 3. Dashboard KPI Cards

The main report page contains three key performance indicators.

### Total Patient Cases

Displays the number of patient cases in the journey dataset.

Current dataset value: 500 cases.

### Average Journey Duration

Displays the average elapsed time across patient journeys.

Current dataset value: approximately 179.58 minutes.

### Longest Journey

Displays the maximum recorded journey duration.

Current dataset value: 332 minutes.

These values describe the current synthetic dataset and may
change if the data is regenerated.

## 4. Dashboard Visualizations

### Activity Frequency

Shows the number of recorded events for each activity.

It helps compare how frequently different hospital activities
appear in the synthetic event log.

### Patient Journey Duration Distribution

Groups patient journey durations into 30-minute bins.

It helps explore how journey durations are distributed
across the 500 patient cases.

### Average Waiting Time by Workflow Transition

Compares average waiting times between workflow activities.

It helps identify transitions with comparatively longer
observed waiting periods.

### Patient Event Details

Displays patient event records in a table.

The table supports examination of individual case information.

## 5. Interactive Filters

The main report page includes two slicers.

### Department Slicer

Filters supported event-level visuals by department.

### Triage Level Slicer

Filters supported event-level visuals by triage level.

The slicers have been tested with the Activity Frequency
visual and the patient journey KPI card.

Filter behaviour depends on the relationships and fields
used by each visual.

## 6. Patient Journey Details Page

A separate report page is provided for patient-level exploration.

It uses the `case_id` field for drill-through navigation.

The page displays the selected patient's:

- Case identifier
- Event count
- Total elapsed journey duration
- First recorded event
- Last recorded event

To use drill-through:

1. Open the main dashboard page.
2. Select a patient case in a suitable visual.
3. Right-click the selected case.
4. Choose the Patient Journey Details drill-through option.
5. Review the selected patient's journey summary.

This page currently displays journey summary information.
It is not a complete event-by-event timeline.

## 7. Data Relationships

The event log and journey summary tables are related
through the `case_id` field.

The event log contains multiple records for a patient case,
while the journey summary contains one summary record per case.

The bottleneck summary is a separate aggregated dataset.
It should not be connected using an unrelated field.

## 8. Opening the Power BI Report

1. Open Power BI Desktop.
2. Select File and then Open.
3. Browse to `CareFlow_Analytics.pbix`.
4. Open the report.
5. Review the dashboard and its report pages.

If the CSV source location changes, update the data source
paths in Power BI before refreshing the report.

## 9. Analytical Purpose

The report is designed to help users:

- Explore patient journey durations.
- Compare hospital activity frequencies.
- Examine workflow waiting-time patterns.
- Filter supported visuals by department.
- Filter supported visuals by triage level.
- Inspect individual patient journey summaries.
- Identify transitions for further investigation.

## 10. Limitations

- All patient records are synthetic.
- The report is intended for educational demonstration.
- Waiting-time patterns do not establish the cause of delays.
- Slicers affect visuals according to configured relationships
  and visual interactions.
- The patient drill-through page displays summary fields,
  not a complete event-level timeline.
- Results are not clinical recommendations.

## 11. Technology

- Microsoft Power BI Desktop
- CSV datasets
- Python
- Pandas
- Streamlit
- Plotly
- Git and GitHub

## 12. Project File

The Power BI report is stored in:

`CareFlow_Analytics.pbix`

The report is part of the CareFlow Healthcare Analytics project.

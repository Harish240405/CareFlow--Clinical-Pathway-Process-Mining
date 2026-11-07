# Week 3 - Power BI Development

**Date:** 1-7 November 2026  
**Latest Update:** 7 November 2026  
**Developer:** Harish Nimaje  
**Project:** CareFlow Healthcare Analytics  
**Platform:** Microsoft Power BI

## 1. Project Overview

CareFlow is a healthcare analytics project that analyzes synthetic
hospital patient journey data.

The objective is to understand patient pathways, waiting times,
and workflow bottlenecks.

Power BI is used to create interactive reports and dashboards.
Python and Streamlit are also used for data analysis.

## 2. Dataset Information

The project uses synthetic hospital patient records.

- Total event records: 4,420
- Unique patient cases: 500
- Patient journey summary records: 500

Each event represents an activity in a patient's hospital journey.
Timestamps are used to analyze the time between activities.

## 3. Data Sources

The following CSV files are used:

- synthetic_event_log.csv
- pathway_journey_summary.csv
- pathway_transition_summary.csv
- waiting_time_summary.csv
- bottleneck_summary.csv

These datasets contain patient activities, journey durations,
transition times, waiting times, and bottleneck information.

## 4. Main Power BI Dashboard

The main dashboard includes:

- Patient journey overview
- KPI cards
- Department filtering
- Triage Level filtering
- Activity frequency analysis
- Workflow bottleneck analysis
- Patient journey duration analysis

The dashboard helps users explore hospital workflow performance.

## 5. Patient Journey Details Page

A second report page named Patient Journey Details was created.

It provides patient-level journey information.

The page contains:

- Patient journey KPI cards
- Patient-level details table
- Journey duration distribution chart
- Department slicer
- Triage Level slicer

## 6. Patient-Level Table

The patient table contains:

- case_id
- event_count
- elapsed_minutes
- first_event
- last_event

These fields help compare individual patient journeys.

## 7. KPI Development

Four KPI cards are included.

### Total Patients
- Calculation: Distinct count of case_id.
- Dataset value: 500.

### Average Journey Duration
- Calculation: Average of elapsed_minutes.
- Dataset value: Approximately 179.58 minutes.

### Maximum Journey Duration
- Calculation: Maximum of elapsed_minutes.
- Dataset value: 332 minutes.

### Shortest Journey Duration
- Calculation: Minimum of elapsed_minutes.
- Dataset value: 48 minutes.

## 8. Data Model and Relationship Validation

**Review Date: 7 November 2026**

The Power BI Model View was inspected.

The relationship between the following tables was verified:

- synthetic_event_log
- pathway_journey_summary

Relationship configuration:

| Property | Configuration |
|---|---|
| First table | synthetic_event_log |
| First column | case_id |
| Second table | pathway_journey_summary |
| Second column | case_id |
| Cardinality | Many to One (*:1) |
| Relationship status | Active |
| Cross-filter direction | Both |

The existing relationship configuration was found to be correct.
No relationship changes were required during this review.

## 9. Interactive Dashboard Development

The report includes two slicers:

1. Department
2. Triage Level

The slicers provide filtering options for patient journey analysis.

The relationship and filtering configuration were reviewed.

Further testing is required to verify that all KPI cards,
tables, and charts respond correctly to slicer selections.

## 10. Patient Journey Distribution

A horizontal bar chart displays patient journey durations.

The chart helps identify differences between shorter and
longer patient journeys.

Further interaction validation is required.

## 11. Work Completed on 7 November 2026

The following activities were completed:

1. Opened the Patient Journey Details report page.
2. Reviewed the patient-level KPI cards.
3. Inspected the patient journey details table.
4. Reviewed the journey duration distribution chart.
5. Inspected the Department slicer.
6. Inspected the Triage Level slicer.
7. Opened Power BI Model View.
8. Inspected the case_id relationship.
9. Verified Many-to-One cardinality.
10. Verified that the relationship is active.
11. Verified Both cross-filter direction.
12. Reviewed the existing GitHub project status.

## 12. Pending Development Tasks

- Configure and validate Edit Interactions.
- Test Department slicer filtering.
- Test Triage Level slicer filtering.
- Verify KPI card filtering.
- Verify patient table filtering.
- Verify journey chart filtering.
- Test patient-level drill-through navigation.
- Improve visual alignment and formatting.
- Validate KPI values against source datasets.
- Save and review the final Power BI report.

## 13. GitHub Progress

Repository branch: main

Remote branch: origin/main

The local repository is synchronized with GitHub.

The backup files app_backup.py and
app_before_improvements.py remain untracked.

No new commit was created on 7 November because
there were no modified tracked project files.

## 14. Next Development Session

The next session will focus on Power BI visual interactions.

The following improvements are planned:

- Configure Edit Interactions.
- Correct any filtering issues.
- Validate all dashboard visuals.
- Improve patient journey analysis.
- Update project documentation.
- Verify at least 50 meaningful changed lines before committing.

## 15. Project Status

**Week:** 3  
**Platform:** Microsoft Power BI  
**Report:** CareFlow_Analytics.pbix  
**Status:** In Progress  
**Project:** CareFlow Healthcare Analytics

The main dashboard and Patient Journey Details page
have been developed.

The data model relationship has been reviewed and verified.

Visual interaction testing and final dashboard improvements
remain ongoing.


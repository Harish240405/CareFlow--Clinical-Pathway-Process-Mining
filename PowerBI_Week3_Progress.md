# CareFlow Healthcare Analytics
## Week 3 - Power BI Development

Date: 1 November 2026
Developer: Harish Nimaje

## 1. Project Overview
CareFlow is a healthcare analytics project.
It analyzes synthetic hospital patient journey data.
The goal is to identify workflow delays and bottlenecks.
Power BI is being used for interactive visualization.

## 2. Dataset Information
The project uses synthetic patient records.
The event log contains 4420 events.
The dataset represents 500 unique patients.
The journey summary contains 500 patient records.

## 3. Data Sources
- synthetic_event_log.csv
- pathway_journey_summary.csv
- pathway_transition_summary.csv
- waiting_time_summary.csv
- bottleneck_summary.csv

## 4. Main Dashboard
The main dashboard was developed in Power BI.
Total patient cases KPI was created.
Average journey duration KPI was created.
Longest journey KPI was created.
Department slicer was implemented.
Triage level slicer was implemented.
Patient journey distribution was added.
Activity frequency analysis was added.
Workflow bottleneck analysis was added.

## 5. Patient Journey Details
A new report page was created.
The page is named Patient Journey Details.
A patient-level journey table was created.
The table displays individual patient information.

## 6. Patient Table Columns
- case_id
- event_count
- elapsed_minutes
- first_event
- last_event

## 7. KPI Development
Total patients uses distinct count of case_id.
The expected total patient count is 500.
Average journey uses elapsed_minutes average.
The expected average is 179.58 minutes.
Longest journey uses elapsed_minutes maximum.
The expected maximum is 332 minutes.

## 8. Interactive Development
The case_id field was added to drill-through.
Patient table selection was tested.
KPI filtering behaviour was verified.
KPI values returned after clearing selection.

## 9. Development Progress
Power BI datasets were imported.
The main report page was completed.
The patient details page was created.
Three patient journey KPI cards were created.
The patient details table was completed.
The report layout is being improved.

## 10. Remaining Tasks
Complete patient journey duration chart.
Test patient-level drill-through.
Improve visual formatting.
Validate all report interactions.
Save the final Power BI report.

## 11. Expected Outcome
Provide patient journey information.
Identify hospital workflow bottlenecks.
Understand patient waiting times.
Support data-driven hospital administration.

## 12. Project Status
Week: 3
Platform: Microsoft Power BI
Status: In Progress
Project: CareFlow Healthcare Analytics

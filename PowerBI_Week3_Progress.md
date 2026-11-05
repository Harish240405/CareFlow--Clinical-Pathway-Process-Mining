# \# Week 3 - Power BI Development

# 

# \*\*Date:\*\* 1 November 2026  

# \*\*Developer:\*\* Harish Nimaje  

# \*\*Project:\*\* CareFlow Healthcare Analytics  

# \*\*Platform:\*\* Microsoft Power BI

# 

# \## 1. Project Overview

# 

# CareFlow is a healthcare analytics project.

# It analyzes synthetic hospital patient journey data.

# The objective is to understand patient pathways and workflow delays.

# The project focuses on identifying bottlenecks in hospital processes.

# Microsoft Power BI is used to build interactive reports.

# Python and Streamlit are also used for data analysis and visualization.

# 

# \## 2. Dataset Information

# 

# The project uses synthetic hospital patient records.

# The event log contains 4,420 events.

# The dataset represents 500 unique patient cases.

# The journey summary contains 500 patient records.

# Each event represents an activity in a patient's hospital journey.

# Timestamps are used to analyze the time between activities.

# 

# \## 3. Data Sources

# 

# The following CSV files are used:

# 

# \- `synthetic\_event\_log.csv`

# \- `pathway\_journey\_summary.csv`

# \- `pathway\_transition\_summary.csv`

# \- `waiting\_time\_summary.csv`

# \- `bottleneck\_summary.csv`

# 

# These files provide patient activity, journey duration, transition and waiting-time information.

# 

# \## 4. Main Dashboard

# 

# The main dashboard was developed in Power BI.

# The report includes patient journey and workflow information.

# KPI cards were created to display important metrics.

# Department and Triage Level slicers were added.

# Patient journey duration distribution was added.

# Activity frequency analysis was included.

# Workflow bottleneck analysis was included.

# The dashboard is designed to support interactive data exploration.

# 

# \## 5. Patient Journey Details Page

# 

# A second report page was created.

# The page is named \*\*Patient Journey Details\*\*.

# It provides information about individual patient journeys.

# A patient-level table was added.

# The page also includes patient journey KPI cards.

# A duration distribution chart was added to understand journey-time variation.

# 

# \## 6. Patient Table Columns

# 

# The patient-level table contains the following fields:

# 

# \- `case\_id`

# \- `event\_count`

# \- `elapsed\_minutes`

# \- `first\_event`

# \- `last\_event`

# 

# These fields help compare the number of activities and total journey duration for individual patients.

# 

# \## 7. KPI Development

# 

# Four KPI cards are included on the patient details page.

# 

# \### Total Patients

# \- Calculation: Distinct count of `case\_id`.

# \- Expected value: 500 patients.

# 

# \### Average Journey Duration

# \- Calculation: Average of `elapsed\_minutes`.

# \- Expected value: Approximately 179.58 minutes.

# 

# \### Maximum Journey Duration

# \- Calculation: Maximum of `elapsed\_minutes`.

# \- Expected value: 332 minutes.

# 

# \### Shortest Journey Duration

# \- Calculation: Minimum of `elapsed\_minutes`.

# \- Expected value: 48 minutes.

# 

# These KPIs provide a quick overview of patient journey performance.

# 

# \## 8. Interactive Development

# 

# A Department slicer was added.

# A Triage Level slicer was added.

# The `case\_id` field was added to the drill-through configuration.

# Patient table selection was tested.

# KPI filtering behaviour was checked.

# KPI values returned after clearing the selection.

# Further validation of slicer interactions and patient-level drill-through is required.

# 

# \## 9. Patient Journey Distribution

# 

# A patient journey duration distribution chart was added.

# The chart helps visualize differences in patient journey times.

# It supports analysis of shorter and longer patient journeys.

# The distribution can help identify unusual journey durations.

# Its interaction with report filters will be validated.

# 

# \## 10. Report Development Progress

# 

# Power BI datasets were imported.

# The main report page was developed.

# The Patient Journey Details page was created.

# Four patient journey KPI cards were created.

# The patient-level details table was added.

# The journey duration distribution chart was added.

# Department and Triage Level slicers were created.

# The report was saved as `CareFlow\_Analytics.pbix`.

# Visual formatting and interaction testing are ongoing.

# 

# \## 11. Remaining Tasks

# 

# \- Validate Department slicer behaviour.

# \- Validate Triage Level slicer behaviour.

# \- Test patient-level drill-through navigation.

# \- Check filtering across the patient table and charts.

# \- Improve the alignment and formatting of report visuals.

# \- Verify KPI values against the source data.

# \- Save and review the final Power BI report.

# 

# \## 12. Expected Outcome

# 

# Provide clear information about patient journeys.

# Understand the duration of individual patient pathways.

# Identify hospital workflow bottlenecks.

# Analyze waiting times between activities.

# Compare patient journeys across departments and triage levels.

# Support data-driven hospital administration.

# 

# \## 13. Project Status

# 

# \*\*Week:\*\* 3  

# \*\*Platform:\*\* Microsoft Power BI  

# \*\*Report:\*\* `CareFlow\_Analytics.pbix`  

# \*\*Status:\*\* In Progress  

# \*\*Project:\*\* CareFlow Healthcare Analytics

# 

# The main dashboard and patient details page have been developed.

# The remaining work focuses on validating report interactions and improving the final layout.


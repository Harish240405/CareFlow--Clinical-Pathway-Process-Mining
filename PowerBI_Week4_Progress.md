# Week 4 - Power BI Dashboard Validation

**Date:** 8 November 2026
**Developer:** Harish Nimaje
**Project:** CareFlow Healthcare Analytics
**Platform:** Microsoft Power BI

## 1. Today's Objective

Continue development of the CareFlow Power BI dashboard.
Validate patient-level filtering and KPI calculations.
Investigate Department slicer interaction issues.

## 2. Patient Journey Details

Reviewed the Patient Journey Details report page.
Checked the four patient KPI cards.
Reviewed the patient-level details table.
Reviewed the patient journey duration chart.

## 3. KPI Validation

The report contains four KPI cards.

- Total Patients
- Average Journey Duration
- Maximum Journey Duration
- Shortest Journey Duration

Verified the unfiltered patient count of 500.
Verified average journey duration of 179.58 minutes.
Verified maximum journey duration of 332 minutes.
Verified minimum journey duration of 48 minutes.

## 4. Triage Level Testing

Tested the Critical triage selection.
Observed 21 patients.
Observed average journey duration of 144.95 minutes.
Observed maximum journey duration of 222 minutes.
Observed minimum journey duration of 48 minutes.

The KPI cards responded to the Critical selection.

## 5. Department Slicer Testing

Tested the Emergency department selection.
Observed that Total Patients displayed 500.
Further investigation is required.
The Department slicer interaction is not yet confirmed as correct.

## 6. Data Model Investigation

Opened Power BI Model View.
Inspected the synthetic_event_log table.
Inspected the pathway_journey_summary table.
Checked the case_id relationship.

Relationship configuration:
- From: synthetic_event_log
- To: pathway_journey_summary
- Matching column: case_id
- Cardinality: Many to one (*:1)
- Cross-filter direction: Both
- Relationship status: Active

The relationship configuration was inspected.
No relationship changes were made.

## 7. Dashboard Components

Reviewed patient KPI cards.
Reviewed the patient-level table.
Reviewed the duration distribution chart.
Reviewed Department slicer.
Reviewed Triage Level slicer.

## 8. Remaining Tasks

- Investigate Department slicer filtering.
- Test Emergency department patient count.
- Test Inpatient department patient count.
- Test Laboratory department patient count.
- Test Reception department patient count.
- Validate combined slicer selections.
- Verify patient table filtering.
- Verify duration chart filtering.
- Improve dashboard visual formatting.
- Save and review the Power BI report.

## 9. Current Project Status

Power BI dashboard development is ongoing.
Patient KPI calculations have been reviewed.
Critical triage filtering has been tested.
Department relationship configuration has been inspected.
Department slicer validation remains pending.

## 10. Expected Outcome

Build a reliable interactive patient journey dashboard.
Provide accurate patient-level information.
Identify hospital workflow bottlenecks.
Analyze patient journey duration.
Support healthcare process improvement.

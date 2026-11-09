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

---

# Week 4 - Continued Power BI Development

**Date:** 9 November 2026  
**Developer:** Harish Nimaje  
**Project:** CareFlow Healthcare Analytics  
**Platform:** Microsoft Power BI

## 11. Today's Objective

Develop a dedicated Patient Drill Through report page.
Display individual patient journey information.
Add patient-level KPI cards.
Explore an activity timeline for individual patients.

## 12. Patient Drill Through Page

Created a new report page named Patient Drill Through.
Configured the patient identifier as the drill-through field.
Used the case_id column from synthetic_event_log.
Enabled the Keep all filters option.
Added a title for Patient Individual Journey Analysis.

The page is designed to display information for one selected patient.
The drill-through context is based on the selected patient case.
The page can be opened from a patient-level report selection.

## 13. Patient Identification

Added a Selected Patient ID card.
Used the selected case_id to identify the patient.
The card displays the patient identifier in the drill-through context.
Tested the page using patient P0001.

## 14. Patient Activity Count KPI

Created a measure named Patient Activity Count.

DAX measure:

    Patient Activity Count =
    COUNTROWS(synthetic_event_log)

Added the measure to a KPI card.
Tested the measure using patient P0001.
Observed 10 recorded activities for the selected patient.

## 15. Patient Journey Duration KPI

Created a measure named Selected Patient Journey Minutes.

DAX measure:

    Selected Patient Journey Minutes =
    VAR SelectedCase =
        SELECTEDVALUE(synthetic_event_log[case_id])
    RETURN
        LOOKUPVALUE(
            pathway_journey_summary[elapsed_minutes],
            pathway_journey_summary[case_id],
            SelectedCase
        )

Added the measure to a KPI card.
The measure retrieves journey duration using the selected case_id.
Tested the measure using patient P0001.
Observed a journey duration of 215 minutes.

## 16. Patient Activity Details

Added a table visual to display patient activity records.
Used the synthetic_event_log table as the source.
Reviewed the activity records for the selected patient.
Checked the patient identifier in the drill-through context.
Reviewed the available activity and event information.

## 17. Activity Timeline Development

Started developing a matrix visual for the patient activity timeline.
Added event_number as an initial field.
The intention is to organize patient activities in event order.
Additional activity details are to be added and reviewed.

The timeline visual is still under development.
Further formatting and validation are required.
No final timeline validation is claimed.

## 18. Patient Drill Through Testing

Selected patient P0001 for testing.
Confirmed that the drill-through page displayed the selected patient.
Observed 10 patient activity records.
Observed a journey duration of 215 minutes.
Reviewed the patient-specific information displayed by the KPI cards.

These observations represent the test performed for P0001.
Additional patients should be tested before final validation.

## 19. Work Completed Today

- Created the Patient Drill Through report page.
- Configured case_id as the drill-through field.
- Enabled Keep all filters.
- Added the Patient Individual Journey Analysis title.
- Added the Selected Patient ID card.
- Created the Patient Activity Count measure.
- Added the Patient Activity Count KPI card.
- Created the Selected Patient Journey Minutes measure.
- Added the journey duration KPI card.
- Added a patient activity details table.
- Tested the drill-through using P0001.
- Reviewed the individual patient activity records.
- Started the activity timeline matrix.

## 20. Remaining Tasks

- Complete the patient activity timeline matrix.
- Add and organize the required activity fields.
- Check chronological event ordering.
- Test drill-through with additional patient IDs.
- Verify patient activity counts for multiple patients.
- Verify journey duration calculations for multiple patients.
- Review the display of missing or blank values.
- Improve the drill-through page layout.
- Check visual alignment and formatting.
- Save and review the final Power BI report.

## 21. Current Project Status

The Patient Drill Through page has been created.
The case_id drill-through configuration has been tested.
Patient-level KPI measures have been created.
Patient P0001 was used for initial testing.
The activity timeline matrix is still being developed.
Further testing is required before marking the page complete.

## 22. Expected Outcome

Provide a detailed view of an individual patient journey.
Make patient activity information easier to inspect.
Display the number of recorded activities.
Display the selected patient's journey duration.
Support investigation of patient workflow sequences.
Improve the usability of the CareFlow analytics report.


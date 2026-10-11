Elapsed-Time Analysis

The CareFlow project analyzes patient journey durations using recorded event timestamps.

Analysis

- Groups events by patient.
- Calculates elapsed time between the first and last recorded events.
- Summarizes patient journey durations.
- Identifies activity transitions that may require further investigation.

Results

Three patient journeys were analyzed:

Patient| Elapsed time
P001| 120 minutes
P002| 155 minutes
P003| 75 minutes

Output Files

- "patient_elapsed_times.csv" — patient-level elapsed-time results.
- "patients_journey_chart.png" — patient journey visualization.
- "waiting_time_chart.png" — activity-transition visualization.
- "patient_pathway_findings.md" — project findings and limitations.

Limitations

The dataset contains only three patient journeys, so the findings are preliminary. Elapsed time includes the entire recorded interval and should not be interpreted as waiting time alone.

Bottleneck Analysis

Objective

Identify the longest activity transitions in the CareFlow patient workflow using patient event logs.

Key Findings

- Sample Collected → Lab Results Available: 53.71 minutes average.
- Triage → Doctor Consultation: 38.45 minutes average.
- Treatment → Admission: 36.81 minutes average.
- Treatment → Discharge: 35.63 minutes average.

Generated Outputs

- "bottleneck_chart.png" — Chart of the 10 longest activity transitions.
- "bottleneck_summary.csv" — Transition statistics containing mean, median, and maximum elapsed times.

Conclusion

The longest average transition is Sample Collected → Lab Results Available. Further investigation of laboratory turnaround time may help identify opportunities to improve patient flow.

Week 2: Patient Waiting-Time Analysis

Objective

Analyze elapsed times between consecutive patient-care activities to identify transitions that may require further investigation.

Work Completed

- Processed the synthetic patient event log using Python and pandas.
- Calculated elapsed time between consecutive activities for each patient.
- Generated activity-transition summaries containing average, median, and maximum elapsed times.
- Created a horizontal bar chart showing the ten transitions with the highest average elapsed times.

Preliminary Findings

- Sample Collected → Lab Results Available had the highest average elapsed time in the generated chart.
- Triage → Doctor Consultation also showed a relatively long elapsed interval.
- Other transitions, including Treatment → Admission and Treatment → Discharge, warrant further examination.

Deliverables

- "Data/analyze_waiting_times.py"
- "Data/patient_waiting_times.csv"
- "Data/waiting_time_summary.csv"
- "Data/waiting_time_chart.py"
- "Data/waiting_time_chart.png"

Limitations

Elapsed time between recorded activities is not necessarily actual waiting time. It may include active care, processing time, or unrecorded activities. Findings based on synthetic or limited data are preliminary and should not be treated as validated clinical conclusions.

Next Steps

- Validate the event log and timestamp ordering.
- Investigate the longest activity transitions.
- Expand the dataset and compare results across patients.
- Document findings before recommending workflow changes.
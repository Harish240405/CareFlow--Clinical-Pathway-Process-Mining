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
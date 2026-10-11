CareFlow: Clinical Pathway Process Mining

1. Project Overview

This project analyzes patient event logs to understand clinical pathways, patient journey durations, and activity frequencies.

2. Dataset

The analysis uses a sample patient event dataset containing patient IDs, clinical activities, and timestamps.

3. Patient Journey Analysis

The analysis calculates:

- Total number of events
- Number of unique patients
- Frequency of clinical activities
- Number of events per patient
- Patient journey start and end times
- Total journey duration in minutes

4. Initial Findings

The sample analysis includes three patient cases: P001, P002, and P003.

The program calculates journey durations and event counts for each case. The average journey duration printed by the current run is approximately 116.67 minutes.

These results describe the sample dataset only and should not be interpreted as real clinical performance measurements.

5. Limitations

The dataset is small and may not represent real-world patient pathways. Journey duration measures the elapsed time between the first and last recorded event, not necessarily actual waiting time.

6. Conclusion

The project demonstrates how Python and pandas can summarize patient pathways and support further process-mining analysis.

7. Next Steps

- Validate dataset quality and timestamps.
- Investigate waiting times between consecutive activities.
- Visualize patient journeys.
- Document findings and upload the final project files to GitHub.

8. Elapsed Time Analysis
### Methodology

Patient elapsed time was calculated as the difference
between the first and last recorded event timestamps
for each patient.

### Interpretation

Elapsed time represents the total duration of the
observed patient journey. It includes both activity
time and waiting time between recorded events.

Longer journeys should be investigated alongside
activity-level waiting-time analysis to identify
potential bottlenecks.

### Limitations

The results depend on the completeness and accuracy
of event timestamps. Patients with only one recorded
event have an elapsed time of zero and may represent
incomplete journeys.
Objective

Compare the elapsed time between the first and last recorded clinical events for each patient case.

Results

Patient Case| Number of Events| Elapsed Time (Minutes)
P001| 5| 180
P002| 4| 155
P003| 5| 210
Mean| —| 181.67
The elapsed-time analysis processed 3 patient journeys.

- Median elapsed time: 120 minutes.
- 75th percentile elapsed time: 137.5 minutes.
- Maximum elapsed time: 155 minutes.

Elapsed time was calculated as the difference between
the first and last recorded event timestamps for each
patient. These results are preliminary because the
dataset contains only three patient journeys.

Key Findings

- P001 had an elapsed time of 180 minutes (3 hours).
- P002 had the shortest elapsed time at 155 minutes (2 hours 35 minutes).
- P003 had the longest elapsed time at 210 minutes (3 hours 30 minutes).
- The difference between the longest and shortest elapsed times was 55 minutes.

Methodology

Elapsed time was calculated by subtracting the first recorded timestamp from the last recorded timestamp for each case. Events were grouped by "case_id" and ordered using their timestamps.

Limitations

- The dataset contains only three patient cases, so the results are preliminary.
- Elapsed time is not the same as waiting time; it can include consultations, laboratory activities, and other care processes.
- Further validation is needed to determine whether recorded time gaps represent actual waiting periods or other intervals.

Next Steps

- Validate timestamps and event sequences.
- Investigate time gaps between consecutive activities.
- Compare patient pathways and identify potential bottlenecks.
- Update visualizations and document findings for the final project presentation.

Elapsed-Time Analysis

Objective

Measure the total elapsed time between the first and last recorded events for each patient.

Method

Events were grouped by patient and ordered by timestamp. Elapsed time was calculated as the difference between the first and last recorded timestamps.

Results

The current dataset contains three patient journeys:

- P001: 120 minutes (2 hours)
- P002: 155 minutes (2 hours 35 minutes)
- P003: 75 minutes (1 hour 15 minutes)

The longest recorded journey was P002, at 155 minutes. The shortest was P003, at 75 minutes.

Interpretation

Elapsed time represents the overall recorded journey duration, not waiting time alone. The activity-transition chart can help identify transitions that warrant further investigation.

Limitations

The analysis includes only three patient journeys. Results are preliminary and may not represent typical hospital performance. Timestamp accuracy, missing events, and differences in patient pathways may affect the results.

Next Steps

- Validate event timestamps and sequences.
- Investigate long gaps between consecutive activities.
- Compare elapsed time across a larger dataset.
- Document findings and update project visualizations.
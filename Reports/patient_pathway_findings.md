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

Objective

Compare the elapsed time between the first and last recorded clinical events for each patient case.

Results

Patient Case| Number of Events| Elapsed Time (Minutes)
P001| 5| 180
P002| 4| 155
P003| 5| 210
Mean| —| 181.67

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
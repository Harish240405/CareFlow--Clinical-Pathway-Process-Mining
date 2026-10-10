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
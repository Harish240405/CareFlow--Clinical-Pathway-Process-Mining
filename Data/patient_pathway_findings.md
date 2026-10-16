CareFlow – Patient Pathway Findings

1. Project Overview

CareFlow is a Python-based project that analyzes patient event logs to understand patient journey durations, activity transitions, and potential workflow bottlenecks.

The Week 2 analysis uses a small synthetic dataset of patient activities and timestamps.

2. Dataset and Validation

- Total event records: 13
- Patient cases analyzed: 3
- Required columns: case_id, activity, timestamp
- Missing values detected: 0
- Duplicate rows detected: 0
- Invalid timestamps detected: 0
- Duplicate events detected: 0

The event log passed the validation checks performed by the current validation script.

3. Patient Elapsed-Time Analysis

The elapsed-time analysis calculates the time between each patient's first recorded event and last recorded event.

Patient Case| Events| Elapsed Time
P001| 5| 120 minutes
P002| 4| 155 minutes
P003| 4| 75 minutes

Summary

- Average elapsed time: 116.67 minutes
- Median elapsed time: 120 minutes
- Shortest journey: 75 minutes
- Longest journey: 155 minutes
- Difference between longest and shortest journeys: 80 minutes

P002 had the longest recorded journey, while P003 had the shortest.

4. Activity Transition Analysis

The waiting-time comparison identified the following transitions:

Activity Transition| Average Minutes| Median Minutes| Maximum Minutes| Cases
Lab Test → Discharge| 120.00| 120| 150| 2
Triage → Doctor Consultation| 46.67| 40| 70| 3
Doctor Consultation → Discharge| 45.00| 45| 45| 1
Registration → Triage| 25.00| 20| 40| 3
Doctor Consultation → Lab Test| 22.50| 22.5| 30| 2

Lab Test → Discharge has the highest observed average transition time at 120 minutes.

Triage → Doctor Consultation also warrants investigation, with an average transition time of approximately 46.67 minutes.

These transition times represent elapsed time between recorded activities and do not necessarily measure actual waiting time.

5. Visualizations and Output Files

The following project outputs have been generated:

- "waiting_time_comparison.png" – comparison of activity transition times
- "waiting_time_summary.csv" – summary statistics for activity transitions
- "patient_elapsed_times.csv" – elapsed-time results for individual patient cases
- "waiting_time_findings.txt" – waiting-time findings report

6. Recommendations

1. Investigate the Lab Test → Discharge transition to understand the time between these recorded activities.
2. Review the Triage → Doctor Consultation transition for possible workflow delays.
3. Check timestamp accuracy and event ordering.
4. Collect additional patient cases to improve the reliability of the analysis.
5. Compare total journey durations with activity-level transition times.
6. Integrate the verified results into the CareFlow dashboard.

7. Limitations

The current dataset contains only three patient cases and is synthetic. Some activity transitions are based on only one or two cases.

The results are preliminary and should not be used to draw conclusions about actual hospital performance. Further analysis with a larger, representative dataset is required.

8. Week 2 Conclusion

The CareFlow Week 2 work successfully validates the event log, calculates patient elapsed times, compares activity transitions, generates visualizations, and documents potential workflow bottlenecks.

The results demonstrate how Python and process-mining techniques can support the analysis of patient pathways. Further validation and a larger dataset will be needed to establish reliable operational insights.

Project Status: Week 2 elapsed-time analysis and waiting-time comparison completed.
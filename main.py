import csv
from pathlib import Path

# Create the output folder
output_dir = Path("Data") / "raw"
output_dir.mkdir(parents=True, exist_ok=True)

# Fictional hospital patient event data
events = [
    ["case_id", "activity", "timestamp", "resource"],
    ["P001", "Registration", "2026-10-01 09:00:00", "Reception"],
    ["P001", "Triage", "2026-10-01 09:20:00", "Nurse"],
    ["P001", "Doctor Consultation", "2026-10-01 10:00:00", "Doctor"],
    ["P001", "Lab Test", "2026-10-01 10:30:00", "Lab"],
    ["P001", "Discharge", "2026-10-01 12:00:00", "Reception"],
    ["P002", "Registration", "2026-10-01 09:10:00", "Reception"],
    ["P002", "Triage", "2026-10-01 09:50:00", "Nurse"],
    ["P002", "Doctor Consultation", "2026-10-01 11:00:00", "Doctor"],
    ["P002", "Discharge", "2026-10-01 11:45:00", "Reception"],
    ["P003", "Registration", "2026-10-01 10:00:00", "Reception"],
    ["P003", "Triage", "2026-10-01 10:15:00", "Nurse"],
    ["P003", "Doctor Consultation", "2026-10-01 10:45:00", "Doctor"],
    ["P003", "Lab Test", "2026-10-01 11:00:00", "Lab"],
    ["P003", "Discharge", "2026-10-01 13:30:00", "Reception"],
]

output_file = output_dir / "patient_event_log.csv"

with output_file.open("w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(events)

print("Patient event log created successfully!")
print(f"Saved to: {output_file}")
print(f"Total events: {len(events) - 1}")
print(f"Total patients: {len(set(row[0] for row in events[1:]))}")

import pandas as pd
from pathlib import Path

# Load the original event log
input_file = Path("Data/raw/patient_event_log.csv")
output_file = Path("Data/processed/patient_event_log_processed.csv")

df = pd.read_csv(input_file)
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Sort events for each patient
df = df.sort_values(["case_id", "timestamp"]).copy()

# Calculate time gaps in minutes
df["time_gap_minutes"] = (
    df.groupby("case_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

# Save processed data
output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

print("Processed event log saved successfully!")
print(f"Output file: {output_file}")
print(f"Total events: {len(df)}")
print(f"Total patients: {df['case_id'].nunique()}")
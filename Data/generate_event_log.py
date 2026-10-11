import random
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd

random.seed(42)

NUM_PATIENTS = 500
START_DATE = datetime(2026, 9, 1, 8, 0)

output_file = Path(__file__).parent / "synthetic_event_log.csv"

triage_levels = ["Critical", "High", "Medium", "Low"]
triage_weights = [5, 20, 45, 30]

wait_ranges = {
    "Critical": (0, 5),
    "High": (3, 20),
    "Medium": (10, 60),
    "Low": (20, 120),
}

records = []

for i in range(1, NUM_PATIENTS + 1):
    patient_id = f"P{i:04d}"

    current_time = START_DATE + timedelta(
        minutes=random.randint(0, 30 * 24 * 60)
    )

    triage = random.choices(
        triage_levels, weights=triage_weights, k=1
    )[0]

    def add_event(activity, department):
        records.append({
            "case_id": patient_id,
            "timestamp": current_time,
            "activity": activity,
            "department": department,
            "triage_level": triage,
        })

    add_event("Patient Arrival", "Emergency")

    current_time += timedelta(minutes=random.randint(2, 15))
    add_event("Registration", "Reception")

    current_time += timedelta(minutes=random.randint(3, 12))
    add_event("Triage", "Emergency")

    low, high = wait_ranges[triage]
    current_time += timedelta(minutes=random.randint(low, high))
    add_event("Doctor Consultation", "Emergency")

    if random.random() < 0.70:
        current_time += timedelta(minutes=random.randint(5, 20))
        add_event("Lab Test Ordered", "Emergency")

        current_time += timedelta(minutes=random.randint(5, 35))
        add_event("Sample Collected", "Laboratory")

        current_time += timedelta(minutes=random.randint(15, 90))
        add_event("Lab Results Available", "Laboratory")

        current_time += timedelta(minutes=random.randint(5, 25))
        add_event("Results Reviewed", "Emergency")

    current_time += timedelta(minutes=random.randint(5, 30))
    add_event("Treatment", "Emergency")

    current_time += timedelta(minutes=random.randint(10, 60))

    if random.random() < 0.20:
        add_event("Admission", "Inpatient")
    else:
        add_event("Discharge", "Emergency")

df = pd.DataFrame(records)
df = df.sort_values(["case_id", "timestamp"])
df["event_number"] = df.groupby("case_id").cumcount() + 1

df = df[
    [
        "case_id",
        "event_number",
        "timestamp",
        "activity",
        "department",
        "triage_level",
    ]
]

df.to_csv(output_file, index=False)

print("Synthetic event log generated successfully!")
print("Patients:", df["case_id"].nunique())
print("Total events:", len(df))
print("Saved to:", output_file)
print(df.head(10).to_string(index=False))
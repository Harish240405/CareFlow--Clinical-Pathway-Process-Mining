import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "patient_events.csv"
OUTPUT_FILE = DATA_DIR / "patient_elapsed_times.csv"

# Read the CSV as three columns, even if it has no header row.
df = pd.read_csv(
    INPUT_FILE,
    header=None,
    names=["patient_id", "activity", "timestamp"]
)

# If the file has a header row, remove it from the data.
if str(df.iloc[0]["patient_id"]).strip().lower() in {
    "patient_id", "patient", "patientid"
}:
    df = df.iloc[1:].copy()

df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce"
)

df = df.dropna(subset=["patient_id", "timestamp"])
df["patient_id"] = df["patient_id"].astype(str).str.strip()

# Sort events by patient and time.
df = df.sort_values(["patient_id", "timestamp"])

# Calculate elapsed time from first event to last event.
elapsed = (
    df.groupby("patient_id")
    .agg(
        first_event=("timestamp", "min"),
        last_event=("timestamp", "max"),
        event_count=("activity", "count")
    )
    .reset_index()
)

elapsed["elapsed_minutes"] = (
    elapsed["last_event"] - elapsed["first_event"]
).dt.total_seconds() / 60

elapsed["elapsed_hours"] = elapsed["elapsed_minutes"] / 60

elapsed.to_csv(OUTPUT_FILE, index=False)

print("\nElapsed Time Summary (minutes)")
print(elapsed["elapsed_minutes"].describe().round(2))

print(f"\nPatient journeys analyzed: {len(elapsed)}")
print(f"Results saved to: {OUTPUT_FILE}")
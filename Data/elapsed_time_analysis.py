import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "patient_events.csv"
OUTPUT_FILE = DATA_DIR / "patient_elapsed_times.csv"

# Load the original event log with its correct column names.
df = pd.read_csv(INPUT_FILE)

required_columns = {"case_id", "activity", "timestamp"}
if not required_columns.issubset(df.columns):
    raise ValueError(
        f"Missing required columns: {required_columns - set(df.columns)}"
    )

# Parse timestamps consistently.
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    format="%Y-%m-%d %H:%M:%S",
    errors="coerce"
)

# Remove records without a valid case ID or timestamp.
df["case_id"] = df["case_id"].astype("string").str.strip()
df["activity"] = df["activity"].astype("string").str.strip()
df = df.dropna(subset=["case_id", "activity", "timestamp"])
df = df[
    df["case_id"].ne("") & df["activity"].ne("")
].copy()

# Sort events chronologically for each patient case.
df = df.sort_values(["case_id", "timestamp"])

# Calculate total elapsed time per case.
elapsed = (
    df.groupby("case_id")
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
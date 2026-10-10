from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "Data" / "patient_events.csv"

# Load dataset
if not DATA_FILE.exists():
    print("ERROR: Dataset not found!")
    print(f"Expected file: {DATA_FILE}")
    raise SystemExit(1)

df = pd.read_csv(DATA_FILE)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Validate required columns
required_columns = {"case_id", "activity", "timestamp"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    print("ERROR: Missing columns:", missing_columns)
    print("Available columns:", list(df.columns))
    raise SystemExit(1)

# Clean data
df["case_id"] = df["case_id"].astype(str).str.strip()
df["activity"] = df["activity"].astype(str).str.strip()
df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce"
)

df = df.dropna(subset=["timestamp"])
df = df.sort_values(["case_id", "timestamp"])

# Summary
print("\n=== CAREFLOW PATHWAY ANALYSIS ===")
print(f"Total events: {len(df)}")
print(f"Unique patients: {df['case_id'].nunique()}")

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

# Activity frequencies
print("\n=== ACTIVITY FREQUENCIES ===")
print(df["activity"].value_counts())

# Patient pathways
print("\n=== PATIENT PATHWAYS ===")
for patient_id, group in df.groupby("case_id"):
    activities = group["activity"].tolist()
    print(f"{patient_id}: {' -> '.join(activities)}")

# Events per patient
print("\n=== PATIENT EVENT COUNTS ===")
print(df.groupby("case_id").size())

# Journey duration
print("\n=== PATIENT JOURNEY DURATIONS ===")

journey = df.groupby("case_id").agg(
    start_time=("timestamp", "min"),
    end_time=("timestamp", "max"),
    event_count=("activity", "size")
)

journey["duration_minutes"] = (
    journey["end_time"] - journey["start_time"]
).dt.total_seconds() / 60

print(journey)

print(
    "\nAverage journey duration (minutes):",
    round(journey["duration_minutes"].mean(), 2)
)

print("\n=== ANALYSIS COMPLETED ===")
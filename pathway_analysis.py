from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "Data"
DATA_FILE = DATA_DIR / "synthetic_event_log.csv"
# Load dataset
if not DATA_FILE.exists():
    raise SystemExit(f"ERROR: Dataset not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip().str.lower()

# Validate required columns
required_columns = {"case_id", "activity", "timestamp"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    raise SystemExit(
        f"ERROR: Missing columns: {sorted(missing_columns)}\n"
        f"Available columns: {list(df.columns)}"
    )

# Preserve original row numbers for data-quality reporting
df["source_row"] = df.index + 2

# Clean text fields
for col in ["case_id", "activity"]:
    df[col] = df[col].astype("string").str.strip()
    df[col] = df[col].replace("", pd.NA)

# Validate timestamps
df["timestamp"] = pd.to_datetime(
    df["timestamp"], errors="coerce"
)

invalid_timestamps = df["timestamp"].isna().sum()
missing_required = df[
    ["case_id", "activity"]
].isna().any(axis=1).sum()

print("\n=== CAREFLOW PATHWAY ANALYSIS ===")
print(f"Input records: {len(df)}")
print(f"Invalid or missing timestamps: {invalid_timestamps}")
print(f"Records missing case ID or activity: {missing_required}")
print(f"Duplicate rows: {df.duplicated(
    subset=['case_id', 'activity', 'timestamp']
).sum()}")

# Exclude invalid records from time-based analysis
valid = df.dropna(
    subset=["case_id", "activity", "timestamp"]
).copy()

valid = valid.sort_values(
    ["case_id", "timestamp", "source_row"]
)

print(f"\nValid events analyzed: {len(valid)}")
print(f"Unique patients: {valid['case_id'].nunique()}")
print(f"Unique activities: {valid['activity'].nunique()}")

# Missing-value report
print("\n=== MISSING VALUES IN INPUT ===")
print(df[["case_id", "activity", "timestamp"]].isna().sum())

# Activity frequencies
activity_counts = (
    valid["activity"]
    .value_counts()
    .rename_axis("activity")
    .reset_index(name="event_count")
)

print("\n=== ACTIVITY FREQUENCIES ===")
print(activity_counts.to_string(index=False))

activity_counts.to_csv(
    DATA_DIR / "pathway_activity_frequencies.csv",
    index=False
)

# Patient pathways
print("\n=== PATIENT PATHWAYS ===")
for case_id, group in valid.groupby("case_id", sort=True):
    activities = group["activity"].tolist()
    print(f"{case_id}: {' -> '.join(activities)}")

# Events per patient
print("\n=== PATIENT EVENT COUNTS ===")
event_counts = (
    valid.groupby("case_id")
    .size()
    .rename("event_count")
    .reset_index()
)
print(event_counts.to_string(index=False))

# Journey duration
print("\n=== PATIENT JOURNEY DURATIONS ===")
journey = valid.groupby("case_id").agg(
    first_event=("timestamp", "min"),
    last_event=("timestamp", "max"),
    event_count=("activity", "size")
)

journey["elapsed_minutes"] = (
    journey["last_event"] - journey["first_event"]
).dt.total_seconds() / 60

print(journey.to_string())

journey.reset_index().to_csv(
    DATA_DIR / "pathway_journey_summary.csv",
    index=False
)

if not journey.empty:
    print(
        "\nAverage journey duration (minutes):",
        round(journey["elapsed_minutes"].mean(), 2)
    )
    print(
        "Longest journey (minutes):",
        round(journey["elapsed_minutes"].max(), 2)
    )
    print(
        "Shortest journey (minutes):",
        round(journey["elapsed_minutes"].min(), 2)
    )

# Activity transitions within each patient journey
print("\n=== ACTIVITY TRANSITIONS ===")
valid["next_activity"] = (
    valid.groupby("case_id")["activity"].shift(-1)
)
valid["next_timestamp"] = (
    valid.groupby("case_id")["timestamp"].shift(-1)
)

transitions = valid.dropna(
    subset=["next_activity", "next_timestamp"]
).copy()

transitions["waiting_minutes"] = (
    transitions["next_timestamp"] - transitions["timestamp"]
).dt.total_seconds() / 60

transitions = transitions.rename(
    columns={"activity": "previous_activity"}
)

transition_summary = (
    transitions.groupby(
        ["previous_activity", "next_activity"],
        as_index=False
    )
    .agg(
        transition_count=("waiting_minutes", "size"),
        average_minutes=("waiting_minutes", "mean"),
        median_minutes=("waiting_minutes", "median"),
        maximum_minutes=("waiting_minutes", "max")
    )
    .sort_values("average_minutes", ascending=False)
)

if transition_summary.empty:
    print("No consecutive activity transitions found.")
else:
    print(transition_summary.to_string(index=False))

transition_summary.to_csv(
    DATA_DIR / "pathway_transition_summary.csv",
    index=False
)

print("\nSaved analysis files:")
print("- Data/pathway_activity_frequencies.csv")
print("- Data/pathway_journey_summary.csv")
print("- Data/pathway_transition_summary.csv")
print("\n=== ANALYSIS COMPLETED ===")
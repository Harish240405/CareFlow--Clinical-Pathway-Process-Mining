import pandas as pd

file_path = "Data/processed/patient_event_log_processed.csv"
df = pd.read_csv(file_path)

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df = df.dropna(subset=["case_id", "activity", "timestamp"])

df = df.sort_values(["case_id", "timestamp"])

print("\n=== Patient Pathways ===")

for patient_id, group in df.groupby("case_id"):
    activities = group["activity"].tolist()
    print(f"{patient_id}: {' -> '.join(activities)}")

print("\n=== Patient Event Counts ===")
print(df.groupby("case_id").size())

print("\n=== Activity Frequencies ===")
print(df["activity"].value_counts())

# Patient-level event counts
print("\n=== Patient Event Counts ===")
print(df.groupby("case_id").size())

# Activity frequencies
print("\n=== Activity Frequencies ===")
print(df["activity"].value_counts())

# Total events and unique patients
print("\n=== Summary ===")
print(f"Total events: {len(df)}")
print(f"Unique patients: {df['case_id'].nunique()}")

# Check missing values
print("\n=== Missing Values ===")
print(df.isnull().sum())

print("\n=== Events With Missing Time Gaps ===")
print(
    df[df["time_gap_minutes"].isna()][
        ["case_id", "activity", "timestamp", "time_gap_minutes"]
    ]
)

# Calculate patient journey duration
print("\n=== Patient Journey Duration ===")

df["timestamp"] = pd.to_datetime(df["timestamp"])

journey = (
    df.groupby("case_id")["timestamp"]
    .agg(start_time="min", end_time="max")
)

journey["duration_minutes"] = (
    journey["end_time"] - journey["start_time"]
).dt.total_seconds() / 60

print(journey)
print("\nAverage journey duration (minutes):")
print(journey["duration_minutes"].mean())

# Analyze waiting times between consecutive activities
print("\n=== Longest Waiting Times ===")

df = df.sort_values(["case_id", "timestamp"]).copy()

df["waiting_minutes"] = (
    df.groupby("case_id")["timestamp"]
    .diff()
    .dt.total_seconds() / 60
)

print(
    df[["case_id", "activity", "waiting_minutes"]]
    .sort_values("waiting_minutes", ascending=False)
    .head(10)
    .to_string(index=False)
)


from pathlib import Path
import pandas as pd

# Locate the Data folder
DATA_DIR = Path(__file__).resolve().parent

# Load the event log
input_file = DATA_DIR / "raw" / "patient_event_log.csv"
df = pd.read_csv(input_file, parse_dates=["timestamp"])

# Sort events in chronological order for each patient
df = df.sort_values(["case_id", "timestamp"]).copy()

# Get the previous activity and timestamp for each patient
df["previous_activity"] = (
    df.groupby("case_id")["activity"].shift(1)
)

df["previous_timestamp"] = (
    df.groupby("case_id")["timestamp"].shift(1)
)

# Calculate elapsed time between consecutive activities
df["time_minutes"] = (
    df["timestamp"] - df["previous_timestamp"]
).dt.total_seconds() / 60

# Remove first events, which have no previous activity
waiting = df.dropna(
    subset=["previous_activity", "time_minutes"]
).copy()

# Summarize time by activity transition
summary = (
    waiting.groupby(
        ["previous_activity", "activity"],
        as_index=False
    )
    .agg(
        average_minutes=("time_minutes", "mean"),
        median_minutes=("time_minutes", "median"),
        maximum_minutes=("time_minutes", "max"),
        number_of_cases=("case_id", "nunique")
    )
    .sort_values("average_minutes", ascending=False)
)

# Save detailed and summarized results
waiting.to_csv(
    DATA_DIR / "patient_waiting_times.csv",
    index=False
)

summary.to_csv(
    DATA_DIR / "waiting_time_summary.csv",
    index=False
)

print("\n=== Longest Average Time Between Activities ===")
print(summary.head(10).to_string(index=False))

print("\nFiles saved:")
print("patient_waiting_times.csv")
print("waiting_time_summary.csv")
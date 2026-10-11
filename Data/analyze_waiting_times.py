from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
input_file = DATA_DIR / "synthetic_event_log.csv"

df = pd.read_csv(input_file, parse_dates=["timestamp"])
df = df.sort_values(["case_id", "timestamp"])

# Calculate time between consecutive events for each patient
df["previous_activity"] = (
    df.groupby("case_id")["activity"].shift(1)
)

df["previous_timestamp"] = (
    df.groupby("case_id")["timestamp"].shift(1)
)

df["time_minutes"] = (
    df["timestamp"] - df["previous_timestamp"]
).dt.total_seconds() / 60

# Save the detailed waiting-time analysis
waits = df.dropna(subset=["time_minutes"]).copy()

waits.to_csv(
    DATA_DIR / "patient_waiting_times.csv",
    index=False
)

# Summarize time between activities
summary = (
    waits.groupby(
        ["previous_activity", "activity"]
    )["time_minutes"]
    .agg(["count", "mean", "median", "max"])
    .round(2)
    .sort_values("mean", ascending=False)
)

summary.to_csv(DATA_DIR / "waiting_time_summary.csv")

print("\n=== Longest Average Time Between Activities ===")
print(summary.head(10).to_string())

print("\nFiles saved:")
print("patient_waiting_times.csv")
print("waiting_time_summary.csv")
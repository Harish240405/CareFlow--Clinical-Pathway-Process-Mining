from pathlib import Path
import pandas as pd
import pm4py

# Project paths
DATA_DIR = Path(__file__).resolve().parent
INPUT_FILE = DATA_DIR / "synthetic_event_log.csv"
OUTPUT_FILE = DATA_DIR / "patient_process_map.png"

# Load the event log
df = pd.read_csv(INPUT_FILE)

print("Columns found:", df.columns.tolist())
print("Total events:", len(df))

# Standardize column names
df.columns = [col.strip().lower() for col in df.columns]

# Map common column names to PM4Py format
column_map = {
    "case_id": "case:concept:name",
    "patient_id": "case:concept:name",
    "activity": "concept:name",
    "activity_name": "concept:name",
    "timestamp": "time:timestamp",
    "event_timestamp": "time:timestamp",
}

df = df.rename(columns=column_map)

required = [
    "case:concept:name",
    "concept:name",
    "time:timestamp",
]

missing = [col for col in required if col not in df.columns]
if missing:
    raise ValueError(
        f"Missing required columns: {missing}. "
        f"Review the column names printed above."
    )

# Normalize timestamps and sort events
df["time:timestamp"] = pd.to_datetime(
    df["time:timestamp"], errors="coerce"
)

if df["time:timestamp"].isna().any():
    raise ValueError("Some timestamps could not be parsed.")

df = df.sort_values(
    ["case:concept:name", "time:timestamp"]
)

# Discover the process model
event_log = pm4py.convert_to_event_log(df)

process_tree = pm4py.discover_process_tree_inductive(event_log)

# Save a process visualization
pm4py.save_vis_process_tree(
    process_tree,
    str(OUTPUT_FILE)
)

print("\nProcess discovery completed!")
print("Patient cases:", df["case:concept:name"].nunique())
print("Activities:", df["concept:name"].nunique())
print("Process map saved to:", OUTPUT_FILE)
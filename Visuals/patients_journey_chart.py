from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    PROJECT_DIR
    / "Data"
    / "processed"
    / "patient_event_log_processed.csv"
)
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = (
    PROJECT_DIR
    / "Data"
    / "processed"
    / "patient_event_log_processed.csv"
)
OUTPUT_FILE = PROJECT_DIR / "Visuals" / "patients_journey_chart.png"

# Load and prepare data
df = pd.read_csv(INPUT_FILE)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(["case_id", "timestamp"])

# Build a label for each patient activity
df["patient_activity"] = (
    df["activity"] + " - " + df["case_id"]
)

# Select the 10 most frequent patient activities
top_activities = (
    df["patient_activity"]
    .value_counts()
    .head(10)
    .index
)

plot_data = df[df["patient_activity"].isin(top_activities)]

# Plot the journey events chronologically
fig, ax = plt.subplots(figsize=(12, 7))

for case_id, patient in plot_data.groupby("case_id"):
    patient = patient.sort_values("timestamp")
    ax.plot(
        patient["timestamp"],
        patient["activity"],
        marker="o",
        label=case_id
    )

ax.set_title("CareFlow: Patient Journey Timeline")
ax.set_xlabel("Timestamp")
ax.set_ylabel("Patient Activity")
ax.tick_params(axis="x", rotation=30)
ax.grid(True, alpha=0.3)
ax.legend(title="Patient", bbox_to_anchor=(1.02, 1), loc="upper left")
fig.tight_layout()

fig.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
print(f"Chart saved to: {OUTPUT_FILE}")
plt.show()
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print(df.head())
print("Columns:", df.columns.tolist())
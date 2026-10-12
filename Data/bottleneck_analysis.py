from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent

summary_file = DATA_DIR / "waiting_time_summary.csv"
output_file = DATA_DIR / "bottleneck_chart.png"

df = pd.read_csv(summary_file)

df = pd.read_csv(summary_file)

# Create transition labels
df["transition"] = (
    df["previous_activity"].astype(str)
    + " -> "
    + df["activity"].astype(str)
)

# Select the 10 longest transitions
df = df.sort_values(
    "average_minutes",
    ascending=False
).head(10)

# Create chart
plt.figure(figsize=(12, 7))
plt.barh(df["transition"], df["average_minutes"])

plt.xlabel("Average elapsed time (minutes)")
plt.ylabel("Activity transition")
plt.title("CareFlow: Top 10 Longest Activity Transitions")
plt.gca().invert_yaxis()
plt.tight_layout()

# Save chart
plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.show()

print("Chart saved to:", output_file)
print("\nTop 10 longest transitions:")
print(
    df[
        ["transition", "average_minutes",
         "median_minutes", "maximum_minutes"]
    ].to_string(index=False)
)
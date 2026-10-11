from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent

summary_file = DATA_DIR / "waiting_time_summary.csv"
output_file = DATA_DIR / "bottleneck_chart.png"

df = pd.read_csv(summary_file)

# Select the 10 transitions with the highest mean elapsed time
df = df.sort_values("mean", ascending=False).head(10)

df["transition"] = (
    df["previous_activity"].astype(str)
    + " → "
    + df["activity"].astype(str)
)

df = df.sort_values("mean")

plt.figure(figsize=(12, 7))
plt.barh(df["transition"], df["mean"])
plt.xlabel("Average elapsed time (minutes)")
plt.ylabel("Activity transition")
plt.title("CareFlow: Top 10 Longest Activity Transitions")
plt.tight_layout()

plt.savefig(output_file, dpi=300, bbox_inches="tight")
plt.show()

print("Chart saved to:", output_file)
print("\nTransitions with the highest average elapsed time:")
print(df[["transition", "mean", "median", "max"]].to_string(index=False))
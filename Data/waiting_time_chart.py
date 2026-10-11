from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent

# Load the activity transition summary
summary = pd.read_csv(DATA_DIR / "waiting_time_summary.csv")

# Select the 10 transitions with the highest average times
top = summary.nlargest(10, "average_minutes").copy()

# Create readable transition labels
top["transition"] = (
    top["previous_activity"].astype(str)
    + " → "
    + top["activity"].astype(str)
)

# Plot the results
top = top.sort_values("average_minutes")

plt.figure(figsize=(11, 6))
plt.barh(top["transition"], top["average_minutes"])
plt.xlabel("Average elapsed time (minutes)")
plt.ylabel("Activity transition")
plt.title("CareFlow: Top 10 Activity Transitions by Average Time")
plt.tight_layout()

# Save the chart
output_file = DATA_DIR / "waiting_time_chart.png"
plt.savefig(output_file, dpi=150, bbox_inches="tight")
plt.show()

print(f"Chart saved to: {output_file}")
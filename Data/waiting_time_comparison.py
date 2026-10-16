from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent

# Load waiting-time summary
summary = pd.read_csv(DATA_DIR / "waiting_time_summary.csv")

# Select the top 5 transitions by average waiting time
top = summary.nlargest(5, "average_minutes").copy()

# Create readable labels
top["transition"] = (
    top["previous_activity"].astype(str)
    + " -> "
    + top["activity"].astype(str)
)

# Sort for a horizontal bar chart
top = top.sort_values("average_minutes")

# Create second chart
plt.figure(figsize=(11, 6))
plt.barh(top["transition"], top["average_minutes"])
plt.xlabel("Average elapsed time (minutes)")
plt.ylabel("Patient activity transition")
plt.title("CareFlow: Top 5 Patient Waiting-Time Bottlenecks")
plt.tight_layout()

# Save chart
plt.tight_layout()
plt.savefig(DATA_DIR / "waiting_time_comparison.png", dpi=300, bbox_inches="tight")
plt.show()

print(f"Second chart saved to: {DATA_DIR / 'waiting_time_comparison.png'}")
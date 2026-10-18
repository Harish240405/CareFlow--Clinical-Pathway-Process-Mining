from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "Data" / "pathway_transition_summary.csv"

if not DATA_FILE.exists():
    raise SystemExit(f"File not found: {DATA_FILE}")

df = pd.read_csv(DATA_FILE)

if df.empty:
    raise SystemExit("No transition data available to plot.")

top = df.nlargest(10, "average_minutes").copy()

top["transition"] = (
    top["previous_activity"].astype(str)
    + " -> "
    + top["next_activity"].astype(str)
)

top = top.sort_values("average_minutes")

plt.figure(figsize=(10, 6))
plt.barh(top["transition"], top["average_minutes"])
plt.xlabel("Average elapsed time (minutes)")
plt.ylabel("Activity transition")
plt.title("CareFlow: Activity Transition Time Analysis")
plt.tight_layout()

output_file = BASE_DIR / "Data" / "transition_times.png"
plt.savefig(output_file, dpi=150)
plt.show()

print(f"Chart saved to: {output_file}")
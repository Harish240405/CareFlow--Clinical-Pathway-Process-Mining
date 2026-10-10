import matplotlib.pyplot as plt

# Waiting times from the current CareFlow analysis
activities = [
    "Discharge - P003",
    "Discharge - P001",
    "Doctor Consultation - P002",
    "Discharge - P002",
    "Triage - P002"
]

waiting_minutes = [150, 90, 70, 45, 40]

plt.figure(figsize=(10, 6))
plt.barh(activities, waiting_minutes)
plt.xlabel("Waiting Time (minutes)")
plt.ylabel("Patient Activity")
plt.title("CareFlow: Longest Recorded Waiting Times")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("Visuals/waiting_time_chart.png", dpi=300)
plt.show()
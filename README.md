
# CareFlow — Healthcare Process Analytics

**Discover patient pathways, analyze waiting times, and identify workflow bottlenecks using Python and interactive analytics.**

CareFlow is a healthcare operations analytics project that explores how patients move through different hospital activities. It uses synthetic event data to demonstrate process analysis, waiting-time measurement, and interactive dashboard development.

> **Disclaimer:** This project uses synthetic data for educational and demonstration purposes. It does not contain real patient records or provide clinical recommendations.

## Features

- **Patient Journey Analysis:** Explore the sequence of activities for individual patient cases.
- **Activity Frequency Analysis:** Visualize the most frequently recorded activities.
- **Interactive Filters:** Filter event records by department and triage level.
- **Waiting-Time Analysis:** Compare average, median, and maximum waiting times.
- **Bottleneck Identification:** Highlight transitions with longer observed waiting times.
- **Actionable Insights:** Present suggested areas for further operational investigation.
- **Interactive Dashboard:** Explore metrics and visualizations through Streamlit.

## Technology Stack

- Python
- Pandas
- Streamlit
- Plotly
- CSV-based event data
- Git and GitHub

## Project Architecture

```text
Synthetic Event Log
        |
        v
Data Preparation and Validation
        |
        v
Pathway and Waiting-Time Analysis
        |
        v
Summary CSV Files
        |
        v
Streamlit Dashboard
        |
        v
Interactive Charts and Insights
```

## Project Structure

```text
CareFlow_Project/
├── Data/
│   ├── synthetic_event_log.csv
│   ├── pathway_transition_summary.csv
│   ├── pathway_journey_summary.csv
│   ├── pathway_activity_frequencies.csv
│   ├── waiting_time_summary.csv
│   ├── patient_waiting_times.csv
│   ├── bottleneck_summary.csv
│   └── plot_waiting_times.py
├── app.py
├── pathway_analysis.py
├── README.md
└── .gitignore
```

*The file list above describes the main expected project files; adjust it if your actual repository structure differs.*

## Dataset Overview

The current synthetic dataset contains:

- 500 patient cases
- 4,420 recorded events
- 11 unique activities

These figures describe the generated demonstration dataset and may change if the data is regenerated.

## Getting Started

### Prerequisites

- Python installed on your computer
- Git
- A terminal or command prompt

### Installation

Clone the repository:

```bash
git clone https://github.com/Harish240405/CareFlow--Clinical-Pathway-Process-Mining.git
cd CareFlow--Clinical-Pathway-Process-Mining
```

Create and activate a virtual environment:

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required libraries:

```bash
pip install streamlit pandas plotly
```

Run the analysis script:

```bash
python pathway_analysis.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal.

## Analytical Workflow

1. Load the synthetic event log.
2. Organize activities by patient case and event order.
3. Calculate activity frequencies and pathway transitions.
4. Summarize waiting times and journey durations.
5. Identify transitions that warrant further investigation.
6. Explore the outputs through the interactive dashboard.

## Project Goals

- Apply practical Python data analysis techniques.
- Understand event logs and patient process pathways.
- Explore operational waiting-time patterns.
- Develop interactive visualizations and dashboard filters.
- Communicate analytical findings clearly.

## Limitations

- The dataset is synthetic and may not reflect real hospital operations.
- Longer waiting times indicate areas for investigation, not necessarily confirmed causes.
- Dashboard filters currently affect the event records they are connected to; not every existing metric or chart necessarily responds to every filter.
- Findings should not be interpreted as validated clinical or operational recommendations.

## Author

**Harish Nimaje**

GitHub: [Harish240405](https://github.com/Harish240405)

## 📄 License

No license has been specified yet. Add an appropriate license if you intend to permit others to reuse or modify this project.

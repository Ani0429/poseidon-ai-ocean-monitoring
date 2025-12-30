import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load reference data (historical)
reference = pd.read_csv("data/processed/oxygen_features.csv")

# Simulate current data with small shift
current = reference.sample(frac=0.7, random_state=42).copy()
current["o2"] = current["o2"] * 0.97   # simulate oxygen drop
current["nppv"] = current["nppv"] * 1.05

# Create drift report
report = Report(metrics=[DataDriftPreset()])
report.run(
    reference_data=reference,
    current_data=current
)

# Save report
report.save_html("reports/oxygen_data_drift_report.html")

print("✅ Oxygen data drift report generated")

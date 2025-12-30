import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load reference (historical) data
reference = pd.read_csv("data/processed/ph_features.csv")

# Simulate current data (slight shift)
current = reference.sample(frac=0.7, random_state=42).copy()
current["ph_value"] = current["ph_value"] + 0.02  # simulate drift

# Create Evidently report
report = Report(metrics=[DataDriftPreset()])
report.run(
    reference_data=reference,
    current_data=current
)

# Save report
report.save_html("reports/ph_data_drift_report.html")

print("✅ pH data drift report generated")

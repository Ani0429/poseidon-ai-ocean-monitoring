import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load SST feature data
reference = pd.read_csv("data/processed/sst_features.csv")

# Simulate new incoming batch
current = reference.sample(frac=0.7, random_state=42)

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)

report.save_html("reports/sst_data_drift_report.html")

print("✅ SST drift report generated")

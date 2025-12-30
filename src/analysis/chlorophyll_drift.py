import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Reference = older data
reference = pd.read_csv("data/processed/modis_chlorophyll_features.csv")

# Simulated current data
current = reference.sample(frac=0.7, random_state=42)

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)

report.save_html("reports/chlorophyll_data_drift_report.html")
print("✅ Chlorophyll drift report generated")

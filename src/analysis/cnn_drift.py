import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

reference = pd.read_csv("data/processed/cnn_features_pca.csv")
current = reference.sample(frac=0.7, random_state=42)

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)

report.save_html("reports/cnn_data_drift_report.html")
print("✅ CNN PCA drift report generated")

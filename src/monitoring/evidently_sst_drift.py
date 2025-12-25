import xarray as xr
import pandas as pd
import os

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

# Load processed SST dataset
ds = xr.open_dataset("data/processed/bay_of_bengal_sst_20231019.nc")

# Convert SST to 1D array
sst_values = ds.to_array().values.flatten()
sst_values = sst_values[~pd.isna(sst_values)]

# Current data
current_df = pd.DataFrame({"sst": sst_values})

# Reference data (simulated historical baseline)
reference_df = current_df.copy()
reference_df["sst"] = reference_df["sst"] - 0.5

# Create Evidently report
report = Report(metrics=[DataDriftPreset()])

# Run drift detection
report.run(
    reference_data=reference_df,
    current_data=current_df
)

# Save HTML report
os.makedirs("reports", exist_ok=True)
report.save_html("reports/sst_data_drift_report.html")

print("✅ Evidently SST data drift report generated successfully")


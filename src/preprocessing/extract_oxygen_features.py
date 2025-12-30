import xarray as xr
import pandas as pd

# Load processed oxygen dataset
ds = xr.open_dataset("data/processed/oxygen_npp_bob_202311_processed.nc")

# Convert to DataFrame
df = ds.to_dataframe().reset_index()

# Keep only useful columns
df = df[["o2", "nppv"]].dropna()

# Save features
output_path = "data/processed/oxygen_features.csv"
df.to_csv(output_path, index=False)

print("✅ Oxygen features extracted to", output_path)

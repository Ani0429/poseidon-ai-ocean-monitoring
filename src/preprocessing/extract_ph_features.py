import xarray as xr
import pandas as pd
import numpy as np

# Load processed pH NetCDF
ds = xr.open_dataset("data/processed/ph_bob_202311_processed.nc")

# Get variable name automatically
ph_var = list(ds.data_vars)[0]
ph_data = ds[ph_var].values.flatten()

# Remove NaNs
ph_data = ph_data[~np.isnan(ph_data)]

# Create feature dataframe
df = pd.DataFrame({
    "ph_value": ph_data
})

# Save CSV
df.to_csv("data/processed/ph_features.csv", index=False)

print("✅ pH features extracted to data/processed/ph_features.csv")

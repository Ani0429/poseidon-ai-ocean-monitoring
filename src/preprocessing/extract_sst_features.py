import xarray as xr
import pandas as pd
import numpy as np
from pathlib import Path

# Input SST NetCDF files
sst_files = [
    "data/processed/bay_of_bengal_sst_20231019.nc",
    "data/processed/bay_of_bengal_sst_20231021.nc"
]

rows = []

for file in sst_files:
    ds = xr.open_dataset(file)
    sst = ds[list(ds.data_vars)[0]].values

    rows.append({
        "mean_sst": np.nanmean(sst),
        "std_sst": np.nanstd(sst),
        "min_sst": np.nanmin(sst),
        "max_sst": np.nanmax(sst),
        "source": Path(file).name
    })

df = pd.DataFrame(rows)

output_path = "data/processed/sst_features.csv"
df.to_csv(output_path, index=False)

print("✅ SST features saved to", output_path)

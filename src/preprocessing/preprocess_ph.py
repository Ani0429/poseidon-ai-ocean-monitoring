#!/usr/bin/env python3
"""
Preprocess pH dataset for Project Poseidon
- Extract surface pH
- Remove depth dimension
- Save clean NetCDF for ML & frontend
"""

import xarray as xr
from pathlib import Path

RAW_FILE = "data/raw/ph_bob_202311.nc"
OUT_FILE = "data/processed/ph_bob_202311_processed.nc"

def main():
    print("⚗️ Loading raw pH dataset...")
    ds = xr.open_dataset(RAW_FILE)

    # Select surface depth
    ds = ds.sel(depth=ds.depth.values[0])

    # Keep only relevant variables
    ds_out = ds[["ph", "dissic", "talk"]]

    # Save
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    ds_out.to_netcdf(OUT_FILE)

    print(f"✅ Saved processed pH file: {OUT_FILE}")
    print("📊 Variables:", list(ds_out.data_vars))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Preprocess Oxygen + NPP dataset for Poseidon
- Surface only
- Bay of Bengal
- ML-ready NetCDF
"""

import xarray as xr
from pathlib import Path

RAW_PATH = "data/raw/oxygen_npp_bob_202311.nc"
OUT_PATH = "data/processed/oxygen_npp_bob_202311_processed.nc"

def main():
    print("🫁 Loading Oxygen + NPP dataset...")
    ds = xr.open_dataset(RAW_PATH)

    # Select surface
    if "depth" in ds.dims:
        ds = ds.sel(depth=ds.depth.values[0])

    # Keep only required variables
    ds = ds[["o2", "nppv"]]

    # Drop missing values safely
    ds = ds.dropna(dim="time", how="all")

    Path("data/processed").mkdir(exist_ok=True, parents=True)
    ds.to_netcdf(OUT_PATH)

    print("✅ Saved processed file:", OUT_PATH)
    print("📊 Variables:", list(ds.data_vars))

if __name__ == "__main__":
    main()

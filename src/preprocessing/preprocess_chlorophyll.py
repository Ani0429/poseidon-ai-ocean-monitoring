#!/usr/bin/env python3
"""
Project Poseidon
Preprocess Chlorophyll-a & Phytoplankton Carbon (CMEMS BGC)

- Input : Raw CMEMS subset NetCDF
- Output: Clean surface-only NetCDF for ML
"""

import xarray as xr
from pathlib import Path

RAW_FILE = Path("data/raw/chlorophyll_phyc_bob_202311.nc")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_FILE = OUT_DIR / "chlorophyll_phyc_bob_202311_processed.nc"


def main():
    print("🌱 Loading chlorophyll dataset...")
    ds = xr.open_dataset(RAW_FILE)

    # Select surface only (depth = 0.49 m)
    if "depth" in ds.dims:
        ds = ds.isel(depth=0)

    # Keep only required variables
    required_vars = ["chl", "phyc"]
    ds = ds[required_vars]

    # Rename coordinates for consistency
    ds = ds.rename({
        "latitude": "lat",
        "longitude": "lon"
    })

    # Add units metadata (helps in reports)
    ds["chl"].attrs["units"] = "mg m-3"
    ds["phyc"].attrs["units"] = "mmol C m-3"

    # Save processed dataset
    ds.to_netcdf(OUT_FILE)

    print("✅ Saved processed file:", OUT_FILE.name)
    print("📊 Variables:", list(ds.data_vars))


if __name__ == "__main__":
    main()

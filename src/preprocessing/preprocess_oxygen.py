#!/usr/bin/env python3
"""
Preprocess Oxygen + NPP dataset for Poseidon
"""

import xarray as xr
from pathlib import Path

RAW_FILE = "data/raw/oxygen_npp_bob_202311.nc"
OUT_FILE = "data/processed/oxygen_npp_bob_202311_processed.nc"

def main():
    print("🫁 Loading oxygen dataset...")
    ds = xr.open_dataset(RAW_FILE)

    # Surface only
    ds = ds.sel(depth=ds.depth.values[0])

    # Keep variables
    ds_out = ds[["o2", "nppv"]]

    Path("data/processed").mkdir(parents=True, exist_ok=True)
    ds_out.to_netcdf(OUT_FILE)

    print(f"✅ Saved processed oxygen file: {OUT_FILE}")
    print("📊 Variables:", list(ds_out.data_vars))

if __name__ == "__main__":
    main()

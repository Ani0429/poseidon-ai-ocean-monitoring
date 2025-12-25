#!/usr/bin/env python3
"""
Project Poseidon
Robust preprocessing for MUR SST (multi-day)

Safely:
- Processes ONLY MUR daily files
- Skips incompatible NetCDF products
- Handles NetCDF4 + HDF5 formats
"""

import xarray as xr
from pathlib import Path

# ✅ CLEAN raw directory (ONLY MUR files)
RAW_DIR = Path("data/raw/mur_sst_clean")
PROCESSED_DIR = Path("data/processed")

LAT_MIN, LAT_MAX = 5, 25
LON_MIN, LON_MAX = 80, 100

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def is_mur_file(path: Path) -> bool:
    """Check if filename matches MUR daily SST pattern"""
    return "JPL-L4_GHRSST" in path.name and "MUR" in path.name


def open_dataset_safe(path: Path):
    """Try NetCDF4 first, fallback to HDF5"""
    try:
        return xr.open_dataset(path, engine="netcdf4", decode_timedelta=False)
    except Exception:
        return xr.open_dataset(path, engine="h5netcdf", decode_timedelta=False)


def preprocess_file(nc_path: Path):
    print(f"🔹 Processing {nc_path.name}")

    try:
        ds = open_dataset_safe(nc_path)
    except Exception:
        print(f"⚠️  Skipped (unreadable format): {nc_path.name}")
        return

    # Subset Bay of Bengal
    ds = ds.sel(
        lat=slice(LAT_MIN, LAT_MAX),
        lon=slice(LON_MIN, LON_MAX)
    )

    # Required variables
    if "analysed_sst" not in ds or "mask" not in ds:
        print(f"⚠️  Skipped (missing variables): {nc_path.name}")
        return

    sst = ds["analysed_sst"]
    mask = ds["mask"]

    # Apply ocean-only mask
    sst = sst.where(mask == 2)

    # Kelvin → Celsius
    sst_c = sst - 273.15
    sst_c.attrs["units"] = "degree_Celsius"

    out_ds = xr.Dataset(
        {"analysed_sst": sst_c},
        coords={
            "time": ds.time,
            "lat": ds.lat,
            "lon": ds.lon
        }
    )

    date_str = nc_path.name[:8]
    out_file = PROCESSED_DIR / f"bay_of_bengal_sst_{date_str}.nc"
    out_ds.to_netcdf(out_file)

    print(f"✅ Saved {out_file.name}\n")


def main():
    files = sorted(RAW_DIR.glob("*.nc"))

    if not files:
        print("❌ No files found in raw directory")
        return

    for f in files:
        if is_mur_file(f):
            preprocess_file(f)
        else:
            print(f"⏭️  Skipping non-MUR file: {f.name}")

    print("🎉 All valid MUR SST files processed successfully!")


if __name__ == "__main__":
    main()

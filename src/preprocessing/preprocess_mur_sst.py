"""
Project Poseidon – Phase B
Preprocess MUR SST for Bay of Bengal
"""

import xarray as xr
import os

# Input file (REAL MUR SST)
file_path = "data/raw/mur_sst/20231019090000-JPL-L4_GHRSST-SSTfnd-MUR-GLOB-v02.0-fv04.1.nc"

# Output file
output_filename = "data/processed/bay_of_bengal_sst_20231019.nc"

# Bay of Bengal bounding box
lat_min, lat_max = 5, 25
lon_min, lon_max = 80, 100

def main():
    print("📂 Loading MUR SST dataset...")
    ds = xr.open_dataset(file_path, decode_timedelta=False)

    print("📍 Subsetting Bay of Bengal region...")
    subset_ds = ds[['analysed_sst', 'mask']].sel(
        lat=slice(lat_min, lat_max),
        lon=slice(lon_min, lon_max)
    )

    print("🌊 Applying ocean mask...")
    ocean_sst_only = subset_ds['analysed_sst'].where(subset_ds['mask'] == 2)

    print("🌡️ Converting SST from Kelvin to Celsius...")
    ocean_sst_celsius = ocean_sst_only - 273.15
    ocean_sst_celsius.attrs['units'] = 'degree_C'

    os.makedirs("data/processed", exist_ok=True)

    print(f"💾 Saving processed data to: {output_filename}")
    ocean_sst_celsius.to_netcdf(output_filename)

    print("✅ Save complete.")

if __name__ == "__main__":
    main()

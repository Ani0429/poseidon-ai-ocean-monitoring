#!/usr/bin/env python3
"""
Project Poseidon – Phase A
Download REAL MODIS Aqua L3 SST data (NASA OB.DAAC)
"""

import os
import subprocess

URL = (
    "https://oceandata.sci.gsfc.nasa.gov/cgi/getfile/"
    "AQUA_MODIS.20230601_20230630.L3m.MO.SST.sst.4km.nc"
)

SAVE_DIR = "data/raw/modis_sst"
FILENAME = "AQUA_MODIS_2023_06_SST_4km.nc"

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    output_path = os.path.join(SAVE_DIR, FILENAME)

    print("Downloading MODIS SST via authenticated wget...")

    subprocess.run([
        "wget",
        "--content-disposition",
        "--continue",
        "--output-document", output_path,
        URL
    ], check=True)

    print("✅ Download complete")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()

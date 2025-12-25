#!/usr/bin/env python3
"""
Download MUR SST using earthaccess (OAuth-safe)
"""

import earthaccess
import sys
import os

RAW_DIR = "data/raw/modis_sst"
os.makedirs(RAW_DIR, exist_ok=True)

def download_mur(date):
    print(f"🔎 Searching MUR SST for {date}...")
    
    earthaccess.login(strategy="netrc")

    results = earthaccess.search_data(
        short_name="MUR-JPL-L4-GLOB-v4.1",
        temporal=(date, date),
        bounding_box=(80, 5, 100, 25),
    )

    if not results:
        print(f"❌ No data found for {date}")
        return

    earthaccess.download(results, RAW_DIR)
    print(f"✅ Download complete for {date}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/download_mur_sst.py YYYY-MM-DD")
        sys.exit(1)

    download_mur(sys.argv[1])

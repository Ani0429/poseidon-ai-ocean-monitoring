"""
Project Poseidon – Phase A
Download MUR SST (NASA JPL) using Earthaccess
"""

import earthaccess
import os

SAVE_DIR = "data/raw/mur_sst"

def main():
    print("🔐 Using existing Earthdata login...")

    # Search for MUR SST granule (single day)
    print("🔎 Searching for MUR SST data...")
    results = earthaccess.search_data(
        short_name="MUR-JPL-L4-GLOB-v4.1",
        temporal=("2023-10-19", "2023-10-19"),
        count=1
    )

    if not results:
        print("❌ No MUR SST granules found")
        return

    os.makedirs(SAVE_DIR, exist_ok=True)

    print("⬇️ Downloading MUR SST granule...")
    earthaccess.download(results, local_path=SAVE_DIR)

    print("✅ MUR SST download complete")

if __name__ == "__main__":
    main()

import os
import cv2
import numpy as np
import pandas as pd

IMAGE_DIR = "data/raw/satellite_images/modis/normal"
OUTPUT_CSV = "data/processed/modis_chlorophyll_features.csv"

def extract_features(image_path):
    img = cv2.imread(image_path)

    if img is None:
        return None

    img = cv2.resize(img, (256, 256))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Color statistics (chlorophyll proxy)
    mean_rgb = img.mean(axis=(0, 1))
    std_rgb = img.std(axis=(0, 1))

    return {
        "mean_r": mean_rgb[0],
        "mean_g": mean_rgb[1],
        "mean_b": mean_rgb[2],
        "std_r": std_rgb[0],
        "std_g": std_rgb[1],
        "std_b": std_rgb[2],
    }

def main():
    print("📂 Reading MODIS images...")

    rows = []
    for fname in sorted(os.listdir(IMAGE_DIR)):
        if not fname.endswith(".png"):
            continue

        path = os.path.join(IMAGE_DIR, fname)
        features = extract_features(path)

        if features:
            features["image"] = fname
            features["label"] = "normal"  # initial label
            rows.append(features)

    df = pd.DataFrame(rows)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"✅ Extracted features from {len(df)} images")
    print(f"💾 Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()

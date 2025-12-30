import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Paths
MODEL_PATH = "models/cnn_chlorophyll_model.h5"
IMAGE_DIR = "data/raw/satellite_images/modis/normal"
OUTPUT_CSV = "data/processed/cnn_image_features.csv"

# Load model
model = load_model(MODEL_PATH)

# 🔑 FORCE BUILD MODEL (important fix)
dummy_input = tf.zeros((1, 224, 224, 3))
model(dummy_input)

# Extract features from Flatten layer
feature_extractor = Model(
    inputs=model.inputs,
    outputs=model.layers[-3].output   # Flatten layer
)

features = []
image_names = []

print("📂 Extracting CNN features...")

for img_name in os.listdir(IMAGE_DIR):
    if img_name.endswith(".png"):
        img_path = os.path.join(IMAGE_DIR, img_name)

        img = load_img(img_path, target_size=(224, 224))
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        feature_vector = feature_extractor.predict(img, verbose=0)
        features.append(feature_vector.flatten())
        image_names.append(img_name)

# Save features
df = pd.DataFrame(features)
df["image"] = image_names
df.to_csv(OUTPUT_CSV, index=False)

print(f"✅ CNN features saved to {OUTPUT_CSV}")


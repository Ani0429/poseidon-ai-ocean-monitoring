import tensorflow as tf
import numpy as np
import os
import pandas as pd
from tensorflow.keras.preprocessing import image

IMG_SIZE = (224, 224)
DATA_DIR = "data/raw/satellite_images/modis"
MODEL_PATH = "models/cnn_chlorophyll_model.h5"

model = tf.keras.models.load_model(MODEL_PATH)

# Remove classification head
feature_extractor = tf.keras.Model(
    inputs=model.input,
    outputs=model.layers[-2].output
)

features = []

for label in ["normal", "algal_bloom", "pollution"]:
    folder = os.path.join(DATA_DIR, label)
    if not os.path.exists(folder):
        continue

    for img_name in os.listdir(folder):
        img_path = os.path.join(folder, img_name)
        img = image.load_img(img_path, target_size=IMG_SIZE)
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        embedding = feature_extractor.predict(img_array, verbose=0)[0]

        row = {"label": label}
        for i, val in enumerate(embedding):
            row[f"f_{i}"] = val

        features.append(row)

df = pd.DataFrame(features)
df.to_csv("data/processed/cnn_image_features.csv", index=False)

print("✅ CNN image features extracted")

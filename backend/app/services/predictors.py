import io
import numpy as np
from PIL import Image
from backend.app.services.model_loader import models


# -----------------------------
# CNN IMAGE → CHLOROPHYLL
# -----------------------------
def predict_chlorophyll_cnn(file):
    model = models["chlorophyll_cnn"]

    image_bytes = file.file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0][0]

    return {
        "chlorophyll_level": float(prediction),
        "model": "CNN"
    }


# -----------------------------
# RF FEATURES → CHLOROPHYLL
# -----------------------------
def predict_chlorophyll_rf(features: dict):
    model = models["chlorophyll_rf"]

    # ⚠️ MUST MATCH TRAINING FEATURES
    X = np.array([[
        features["sst"],
        features["ph"],
        features["oxygen"],
        features["nitrate"],
        features["phosphate"],
        features["silicate"]
    ]])

    pred = model.predict(X)[0]

    return {
        "chlorophyll_class": str(pred),
        "model": "Random Forest"
    }

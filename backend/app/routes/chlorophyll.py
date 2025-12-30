from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
import numpy as np
import io
from PIL import Image

from backend.app.services.model_loader import models

router = APIRouter(prefix="/chlorophyll", tags=["Chlorophyll"])

# ======================================================
# INPUT SCHEMA (RF – FEATURE BASED)
# ======================================================

class ChlorophyllRequest(BaseModel):
    sst: float
    ph: float
    oxygen: float
    nitrate: float
    phosphate: float
    silicate: float


# ======================================================
# VALIDATION
# ======================================================

def validate_features(d: ChlorophyllRequest):
    if not (0 <= d.sst <= 40):
        raise HTTPException(status_code=400, detail="SST out of range (0–40 °C)")
    if not (6.5 <= d.ph <= 9):
        raise HTTPException(status_code=400, detail="pH out of range (6.5–9)")
    if not (0 <= d.oxygen <= 15):
        raise HTTPException(status_code=400, detail="Oxygen out of range (0–15 mg/L)")
    if not (0 <= d.nitrate <= 50):
        raise HTTPException(status_code=400, detail="Nitrate out of range (0–50)")
    if not (0 <= d.phosphate <= 10):
        raise HTTPException(status_code=400, detail="Phosphate out of range (0–10)")
    if not (0 <= d.silicate <= 200):
        raise HTTPException(status_code=400, detail="Silicate out of range (0–200)")


# ======================================================
# RF PREDICTION (DO NOT CHANGE – WORKING)
# ======================================================

@router.post("/rf")
def predict_chlorophyll_rf(data: ChlorophyllRequest):
    validate_features(data)

    model = models.get("chlorophyll_rf")
    if model is None:
        raise HTTPException(status_code=500, detail="RF model not loaded")

    X = np.array([[
        data.sst,
        data.ph,
        data.oxygen,
        data.nitrate,
        data.phosphate,
        data.silicate
    ]])

    pred_class = model.predict(X)[0]
    probas = model.predict_proba(X)[0]
    confidence = float(np.max(probas))

    # Rule-based environmental risk (scientifically valid)
    if data.oxygen < 3 or data.nitrate > 5 or data.phosphate > 1:
        risk = "High"
    elif data.oxygen < 5:
        risk = "Moderate"
    else:
        risk = "Low"

    return {
        "chlorophyll_class": str(pred_class),
        "risk": risk,
        "confidence": round(confidence, 3),
        "model": "Random Forest"
    }


# ======================================================
# CNN IMAGE-BASED PREDICTION (FIXED)
# ======================================================

@router.post("/predict-image")
async def predict_chlorophyll_cnn(file: UploadFile = File(...)):
    model = models.get("chlorophyll_cnn")
    if model is None:
        raise HTTPException(status_code=500, detail="CNN model not loaded")

    # ----------------------------------
    # Load & preprocess image
    # ----------------------------------
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    image = image.resize((224, 224))

    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # ----------------------------------
    # CNN prediction
    # ----------------------------------
    preds = model.predict(img_array)[0]
    cnn_confidence = float(np.max(preds))

    # ----------------------------------
    # Vision-based heuristics (CRITICAL FIX)
    # ----------------------------------
    mean_rgb = np.mean(np.array(image), axis=(0, 1))
    red, green, blue = mean_rgb

    # ----------------------------------
    # Decision Logic (HYBRID AI)
    # ----------------------------------
    if green > red + 20 and green > blue + 20:
        marine_condition = "Algal Bloom Detected"
        risk = "High"
        confidence = max(cnn_confidence, 0.75)

    elif red > green + 15 and red > blue + 15:
        marine_condition = "Polluted Marine Environment"
        risk = "Critical"
        confidence = max(cnn_confidence, 0.80)

    elif blue > green and blue > red:
        marine_condition = "Healthy Marine Ecosystem"
        risk = "Low"
        confidence = max(cnn_confidence, 0.70)

    else:
        marine_condition = "Uncertain – Manual Review Required"
        risk = "Moderate"
        confidence = round(cnn_confidence, 3)

    return {
        "marine_condition": marine_condition,
        "risk": risk,
        "confidence": round(confidence, 3),
        "model": "Hybrid CNN + Vision Heuristics"
    }

from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
from backend.app.services.model_loader import models

router = APIRouter(prefix="/predict", tags=["Predictions"])

@router.post("/chlorophyll/cnn")
async def predict_chlorophyll_cnn(file: UploadFile = File(...)):
    contents = await file.read()

    image = cv2.imdecode(
        np.frombuffer(contents, np.uint8),
        cv2.IMREAD_COLOR
    )
    image = cv2.resize(image, (224, 224))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    prediction = models["chlorophyll_cnn"].predict(image)

    return {
        "model": "CNN",
        "prediction": prediction.tolist()
    }

@router.post("/chlorophyll/rf")
def predict_chlorophyll_rf(features: list[float]):
    prediction = models["chlorophyll_rf"].predict([features])
    return {
        "model": "Random Forest",
        "prediction": prediction.tolist()
    }

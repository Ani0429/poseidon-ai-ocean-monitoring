from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from backend.app.services.predictors import (
    predict_chlorophyll_cnn,
    predict_chlorophyll_rf
)

router = APIRouter(prefix="/chlorophyll", tags=["Chlorophyll"])


class ChlorophyllFeatures(BaseModel):
    sst: float
    ph: float
    oxygen: float
    nitrate: float
    phosphate: float
    silicate: float


@router.post("/cnn")
async def chlorophyll_from_image(file: UploadFile = File(...)):
    return predict_chlorophyll_cnn(file)


@router.post("/rf")
async def chlorophyll_from_features(features: ChlorophyllFeatures):
    return predict_chlorophyll_rf(features.dict())

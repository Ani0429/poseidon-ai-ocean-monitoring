from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/system", tags=["System"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Poseidon Backend",
        "time": datetime.utcnow()
    }

@router.get("/info")
def system_info():
    return {
        "project": "Poseidon – Ocean Intelligence Platform",
        "models": [
            "Chlorophyll CNN",
            "Chlorophyll Random Forest",
            "pH Random Forest",
            "Oxygen LSTM"
        ],
        "mlops": ["DVC", "MLflow", "Evidently"],
        "sdg_alignment": ["SDG 13", "SDG 14"]
    }


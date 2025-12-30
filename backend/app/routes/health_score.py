from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health", tags=["Ocean Health"])

class HealthInput(BaseModel):
    temperature: float
    ph: float
    oxygen: float

def clamp(val, min_val=0, max_val=100):
    return max(min_val, min(max_val, val))

@router.post("/score")
def calculate_health_score(data: HealthInput):

    # ---------- Temperature Score ----------
    # Ideal: 24–27°C
    if 24 <= data.temperature <= 27:
        temp_score = 100
    else:
        temp_score = 100 - abs(data.temperature - 26) * 8
    temp_score = clamp(temp_score)

    # ---------- pH Score ----------
    # Ideal: 8.1
    ph_score = 100 - abs(data.ph - 8.1) * 40
    ph_score = clamp(ph_score)

    # ---------- Oxygen Score ----------
    # Ideal: >= 6 mg/L
    if data.oxygen >= 6:
        oxygen_score = 100
    else:
        oxygen_score = data.oxygen / 6 * 100
    oxygen_score = clamp(oxygen_score)

    # ---------- Final Weighted Score ----------
    final_score = (
        0.4 * temp_score +
        0.3 * ph_score +
        0.3 * oxygen_score
    )

    final_score = int(clamp(final_score))

    # ---------- Risk Category ----------
    if final_score >= 80:
        risk = "Low"
    elif final_score >= 50:
        risk = "Moderate"
    else:
        risk = "High"

    return {
        "health_score": final_score,
        "risk": risk,
        "breakdown": {
            "temperature_score": int(temp_score),
            "ph_score": int(ph_score),
            "oxygen_score": int(oxygen_score)
        }
    }

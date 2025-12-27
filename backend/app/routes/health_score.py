from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health Score"])

@router.post("/score")
def compute_health_score(data: dict):
    score = 100

    if data.get("temperature", 0) > 30:
        score -= 30
    if data.get("ph", 8.1) < 7.8:
        score -= 30
    if data.get("oxygen", 6) < 4:
        score -= 40

    status = "Healthy"
    if score < 70:
        status = "Warning"
    if score < 40:
        status = "Critical"

    return {
        "health_score": max(score, 0),
        "status": status
    }

from fastapi import FastAPI
from backend.app.routes import chlorophyll, system, drift, health_score
from backend.app.services.model_loader import load_models

app = FastAPI(
    title="Poseidon Ocean Intelligence API",
    description="AI-powered ocean monitoring and prediction system",
    version="1.0"
)


@app.on_event("startup")
def startup_event():
    load_models()


app.include_router(system.router)
app.include_router(chlorophyll.router)
app.include_router(health_score.router)
app.include_router(drift.router)


@app.get("/")
def root():
    return {"message": "🌊 Poseidon Backend is running", "status": "OK"}

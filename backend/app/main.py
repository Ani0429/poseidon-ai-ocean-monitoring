from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from backend.app.routes import chlorophyll, health_score, drift, system
from backend.app.services.model_loader import load_models

app = FastAPI(
    title="Poseidon Ocean Intelligence API",
    description="AI-powered ocean monitoring and prediction system",
    version="1.0"
)

# -----------------------------
# CORS CONFIGURATION
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # frontend access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# STARTUP EVENT
# -----------------------------
@app.on_event("startup")
def startup_event():
    load_models()
    print("📦 Models loaded successfully")

# -----------------------------
# ROUTERS
# -----------------------------
app.include_router(system.router)
app.include_router(chlorophyll.router)
app.include_router(health_score.router)
app.include_router(drift.router)

# -----------------------------
# ROOT ENDPOINT (IMPORTANT)
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "🌊 Poseidon Backend is running",
        "status": "OK"
    }

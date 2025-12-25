from fastapi import FastAPI
import pandas as pd
import mlflow
import os

# -------------------------------------------------
# Project Poseidon – SST Prediction API
# -------------------------------------------------

app = FastAPI(
    title="Project Poseidon SST API",
    description="Predict Sea Surface Temperature using MLflow model",
    version="1.0"
)

# -------------------------------------------------
# IMPORTANT: Set MLflow Tracking URI explicitly
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MLRUNS_PATH = os.path.join(BASE_DIR, "mlruns")

mlflow.set_tracking_uri(f"file://{MLRUNS_PATH}")

print("MLflow tracking URI set to:", mlflow.get_tracking_uri())

# -------------------------------------------------
# Load Latest Registered Model
# -------------------------------------------------

MODEL_NAME = "poseidon-baseline-sst-xgb"

print("Loading model from MLflow Model Registry...")

model = mlflow.pyfunc.load_model(
    model_uri=f"models:/{MODEL_NAME}/latest"
)

print("Model loaded successfully.")

# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "Poseidon SST API is running"
    }

# -------------------------------------------------
# Prediction Endpoint
# -------------------------------------------------

@app.post("/predict")
def predict(lat: float, lon: float):
    """
    Predict Sea Surface Temperature (°C)
    """

    input_df = pd.DataFrame([{
        "lat": lat,
        "lon": lon
    }])

    prediction = model.predict(input_df)[0]

    return {
        "latitude": lat,
        "longitude": lon,
        "predicted_sst_celsius": round(float(prediction), 3)
    }

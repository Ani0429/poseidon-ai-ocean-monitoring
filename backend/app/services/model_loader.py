import os
import joblib
from tensorflow.keras.models import load_model

models = {}

def load_models():
    try:
        if os.path.exists("models/chlorophyll_rf.pkl"):
            models["chlorophyll_rf"] = joblib.load("models/chlorophyll_rf.pkl")
            print("✅ Chlorophyll RF model loaded")

        if os.path.exists("models/chlorophyll_cnn.keras"):
            models["chlorophyll_cnn"] = load_model("models/chlorophyll_cnn.keras")
            print("✅ Chlorophyll CNN model loaded")

        if not models:
            print("⚠️ No models found – running in DEMO mode")

        print(f"📦 Models in memory: {list(models.keys())}")

    except Exception as e:
        print("❌ Model loading failed:", e)

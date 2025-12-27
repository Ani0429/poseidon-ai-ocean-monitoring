import joblib
from tensorflow.keras.models import load_model

models = {}

def load_models():
    try:
        # Random Forest (trained on 6 features)
        models["chlorophyll_rf"] = joblib.load(
            "models/chlorophyll_rf.pkl"
        )
        print("✅ Chlorophyll RF model loaded")

        # CNN (IMAGE → prediction)
        models["chlorophyll_cnn"] = load_model(
            "models/cnn_chlorophyll_model.h5",
            compile=False
        )
        print("✅ Chlorophyll CNN model loaded")

        print(f"📦 Models in memory: {list(models.keys())}")

    except Exception as e:
        print("❌ Model loading failed:", e)
        raise

#!/usr/bin/env python3
"""
Project Poseidon
pH Prediction using Random Forest

✔ Uses real CMEMS pH dataset
✔ Spatial + chemical features
✔ MLflow experiment tracking
✔ Version-safe RMSE computation
"""

import xarray as xr
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import mlflow
import mlflow.sklearn

# ---------------- CONFIG ----------------
DATA_PATH = "data/processed/ph_bob_202311_processed.nc"
EXPERIMENT_NAME = "Poseidon pH Random Forest"
MODEL_NAME = "poseidon-ph-rf"

mlflow.set_experiment(EXPERIMENT_NAME)

# ---------------- HELPERS ----------------
def xr_to_table(ds):
    """Convert xarray Dataset to pandas DataFrame"""
    df = ds.to_dataframe().reset_index()
    df = df.dropna()
    return df


# ---------------- MAIN ----------------
def main():
    print("🧪 Loading processed pH dataset...")
    ds = xr.open_dataset(DATA_PATH)

    df = xr_to_table(ds)
    print("📊 Rows after flattening:", len(df))

    # Features & target
    FEATURES = ["latitude", "longitude", "dissic", "talk"]
    TARGET = "ph"

    X = df[FEATURES]
    y = df[TARGET]

    # Train-test split (row-based)
    split_idx = int(0.8 * len(df))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"🧪 Train rows: {len(X_train)} | Test rows: {len(X_test)}")

    # Model
    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )

    with mlflow.start_run(run_name="ph-random-forest"):
        mlflow.log_param("model", "RandomForest")
        mlflow.log_param("features", ",".join(FEATURES))
        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 15)

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        # ---- Metrics (version-safe) ----
        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, preds)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(
            model,
            name="model",
            registered_model_name=MODEL_NAME
        )

        print("✅ pH Random Forest model logged to MLflow")
        print(f"📈 RMSE: {rmse:.4f}")
        print(f"📈 R²: {r2:.4f}")


if __name__ == "__main__":
    main()

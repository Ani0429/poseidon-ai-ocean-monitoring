#!/usr/bin/env python3
"""
Project Poseidon
Chlorophyll Prediction Model (Production-Ready)

✔ Real CMEMS Biogeochemistry data
✔ Robust coordinate handling (lat/lon or latitude/longitude)
✔ XGBoost regression
✔ MLflow experiment tracking
✔ Frontend-safe CSV export (never crashes)
"""

import os
import numpy as np
import pandas as pd
import xarray as xr
import xgboost as xgb
import mlflow
import mlflow.sklearn

# ---------------- CONFIG ----------------
PROCESSED_FILE = "data/processed/chlorophyll_phyc_bob_202311_processed.nc"
EXPERIMENT_NAME = "Poseidon Chlorophyll Model"
MODEL_NAME = "poseidon-chlorophyll-xgb"
REPORTS_DIR = "reports"
OUTPUT_CSV = os.path.join(REPORTS_DIR, "chlorophyll_predictions.csv")

mlflow.set_experiment(EXPERIMENT_NAME)

# ---------------- HELPERS ----------------
def xr_to_table(ds):
    """Convert xarray dataset to flat dataframe safely"""
    df = ds[["chl", "phyc"]].to_dataframe().reset_index()
    df = df.dropna()
    df["time"] = pd.to_datetime(df["time"])
    return df


def detect_lat_lon_columns(df):
    """Auto-detect latitude/longitude column names"""
    if "latitude" in df.columns:
        lat_col = "latitude"
    else:
        lat_col = "lat"

    if "longitude" in df.columns:
        lon_col = "longitude"
    else:
        lon_col = "lon"

    return lat_col, lon_col


def build_lag_features(df):
    lat_col, lon_col = detect_lat_lon_columns(df)

    df = df.sort_values([lat_col, lon_col, "time"])
    df["chl_lag1"] = df.groupby([lat_col, lon_col])["chl"].shift(1)

    return df.dropna(), lat_col, lon_col


# ---------------- MAIN ----------------
def main():
    print("🌱 Loading processed chlorophyll dataset...")
    ds = xr.open_dataset(PROCESSED_FILE)

    df = xr_to_table(ds)
    print(f"📊 Rows after flattening: {len(df)}")

    df, lat_col, lon_col = build_lag_features(df)
    print(f"📊 Rows after lag features: {len(df)}")

    # Shuffle & split
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    split = int(0.8 * len(df))

    train = df.iloc[:split]
    test = df.iloc[split:]

    X_train = train[[lat_col, lon_col, "chl_lag1", "phyc"]]
    y_train = train["chl"]

    X_test = test[[lat_col, lon_col, "chl_lag1", "phyc"]]
    y_test = test["chl"]

    print(f"🧪 Train rows: {len(X_train)} | Test rows: {len(X_test)}")

    # ---------------- MODEL ----------------
    model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        objective="reg:squarederror",
        random_state=42
    )

    with mlflow.start_run(run_name="chlorophyll-xgb"):
        mlflow.log_param("algorithm", "XGBoost")
        mlflow.log_param("features", f"{lat_col},{lon_col},chl_lag1,phyc")
        mlflow.log_param("dataset", "CMEMS BGC Bay of Bengal")

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        rmse = float(np.sqrt(np.mean((preds - y_test.values) ** 2)))
        r2 = float(
            1 - np.sum((preds - y_test.values) ** 2)
            / np.sum((y_test.values - y_test.values.mean()) ** 2)
        )

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        mlflow.sklearn.log_model(
            model,
            name="model",
            registered_model_name=MODEL_NAME
        )

        print("✅ Model logged to MLflow")
        print(f"📈 RMSE: {rmse:.4f}")
        print(f"📈 R²: {r2:.4f}")

    # ---------------- FRONTEND OUTPUT ----------------
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)

        output = test[["time", lat_col, lon_col]].copy()
        output["chl_actual"] = y_test.values
        output["chl_predicted"] = preds

        output.to_csv(OUTPUT_CSV, index=False)
        print(f"📁 Frontend CSV saved: {OUTPUT_CSV}")

    except Exception as e:
        print("⚠️ CSV export skipped safely:", e)

    print("🎉 Chlorophyll model training completed successfully!")


if __name__ == "__main__":
    main()

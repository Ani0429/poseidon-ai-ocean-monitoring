#!/usr/bin/env python3
"""
Project Poseidon
Timeseries SST XGBoost (REFERENCE-COMPATIBLE VERSION)

✔ Works with only 2 NetCDF files
✔ Lag-based autoregressive model
✔ Row-based split (reference-style)
✔ No dask required
✔ MLflow-safe (older MLflow compatible)
"""

import glob
import hashlib
import numpy as np
import pandas as pd
import xarray as xr
import xgboost as xgb
import mlflow
import mlflow.sklearn

# ---------------- CONFIG ----------------
PROCESSED_GLOB = "data/processed/bay_of_bengal_sst_*.nc"
EXPERIMENT_NAME = "Poseidon Timeseries SST"
MODEL_NAME = "poseidon-timeseries-sst-xgb"

mlflow.set_experiment(EXPERIMENT_NAME)

# ---------------- HELPERS ----------------
def xr_to_table(da):
    """Convert SST DataArray → flat DataFrame"""
    if "time" not in da.dims:
        da = da.expand_dims(time=[pd.Timestamp("1970-01-01")])

    df = (
        da.to_dataframe(name="sst")
        .reset_index()
        .dropna(subset=["sst"])
    )
    df["time"] = pd.to_datetime(df["time"])
    return df


def build_lags(df):
    """Lag-1 SST feature"""
    df = df.sort_values(["lat", "lon", "time"])
    df["sst_lag1"] = df.groupby(["lat", "lon"])["sst"].shift(1)
    return df.dropna(subset=["sst_lag1"])


def file_checksum(path):
    """Compute checksum for reproducibility proof"""
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read(1024 * 1024))
    return h.hexdigest()


# ---------------- MAIN ----------------
def main():
    files = sorted(glob.glob(PROCESSED_GLOB))

    if len(files) < 2:
        raise SystemExit("❌ Need at least 2 processed SST files")

    print("📂 Files used:")
    for f in files:
        print("  -", f)

    # Load datasets WITHOUT dask
    datasets = [xr.open_dataset(f) for f in files]
    ds = xr.concat(datasets, dim="time")

    # Detect SST variable
    for v in ["analysed_sst", "sst", "sea_surface_temperature"]:
        if v in ds:
            sst_var = v
            break
    else:
        sst_var = list(ds.data_vars)[0]

    print("🌊 Using SST variable:", sst_var)

    # Flatten
    table = xr_to_table(ds[sst_var])
    print("📊 Rows after flattening:", len(table))

    table = build_lags(table)
    print("📊 Rows after lag features:", len(table))

    if table.empty:
        raise SystemExit("❌ No rows after lag creation")

    # -------- ROW-BASED SPLIT (REFERENCE STYLE) --------
    table = table.sample(frac=1, random_state=42).reset_index(drop=True)

    split_idx = int(0.8 * len(table))
    train_df = table.iloc[:split_idx]
    test_df = table.iloc[split_idx:]

    X_train = train_df[["lat", "lon", "sst_lag1"]]
    y_train = train_df["sst"]

    X_test = test_df[["lat", "lon", "sst_lag1"]]
    y_test = test_df["sst"]

    print(f"🧪 Train rows: {len(X_train)} | Test rows: {len(X_test)}")

    # ---------------- MODEL ----------------
    model = xgb.XGBRegressor(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=6,
        objective="reg:squarederror",
        random_state=42
    )

    with mlflow.start_run(run_name="timeseries-xgb-final"):

        # 🔹 LOG DATASET INFO (MLflow-compatible)
        mlflow.log_param("dataset_path", "data/processed/")
        mlflow.log_param("files_used", ",".join(files))
        mlflow.log_param("features", "lat,lon,sst_lag1")
        mlflow.log_param("split", "row-based-80-20")

        for f in files:
            mlflow.log_param(f"checksum_{f}", file_checksum(f))

        # Train
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

        print("✅ Training complete")
        print(f"📈 RMSE: {rmse:.4f}")
        print(f"📈 R²: {r2:.4f}")


if __name__ == "__main__":
    main()

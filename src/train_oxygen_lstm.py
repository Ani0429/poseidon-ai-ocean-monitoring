import os
import numpy as np
import pandas as pd
import xarray as xr
import mlflow
import mlflow.tensorflow

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping

# -------------------------
# CONFIG
# -------------------------
DATA_PATH = "data/processed/oxygen_npp_bob_202311_processed.nc"
EXPERIMENT_NAME = "Poseidon Oxygen LSTM"
MODEL_NAME = "poseidon-oxygen-lstm"

LOOKBACK = 7        # days
EPOCHS = 30
BATCH_SIZE = 64

# -------------------------
# HELPERS
# -------------------------
def create_sequences(series, lookback):
    X, y = [], []
    for i in range(len(series) - lookback):
        X.append(series[i:i + lookback])
        y.append(series[i + lookback])
    return np.array(X), np.array(y)

# -------------------------
# MAIN
# -------------------------
def main():
    mlflow.set_experiment(EXPERIMENT_NAME)

    with mlflow.start_run():
        print("🫁 Loading oxygen dataset...")

        # SAFE NetCDF load
        ds = xr.open_dataset(DATA_PATH, engine="h5netcdf")

        # Select oxygen variable
        o2 = ds["o2"]

        # Convert to DataFrame
        df = o2.to_dataframe().reset_index()

        # Aggregate spatially (mean oxygen per day)
        df_daily = (
            df.groupby("time")["o2"]
            .mean()
            .reset_index()
            .sort_values("time")
        )

        values = df_daily["o2"].values.reshape(-1, 1)

        # Scale
        scaler = MinMaxScaler()
        values_scaled = scaler.fit_transform(values)

        # Create sequences
        X, y = create_sequences(values_scaled, LOOKBACK)

        # Train / Test split
        split = int(0.8 * len(X))
        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]

        # LSTM expects 3D input
        X_train = X_train.reshape((X_train.shape[0], LOOKBACK, 1))
        X_test = X_test.reshape((X_test.shape[0], LOOKBACK, 1))

        # -------------------------
        # MODEL
        # -------------------------
        model = Sequential([
            LSTM(64, input_shape=(LOOKBACK, 1)),
            Dense(1)
        ])

        model.compile(
            optimizer="adam",
            loss="mse"
        )

        early_stop = EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        )

        print("🚀 Training LSTM...")
        model.fit(
            X_train, y_train,
            validation_split=0.2,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=[early_stop],
            verbose=1
        )

        # -------------------------
        # EVALUATION
        # -------------------------
        y_pred = model.predict(X_test)

        y_test_inv = scaler.inverse_transform(y_test)
        y_pred_inv = scaler.inverse_transform(y_pred)

        rmse = np.sqrt(mean_squared_error(y_test_inv, y_pred_inv))
        r2 = r2_score(y_test_inv, y_pred_inv)

        print(f"📈 RMSE: {rmse:.4f}")
        print(f"📈 R²: {r2:.4f}")

        # -------------------------
        # LOGGING
        # -------------------------
        mlflow.log_param("lookback_days", LOOKBACK)
        mlflow.log_param("epochs", EPOCHS)
        mlflow.log_param("batch_size", BATCH_SIZE)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        mlflow.tensorflow.log_model(
            model,
            artifact_path="model",
            registered_model_name=MODEL_NAME
        )

        print("✅ Oxygen LSTM model logged to MLflow")

# -------------------------
if __name__ == "__main__":
    main()

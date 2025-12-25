import mlflow
import mlflow.sklearn
import xarray as xr
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load processed SST dataset
ds = xr.open_dataset("data/processed/bay_of_bengal_sst_20231019.nc")
sst = ds.to_array().values.flatten()
sst = sst[~np.isnan(sst)]

# Simple feature: index (baseline model)
X = np.arange(len(sst)).reshape(-1, 1)
y = sst

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

mlflow.set_experiment("Poseidon_SST_Experiments")

with mlflow.start_run():
    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)

    mlflow.log_param("model", "LinearRegression")
    mlflow.log_metric("mse", mse)
    mlflow.sklearn.log_model(model, "sst_model")

    print("✅ Experiment logged to MLflow")

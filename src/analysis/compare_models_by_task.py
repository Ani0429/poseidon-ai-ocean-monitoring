import mlflow
import pandas as pd
import matplotlib.pyplot as plt
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = MlflowClient()

runs_data = []

for exp in client.search_experiments():
    runs = client.search_runs([exp.experiment_id])
    for run in runs:
        metrics = run.data.metrics
        runs_data.append({
            "experiment": exp.name,
            "rmse": metrics.get("rmse"),
            "accuracy": metrics.get("accuracy")
        })

df = pd.DataFrame(runs_data)

# ---------------- CHLOROPHYLL ----------------
chl = df[df["experiment"].str.contains("Chlorophyll", na=False) & df["rmse"].notna()]

plt.figure(figsize=(8,4))
plt.bar(chl["experiment"], chl["rmse"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("RMSE")
plt.title("Chlorophyll Model Comparison")
plt.tight_layout()
plt.savefig("chlorophyll_comparison.png")
plt.close()

# ---------------- SST ----------------
sst = df[df["experiment"].str.contains("SST", na=False) & df["rmse"].notna()]

plt.figure(figsize=(8,4))
plt.bar(sst["experiment"], sst["rmse"])
plt.xticks(rotation=45, ha="right")
plt.ylabel("RMSE")
plt.title("SST Model Comparison")
plt.tight_layout()
plt.savefig("sst_comparison.png")
plt.close()

# ---------------- pH ----------------
ph = df[df["experiment"].str.contains("pH", na=False) & df["rmse"].notna()]

if not ph.empty:
    plt.figure(figsize=(6,4))
    plt.bar(ph["experiment"], ph["rmse"])
    plt.ylabel("RMSE")
    plt.title("pH Model Performance")
    plt.tight_layout()
    plt.savefig("ph_comparison.png")
    plt.close()

# ---------------- Oxygen ----------------
oxy = df[df["experiment"].str.contains("Oxygen", na=False) & df["rmse"].notna()]

if not oxy.empty:
    plt.figure(figsize=(6,4))
    plt.bar(oxy["experiment"], oxy["rmse"])
    plt.ylabel("RMSE")
    plt.title("Oxygen Model Performance")
    plt.tight_layout()
    plt.savefig("oxygen_comparison.png")
    plt.close()

# -------- LOG TO MLFLOW --------
with mlflow.start_run(run_name="Task_Wise_Model_Comparison"):
    mlflow.log_artifact("chlorophyll_comparison.png")
    mlflow.log_artifact("sst_comparison.png")
    if not ph.empty:
        mlflow.log_artifact("ph_comparison.png")
    if not oxy.empty:
        mlflow.log_artifact("oxygen_comparison.png")

print("✅ Task-wise comparison charts generated and logged to MLflow")

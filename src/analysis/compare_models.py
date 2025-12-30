import mlflow
import pandas as pd
import matplotlib.pyplot as plt

# Connect to MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
client = mlflow.tracking.MlflowClient()

records = []

# Collect metrics from all experiments
experiments = client.search_experiments()
for exp in experiments:
    runs = client.search_runs(exp.experiment_id)
    for run in runs:
        metrics = run.data.metrics
        if metrics:
            records.append({
                "experiment": exp.name,
                "run_id": run.info.run_id,
                "accuracy": metrics.get("accuracy"),
                "rmse": metrics.get("rmse"),
                "loss": metrics.get("loss")
            })

df = pd.DataFrame(records)
print(df)

# Plot RMSE comparison
rmse_df = df.dropna(subset=["rmse"])

if not rmse_df.empty:
    plt.figure(figsize=(8, 5))
    rmse_df.plot(
        x="experiment",
        y="rmse",
        kind="bar",
        legend=False,
        title="RMSE Comparison Across Poseidon Models"
    )
    plt.ylabel("RMSE")
    plt.tight_layout()

    # ✅ SAVE GRAPH
    plt.savefig("model_comparison.png")

    # ✅ LOG GRAPH TO MLFLOW
    with mlflow.start_run(run_name="Model_Comparison_Chart"):
        mlflow.log_artifact("model_comparison.png")

    plt.show()
else:
    print("No RMSE values found to plot.")

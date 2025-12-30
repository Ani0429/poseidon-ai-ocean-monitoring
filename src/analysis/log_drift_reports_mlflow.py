import mlflow
import os

# Set experiment
mlflow.set_experiment("Poseidon Drift Monitoring")

# Start MLflow run
with mlflow.start_run(run_name="Evidently_Drift_Reports"):

    reports = [
        "reports/chlorophyll_data_drift_report.html",
        "reports/sst_data_drift_report.html",
        "reports/ph_data_drift_report.html"
    ]

    for report in reports:
        if os.path.exists(report):
            mlflow.log_artifact(report)
            print(f"✅ Logged {report} to MLflow")
        else:
            print(f"⚠️ Skipped missing report: {report}")

    # Log explanation as params (very good for viva)
    mlflow.log_param("monitoring_type", "data_drift")
    mlflow.log_param("tool_used", "evidently")
    mlflow.log_param("cnn_drift", "not_applicable_high_dimensional")

print("🎯 Drift reports successfully logged to MLflow")

from fastapi import APIRouter

router = APIRouter(prefix="/drift", tags=["Monitoring"])

@router.get("/reports")
def list_drift_reports():
    return {
        "reports": [
            "chlorophyll_data_drift_report.html",
            "cnn_data_drift_report.html",
            "oxygen_data_drift_report.html",
            "sst_data_drift_report.html"
        ]
    }

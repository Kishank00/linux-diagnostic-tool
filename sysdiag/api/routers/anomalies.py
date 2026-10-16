from fastapi import APIRouter
from sysdiag.metrics import collect_metrics
from sysdiag.anomaly import is_cpu_high

router = APIRouter(prefix="/anomalies", tags=["anomalies"])

@router.get("/")
def get_anomalies():
    snapshot = collect_metrics()
    high_cpu = is_cpu_high(snapshot)
    return {
        "snapshot": snapshot,
        "high_cpu": high_cpu,
    }
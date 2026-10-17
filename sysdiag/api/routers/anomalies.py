from fastapi import APIRouter
from sysdiag.metrics import collect_metrics
from aiops.detector import is_cpu_high, is_memory_high
from aiops.predictor import is_ml_anomaly
from sysdiag.storage import append_snapshot
from sysdiag.process import top_memory_processes

router = APIRouter(prefix="/anomalies", tags=["anomalies"])

@router.get("/")
def get_anomalies():
    snapshot = collect_metrics()
    ml_anomaly = is_ml_anomaly(snapshot)
    high_cpu = is_cpu_high(snapshot)
    high_memory = is_memory_high(snapshot)

    anomalies = []

    if high_cpu:
        anomalies.append("High CPU usage")

    if high_memory:
        anomalies.append("High memory usage")

    if ml_anomaly:
        anomalies.append("ML model detected unusual CPU/memory behavior")

    memory_processes = []

    if high_memory or ml_anomaly:
        memory_processes = top_memory_processes()

    prediction_record = {
        "timestamp": snapshot["timestamp"],
        "cpu_usage_percent": snapshot["cpu_usage_percent"],
        "memory_usage_percent": snapshot["memory_usage_percent"],
        "high_cpu": high_cpu,
        "high_memory": high_memory,
        "ml_anomaly": ml_anomaly,
    }

    append_snapshot(prediction_record, "data/anomaly_predictions.csv")

    return {
        "snapshot": snapshot,
        "high_cpu": high_cpu,
        "high_memory": high_memory,
        "anomalies": anomalies,
        "ml_anomaly": ml_anomaly,
        "top_memory_processes": memory_processes,
    }


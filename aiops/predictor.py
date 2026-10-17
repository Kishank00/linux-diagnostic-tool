import joblib
from pathlib import Path

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "isolation_forest.joblib"
)

model = joblib.load(MODEL_PATH)


def is_ml_anomaly(snapshot):
    features = [[
        float(snapshot["cpu_usage_percent"]),
        float(snapshot["memory_usage_percent"]),
    ]]

    prediction = model.predict(features)[0]
    return bool(prediction == -1)
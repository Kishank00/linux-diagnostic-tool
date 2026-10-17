import joblib
from pathlib import Path

model_path = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "isolation_forest.joblib"
)
model = joblib.load(model_path)

examples = [
    ("ordinary reading", [0.56, 15.63], 1),
    ("very high reading", [90.0, 90.0], -1),
]

for name, features, expected in examples:
    predicted = int(model.predict([features])[0])
    print(f"{name}: expected {expected}, model predicted {predicted}")
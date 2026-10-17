from pathlib import Path

import joblib


MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "isolation_forest_candidate.joblib"
)


def evaluate_candidate():
    model = joblib.load(MODEL_PATH)

    examples = [
        ("ordinary reading", [0.56, 15.63], 1),
        ("very high reading", [90.0, 90.0], -1),
    ]

    for name, features, expected in examples:
        predicted = int(model.predict([features])[0])
        print(f"{name}: expected {expected}, got {predicted}")

        if predicted != expected:
            raise ValueError(f"Candidate check failed for: {name}")

    print("Candidate checks passed")


if __name__ == "__main__":
    evaluate_candidate()
from pathlib import Path

import joblib
from sklearn.ensemble import IsolationForest

from aiops.prepare_data import load_features, split_features


def train_model():
    features = load_features()

    if len(features) < 2:
        raise ValueError("Need at least two metric snapshots")

    training_features, validation_features = split_features(features)

    model = IsolationForest(random_state=42, contamination=0.01)
    model.fit(training_features)

    validation_predictions = model.predict(validation_features)
    normal_count = list(validation_predictions).count(1)
    unusual_count = list(validation_predictions).count(-1)

    return model, len(training_features), len(validation_features), normal_count, unusual_count


if __name__ == "__main__":
    model, training_count, validation_count, normal_count, unusual_count = train_model()

    print(f"Training snapshots: {training_count}")
    print(f"Validation snapshots: {validation_count}")
    print(f"Validation readings classified as normal: {normal_count}")
    print(f"Validation readings flagged as unusual: {unusual_count}")

    model_path = Path("models/isolation_forest_candidate.joblib")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"Saved candidate model to {model_path}")
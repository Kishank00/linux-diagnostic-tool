import csv
from pathlib import Path

METRICS_FILE = Path("data/metrics-baseline.csv")


def load_features(path=METRICS_FILE):
    features = []

    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Skip an incomplete row, if the CSV contains one.
            if not row.get("timestamp"):
                continue

            # CSV values are text, so convert the two metric values to numbers.
            cpu = float(row["cpu_usage_percent"])
            memory = float(row["memory_usage_percent"])

            features.append([cpu, memory])

    return features

def split_features(features, train_ratio=0.8):
    split_index = int(len(features) * train_ratio)

    train_features = features[:split_index]
    validation_features = features[split_index:]

    if not train_features or not validation_features:
        raise ValueError("Need training and validation snapshots")

    return train_features, validation_features


if __name__ == "__main__":
    rows = load_features()
    train_features, validation_features = split_features(rows)

    print(f"Loaded {len(rows)} snapshots")
    print(f"Training snapshots: {len(train_features)}")
    print(f"Validation snapshots: {len(validation_features)}")
import csv
from pathlib import Path

PREDICTIONS_FILE = Path("data/anomaly_predictions.csv")


def summarize_predictions():
    with PREDICTIONS_FILE.open(newline="") as file:
        rows = list(csv.DictReader(file))

    total = len(rows)
    cpu_flags = sum(row["high_cpu"] == "True" for row in rows)
    memory_flags = sum(row["high_memory"] == "True" for row in rows)
    ml_flags = sum(row["ml_anomaly"] == "True" for row in rows)

    print(f"Total API predictions: {total}")
    print(f"High CPU flags: {cpu_flags}")
    print(f"High memory flags: {memory_flags}")
    print(f"ML anomaly flags: {ml_flags}")


if __name__ == "__main__":
    summarize_predictions()
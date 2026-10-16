import csv
from pathlib import Path

def append_snapshot(snapshot: dict, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not output_path.exists() or output_path.stat().st_size == 0

    with output_path.open("a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=snapshot.keys())

        if write_header is True:
            writer.writeheader()

        writer.writerow(snapshot)

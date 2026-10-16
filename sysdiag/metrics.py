from datetime import datetime, timezone
import time
from sysdiag.anomaly import is_cpu_high

from sysdiag.cpu import cpu_usage, load_diagnostics
from sysdiag.memory import read_memory_info
from sysdiag.storage import append_snapshot

def collect_metrics():
    date_time = datetime.now(timezone.utc).isoformat()
    cpu_percent = cpu_usage()
    load = load_diagnostics()
    memory = read_memory_info()

    if memory["mem_total"] == 0:
        raise ValueError("Total memory must be greater than zero")
    
    memory_percent = round(
        ((memory["mem_total"] - memory["mem_available"])
        / memory["mem_total"]
        * 100), 2
    )
    return {
        "timestamp": date_time,
        "cpu_usage_percent": cpu_percent,
        "load_1m": load["load_1m"],
        "load_5m": load["load_5m"],
        "load_15m": load["load_15m"],
        "memory_usage_percent": memory_percent,
    }

if __name__ == "__main__":
    while True:
        snapshot = collect_metrics()
        print("High CPU:", is_cpu_high(snapshot))
        append_snapshot(snapshot, "data/metrics.csv")
        print(snapshot)
        time.sleep(10)
from unittest.mock import patch
from datetime import datetime, timezone

from sysdiag.metrics import collect_metrics


def test_collect_metrics():
    with (
        patch("sysdiag.metrics.cpu_usage", return_value=12.5),
        patch("sysdiag.metrics.load_diagnostics", return_value={
            "load_1m": 1.0,
            "load_5m": 0.8,
            "load_15m": 0.6,
        }),
        patch("sysdiag.metrics.read_memory_info", return_value={
            "mem_total": 1000,
            "mem_available": 250,
            "swap_total": 0,
        }),
    ):
        snapshot = collect_metrics()

    assert snapshot["cpu_usage_percent"] == 12.5
    assert snapshot["memory_usage_percent"] == 75.0
    assert snapshot["load_1m"] == 1.0
    assert snapshot["load_5m"] == 0.8
    assert snapshot["load_15m"] == 0.6
    timestamp = datetime.fromisoformat(snapshot["timestamp"])
    assert timestamp.tzinfo == timezone.utc
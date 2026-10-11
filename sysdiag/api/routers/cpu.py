from fastapi import APIRouter

from sysdiag.cpu import (
    read_logical_cpu_count,
    cpu_usage,
    load_diagnostics,
)

router = APIRouter(prefix="/cpu", tags=["cpu"])

@router.get("/")
def get_cpu_diagnostics():
    logical_cpus = read_logical_cpu_count()
    usage = cpu_usage()
    load_info = load_diagnostics()

    return {
        "logical_cpus": logical_cpus,
        "cpu_usage_percent": usage,
        "load_1m": load_info["load_1m"],
        "load_5m": load_info["load_5m"],
        "load_15m": load_info["load_15m"],
    }
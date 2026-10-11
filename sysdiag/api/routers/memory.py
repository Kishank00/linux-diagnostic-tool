from fastapi import APIRouter

from sysdiag.memory import read_memory_info

router = APIRouter(prefix="/memory", tags=["memory"])

@router.get("/")
def get_memory_diagnostics():
    memory_info = read_memory_info()
    total_memory_gib = memory_info["mem_total"] / (1024 ** 2)
    available_memory_gib = memory_info["mem_available"] / (1024 ** 2)
    used_memory_gib = (memory_info["mem_total"] - memory_info["mem_available"]) / (1024 ** 2)

    memory_usage_percentage = ((total_memory_gib - available_memory_gib) / total_memory_gib) * 100

    return {
        "total_memory_gib": round(total_memory_gib, 2),
        "avalable_memory_gib": round(available_memory_gib, 2),
        "used_memory_gib": round(used_memory_gib, 2),
        "memory_usage_percentage": round(memory_usage_percentage, 2),
        # swap_total_gib
        # swap_enabled
    }
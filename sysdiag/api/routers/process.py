from fastapi import APIRouter, HTTPException

from sysdiag.process import top_memory_processes, read_process_info, get_all_process_info

router = APIRouter(prefix="/processes", tags=["processes"])

@router.get("/")
def get_all_processes():
    processes = get_all_process_info()
    return processes

@router.get("/top-memory")
def get_top_memory_process():
    processes = top_memory_processes()
    return processes

@router.get("/{pid}")
def get_process_details(pid: int):
    process_details = read_process_info(pid)
    if process_details is None:
        raise HTTPException(
            status_code=404,
            detail= f"Process with PID {pid} Not Found"
        )
    return process_details
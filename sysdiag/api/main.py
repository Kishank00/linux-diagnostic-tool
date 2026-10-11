from fastapi import FastAPI
from .routers import health, cpu, memory, process, disk

app = FastAPI(title="Linux Diagnostic Tool API")

app.include_router(health.router)
app.include_router(cpu.router)
app.include_router(memory.router)
app.include_router(process.router)
app.include_router(disk.router)
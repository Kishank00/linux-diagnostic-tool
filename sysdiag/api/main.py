from fastapi import FastAPI
from .routers import health, cpu, memory, process, disk, anomalies

app = FastAPI(title="Linux Diagnostic Tool API", version="0.2.0")

app.include_router(health.router)
app.include_router(cpu.router)
app.include_router(memory.router)
app.include_router(process.router)
app.include_router(disk.router)
app.include_router(anomalies.router)

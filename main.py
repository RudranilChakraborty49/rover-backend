# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from datetime import datetime

app = FastAPI()

# Allow mobile app to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

events = []

@app.post("/api/rover/update")
async def update(data: Dict[str, Any]):
    events.append({"time": datetime.utcnow().isoformat() + "Z", "data": data})
    return {"status": "ok"}

@app.get("/api/reports")
async def reports(limit: int = 10):
    return events[-limit:]
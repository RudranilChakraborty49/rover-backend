# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from datetime import datetime

# Create the FastAPI app
app = FastAPI(
    title="Rover Security API",
    description="Backend for hazard & person detection system",
    version="1.0.0"
)

# Enable CORS so your React website can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites (OK for now)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # All headers
)

# In-memory storage for events (will reset when server restarts)
events = []

# ✅ Root endpoint — shows a friendly message
@app.get("/", summary="Health check")
async def root():
    return {
        "status": "success",
        "message": "✅ Rover Backend is LIVE!",
        "docs": "/docs"
    }

# 📥 Endpoint: Raspberry Pi sends detection data
@app.post("/api/rover/update", summary="Receive detection data from Pi")
async def receive_rover_data(data: Dict[str, Any]):
    """
    Accepts data from Raspberry Pi in this format:
    {
      "person_1": {
        "person_name": "Priyanshu Roy",
        "is_known": true,
        "suspicious_level": "High",
        "detected_items": ["knife"],
        "detected_action": "furtive"
      }
    }
    """
    timestamped_event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": data
    }
    events.append(timestamped_event)
    return {"status": "success", "events_received": len(data)}

# 📤 Endpoint: Website fetches historical reports
@app.get("/api/reports", summary="Get detection history")
async def get_reports(limit: int = 50):
    """
    Returns last N events (default: 50)
    """
    return events[-limit:]
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# --- DATABASE SETUP ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EventLog(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, default=lambda: datetime.utcnow().isoformat() + "Z")
    data = Column(JSON)  # stores your full detection dict

# Create tables (safe to run multiple times)
Base.metadata.create_all(bind=engine)

# --- FASTAPI APP ---
app = FastAPI(
    title="Rover Security API with DB",
    description="Now with PostgreSQL!"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "✅ Backend with PostgreSQL is LIVE!"}

@app.post("/api/rover/update")
async def receive_rover_data(data: dict):
    db = SessionLocal()
    try:
        event = EventLog(data=data)
        db.add(event)
        db.commit()
        return {"status": "success", "event_id": event.id}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    finally:
        db.close()

@app.get("/api/reports")
async def get_reports(limit: int = 50):
    db = SessionLocal()
    try:
        events = db.query(EventLog).order_by(EventLog.id.desc()).limit(limit).all()
        return [
            {
                "id": e.id,
                "timestamp": e.timestamp,
                "data": e.data
            }
            for e in events
        ]
    finally:
        db.close()
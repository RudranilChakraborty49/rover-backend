# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List
import os

# --- DATABASE (PostgreSQL on Render) ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- TABLE MODELS ---
class EventLog(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, default=lambda: __import__('datetime').datetime.utcnow().isoformat() + "Z")
    data = Column(JSON)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    position = Column(String)
    department = Column(String)
    phone = Column(String)
    email = Column(String)
    face_image = Column(String)

# Create tables (safe to run multiple times)
Base.metadata.create_all(bind=engine)

# --- FASTAPI APP ---
app = FastAPI(
    title="Rover Security API",
    description="Hazard detection + Employee management on PostgreSQL"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- HAZARD ENDPOINTS ---
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
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/reports")
async def get_reports(limit: int = 50):
    db = SessionLocal()
    try:
        events = db.query(EventLog).order_by(EventLog.id.desc()).limit(limit).all()
        return [{"id": e.id, "timestamp": e.timestamp, "data": e.data} for e in events]
    finally:
        db.close()

# --- EMPLOYEE ENDPOINTS ---
@app.get("/api/employees", response_model=List[dict])
async def get_all_employees():
    db = SessionLocal()
    try:
        employees = db.query(Employee).order_by(Employee.name).all()
        return [
            {
                "id": e.id,
                "employee_id": e.employee_id,
                "name": e.name,
                "position": e.position,
                "department": e.department,
                "phone": e.phone,
                "email": e.email,
                "face_image": e.face_image
            }
            for e in employees
        ]
    finally:
        db.close()

@app.post("/api/employees")
async def add_employee(emp: dict):
    required = ["employee_id", "name"]
    if not all(k in emp for k in required):
        raise HTTPException(status_code=400, detail="Missing required fields: employee_id, name")
    
    db = SessionLocal()
    try:
        new_emp = Employee(
            employee_id=emp["employee_id"],
            name=emp["name"],
            position=emp.get("position", ""),
            department=emp.get("department", ""),
            phone=emp.get("phone", ""),
            email=emp.get("email", ""),
            face_image=emp.get("face_image", "")
        )
        db.add(new_emp)
        db.commit()
        return {"status": "success", "id": new_emp.id}
    except Exception as e:
        db.rollback()
        if "UNIQUE constraint" in str(e) or "unique constraint" in str(e).lower():
            raise HTTPException(status_code=400, detail="Employee ID already exists")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.put("/api/employees/{emp_id}")
async def update_employee(emp_id: int, update_data: dict):
    db = SessionLocal()
    try:
        emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        for key, value in update_data.items():
            if hasattr(emp, key):
                setattr(emp, key, value)
        
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.delete("/api/employees/{emp_id}")
async def delete_employee(emp_id: int):
    db = SessionLocal()
    try:
        emp = db.query(Employee).filter(Employee.id == emp_id).first()
        if not emp:
            raise HTTPException(status_code=404, detail="Employee not found")
        db.delete(emp)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
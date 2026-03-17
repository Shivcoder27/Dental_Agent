from fastapi import FastAPI

from app.database.base import Base
from app.database.db_connection import engine, SessionLocal

import app.database.models

from app.api import patient_routes
from app.rag.retriever import load_patients
from app.api import appointment_routes

from app.scheduler.reminder_scheduler import start_scheduler


app = FastAPI(
    title="Dental AI Agent",
    version="1.0"
)


@app.on_event("startup")
def startup():

    db = SessionLocal()

    load_patients(db)

    db.close()

    start_scheduler()


Base.metadata.create_all(bind=engine)

app.include_router(patient_routes.router)
app.include_router(appointment_routes.router)


@app.get("/")
def home():
    return {"message": "Dental AI Agent Backend Running"}
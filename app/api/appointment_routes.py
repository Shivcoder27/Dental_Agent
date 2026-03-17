from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db_connection import get_db
from app.schemas.appointment_schema import AppointmentCreate
from app.services.appointment_service import schedule_appointment

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/")
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):

    result = schedule_appointment(db, data)

    return result
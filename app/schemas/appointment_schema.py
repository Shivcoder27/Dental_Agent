from pydantic import BaseModel
from datetime import datetime


class AppointmentCreate(BaseModel):

    patient_id: int
    treatment: str
    appointment_time: datetime
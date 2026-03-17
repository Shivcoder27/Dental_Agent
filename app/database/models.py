from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Patient(Base):

    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    phone = Column(String(15), unique=True)

    age = Column(Integer)
    gender = Column(String(10))

    created_at = Column(DateTime, default=datetime.utcnow)

class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    treatment = Column(String(100))

    appointment_time = Column(DateTime, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")
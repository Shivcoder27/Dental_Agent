from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.models import Appointment, Patient


def create_appointment(db: Session, data):

    start = data.appointment_time
    end = start + timedelta(minutes=15)

    existing = db.query(Appointment).filter(
        Appointment.appointment_time >= start,
        Appointment.appointment_time < end
    ).all()

    if len(existing) >= 2:

        patient = db.query(Patient).filter(Patient.id == existing[0].patient_id).first()

        return {
            "error": f"There is already meeting at {existing[0].appointment_time} with patient ID {patient.id} name {patient.name}"
        }

    appointment = Appointment(
        patient_id=data.patient_id,
        treatment=data.treatment,
        appointment_time=data.appointment_time
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment
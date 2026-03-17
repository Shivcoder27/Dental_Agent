from sqlalchemy.orm import Session
from app.database.appointment_repository import create_appointment

from app.services.sms_service import send_sms
from app.database.patient_repository import get_patient_by_id


def schedule_appointment(db, data):

    appointment = create_appointment(db, data)

    if isinstance(appointment, dict):
        return appointment

    patient = get_patient_by_id(db, data.patient_id)

    message = f"""
Appointment Confirmation: Amravati Dental Clinic

Dear {patient.name} (ID: {patient.id}),

This is a reminder for your upcoming appointment at
Amravati Dental Clinic for your {data.treatment}.

Date: {data.appointment_time.date()}
Time: {data.appointment_time.strftime("%I:%M %p")}

Location: Amravati Dental Clinic

Please arrive 10 minutes early.
See you soon!

Amravati Dental Clinic
"""

    send_sms(patient.phone, message)

    return appointment
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.database.db_connection import SessionLocal
from app.database.models import Appointment, Patient
from app.services.sms_service import send_sms

scheduler = BackgroundScheduler()


def check_appointments():

    db = SessionLocal()

    now = datetime.now()

    appointments = db.query(Appointment).all()

    for a in appointments:

        reminder_time = a.appointment_time - timedelta(hours=5)

        if reminder_time <= now <= reminder_time + timedelta(minutes=10):

            patient = db.query(Patient).filter(Patient.id == a.patient_id).first()

            message = f"""
Appointment Reminder: Amravati Dental Clinic

Dear {patient.name} (ID: {patient.id}),

This is a reminder for your upcoming appointment.

Treatment: {a.treatment}

Date: {a.appointment_time.date()}
Time: {a.appointment_time.strftime("%I:%M %p")}

Location: Amravati Dental Clinic

Please arrive 10 minutes early.

Amravati Dental Clinic
"""

            send_sms(patient.phone, message)

    db.close()


def start_scheduler():

    scheduler.add_job(check_appointments, "interval", minutes=10)

    scheduler.start()
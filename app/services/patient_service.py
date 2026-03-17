from sqlalchemy.orm import Session
from app.database import patient_repository


def create_patient(db: Session, patient):
    return patient_repository.create_patient(db, patient)


def get_patients(db: Session):
    return patient_repository.get_all_patients(db)


def get_patient(db: Session, patient_id: int):
    return patient_repository.get_patient_by_id(db, patient_id)
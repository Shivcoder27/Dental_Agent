from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.patient_schema import PatientCreate
from app.services import patient_service
from app.database.db_connection import get_db
from app.database.models import Patient

router = APIRouter(prefix="/patients", tags=["Patients"])


# -------------------------
# CREATE PATIENT
# -------------------------
@router.post("/")
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return patient_service.create_patient(db, patient)


# -------------------------
# GET ALL PATIENTS
# -------------------------
@router.get("/")
def get_patients(db: Session = Depends(get_db)):
    return patient_service.get_patients(db)


# -------------------------
# GET PATIENT BY ID
# -------------------------
@router.get("/{patient_id}")
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_service.get_patient(db, patient_id)


# -------------------------
# UPDATE PATIENT
# -------------------------
@router.put("/{patient_id}")
def update_patient(patient_id: int, patient: PatientCreate, db: Session = Depends(get_db)):

    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db_patient.name = patient.name
    db_patient.phone = patient.phone
    db_patient.age = patient.age
    db_patient.gender = patient.gender

    db.commit()
    db.refresh(db_patient)

    return {
        "message": "Patient updated successfully",
        "patient": db_patient
    }


# -------------------------
# DELETE PATIENT BY ID
# -------------------------
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):

    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(db_patient)
    db.commit()

    return {"message": f"Patient ID {patient_id} deleted successfully"}
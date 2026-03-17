from app.database.patient_repository import get_all_patients
from app.rag.vector_store import add_document


def load_patients(db):

    patients = get_all_patients(db)

    for p in patients:

        text = f"""
Patient name: {p.name}
Age: {p.age}
Phone: {p.phone}
Gender: {p.gender}
"""

        add_document(text)
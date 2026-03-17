from app.database.db_connection import SessionLocal
from app.database.models import Patient
from app.integrations.gemini_client import ask_gemini


def answer_query(question):

    db = SessionLocal()

    patients = db.query(Patient).all()

    if not patients:
        return "No patient data available."

    context = ""

    for p in patients:
        context += f"""
Patient name: {p.name}
Age: {p.age}
Phone: {p.phone}
Gender: {p.gender}
"""

    db.close()

    prompt = f"""
You are a dental clinic assistant.

Use the patient data below to answer the question.

Patient Data:
{context}

Question:
{question}
"""

    return ask_gemini(prompt)
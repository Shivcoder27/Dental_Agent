from app.integrations.gemini_client import ask_gemini


def extract_appointment(message):

    prompt = f"""
Extract appointment information.

Return JSON only.

Format:

{{
"patient_id": 1,
"treatment": "tooth pain",
"appointment_time": "2026-04-10 17:00:00"
}}

Message:
{message}
"""

    return ask_gemini(prompt)
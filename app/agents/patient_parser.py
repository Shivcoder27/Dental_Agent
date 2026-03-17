from app.integrations.gemini_client import ask_gemini


def extract_patient_data(message):

    prompt = f"""
Extract patient details from the text.

Return STRICT JSON only.

Example output:
{{
"name": "Rahul",
"phone": "9876543210",
"age": 30,
"gender": "Male"
}}

Text:
{message}
"""

    return ask_gemini(prompt)
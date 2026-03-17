import json
import re
from app.agents.patient_parser import extract_patient_data


def parse_patient_message(message):

    response = extract_patient_data(message)

    try:
        # remove markdown ```json ```
        cleaned = re.sub(r"```json|```", "", response).strip()

        data = json.loads(cleaned)

        return data

    except Exception as e:
        print("AI parsing error:", response)
        return None
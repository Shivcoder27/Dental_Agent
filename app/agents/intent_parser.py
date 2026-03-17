import json
import re
from app.integrations.gemini_client import ask_gemini


def parse_intent(message):

    prompt = f"""
You are an AI assistant for a dental clinic system.

Identify the user intent.

Possible intents:
create_patient
delete_patient
get_patient
update_patient
history_query
appointment
unknown

Extract parameters if present.

Return STRICT JSON only.

Example outputs:

User: delete rocky patient id 12

{{
 "intent": "delete_patient",
 "patient_id": 12,
 "name": "rocky",
 "phone": null,
 "age": null,
 "gender": null
}}

User: show mok data

{{
 "intent": "get_patient",
 "patient_id": null,
 "name": "mok",
 "phone": null,
 "age": null,
 "gender": null
}}

User message:
{message}
"""

    response = ask_gemini(prompt)

    if not response:
        return {"intent": "unknown"}

    try:
        # remove markdown ```json ```
        response = re.sub(r"```json|```", "", response)

        data = json.loads(response)

        return data

    except Exception as e:

        print("Intent parse error:", response)

        return {"intent": "unknown"}
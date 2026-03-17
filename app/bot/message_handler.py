from app.services.ai_service import parse_patient_message
import requests

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    data = parse_patient_message(text)

    if data:

        response = requests.post(
            "http://127.0.0.1:8000/patients/",
            json=data
        )

        if response.status_code == 200:
            await update.message.reply_text("Patient added successfully")
        else:
            await update.message.reply_text("Error adding patient")

    else:
        await update.message.reply_text("I could not understand the message")
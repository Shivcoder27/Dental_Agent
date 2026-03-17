import os
import json
import requests

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from app.utils.conversation_memory import save_message, get_history
from app.agents.appointment_parser import extract_appointment
from app.agents.intent_parser import parse_intent
from app.rag.vector_store import add_document

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dental AI Agent Bot Ready")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    print("User message:", text)

    text_lower = text.lower()

    # Greeting
    if text_lower in ["hi", "hello", "hey"]:
        await update.message.reply_text(
            "Hello 👋 I am your Dental Clinic Assistant.\n\n"
            "You can ask me to:\n"
            "• Add patient\n"
            "• Schedule appointment\n"
            "• Show patient history\n"
        )
        return

    intent_data = parse_intent(text_lower) or {"intent": "unknown"}
    intent = intent_data.get("intent")

    user_id = update.message.chat_id
    save_message(user_id, text)
    history = get_history(user_id)

    # -------------------------
    # CREATE PATIENT
    # -------------------------
    if intent == "create_patient":

        name = intent_data.get("name")
        phone = intent_data.get("phone")
        age = intent_data.get("age")
        gender = intent_data.get("gender")

        if not name or not phone:
            await update.message.reply_text(
                "Please provide patient name and phone number."
            )
            return

        payload = {
            "name": name,
            "phone": str(phone),
            "age": age,
            "gender": gender
        }

        response = requests.post(
            "http://127.0.0.1:8000/patients/",
            json=payload
        )

        if response.status_code in [200, 201]:

            doc_text = f"""
Patient name: {name}
Age: {age}
Phone: {phone}
Gender: {gender}
"""

            add_document(doc_text)

            await update.message.reply_text(
                f"Patient {name} created successfully"
            )

        else:
            print("API error:", response.text)
            await update.message.reply_text("Error creating patient")

        return

    # -------------------------
    # DELETE PATIENT
    # -------------------------
    if intent == "delete_patient":

        patient_id = intent_data.get("patient_id")

        if not patient_id:
            await update.message.reply_text(
                "Please provide the patient ID to delete."
            )
            return

        response = requests.delete(
            f"http://127.0.0.1:8000/patients/{patient_id}"
        )

        if response.status_code == 200:
            await update.message.reply_text(
                f"Patient ID {patient_id} deleted successfully"
            )
        else:
            await update.message.reply_text("Patient not found")

        return

    # -------------------------
    # GET PATIENT
    # -------------------------
    if intent == "get_patient":

        patient_id = intent_data.get("patient_id")

        if not patient_id:
            await update.message.reply_text("Please provide patient ID.")
            return

        response = requests.get(
            f"http://127.0.0.1:8000/patients/{patient_id}"
        )

        if response.status_code == 200:

            data = response.json()

            msg = f"""
Patient ID: {data['id']}
Name: {data['name']}
Age: {data['age']}
Phone: {data['phone']}
Gender: {data['gender']}
"""

            await update.message.reply_text(msg)

        else:
            await update.message.reply_text("Patient not found")

        return

    # -------------------------
    # APPOINTMENT
    # -------------------------
    if "appointment" in text_lower:

        try:

            result = extract_appointment(text)

            clean = result.replace("```json", "").replace("```", "").strip()

            data = json.loads(clean)

            response = requests.post(
                "http://127.0.0.1:8000/appointments/",
                json=data
            )

            res = response.json()

            if "error" in res:
                await update.message.reply_text(res["error"])
            else:
                await update.message.reply_text("Appointment scheduled")

            return

        except Exception as e:
            print("Appointment error:", e)
            await update.message.reply_text("Could not schedule appointment")
            return

    # -------------------------
    # UNKNOWN
    # -------------------------
    await update.message.reply_text(
        "I could not understand your request. Please try again."
    )


def run_bot():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram Bot Running...")

    app.run_polling()
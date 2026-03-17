import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_sms(phone, message):

    try:

        sms = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to="+91" + phone
        )

        print("SMS SENT:", sms.sid)

    except Exception as e:

        print("SMS ERROR:", e)








# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("FAST2SMS_API_KEY")


# def send_sms(phone, message):

#     url = "https://www.fast2sms.com/dev/bulkV2"

#     payload = {
#         "route": "q",
#         "message": message,
#         "numbers": phone
#     }

#     headers = {
#         "authorization": API_KEY
#     }

#     requests.post(url, data=payload, headers=headers)
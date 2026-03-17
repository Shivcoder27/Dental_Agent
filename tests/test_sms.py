import requests

API_KEY = "5BIWDKAJ1m8iUaTpPZRfM7b3ChvONwnrQqo46ezEySs9c0gtYLFexTW20hAa1OpJ6GnjucP3kmRXdYMs"

url = "https://www.fast2sms.com/dev/bulkV2"

payload = {
    "route": "q",
    "message": "Test message from Dental Agent",
    "numbers": "6398651236"
}

headers = {
    "authorization": API_KEY
}

response = requests.post(url, data=payload, headers=headers)

print(response.text)
import os
import requests
from dotenv import load_dotenv


load_dotenv()
URL = "https://api.brevo.com/v3/smtp/email"
headers = {
    "accept": "application/json",
    "api-key": os.getenv("BREVO_API_KEY"),
    "content-type": "application/json"
}

def send_email(receiver_email, receiver_name, html_content):
    payload = {
        "sender": {
            "name": "Code Blue CPR Services",
            "email": os.getenv("SENDER_EMAIL")
        },
        "to": [
            {
                "email": receiver_email,
                "name": receiver_name
            }
        ],
        "subject": f"New Student Enrollment",
        "htmlContent": html_content
    }

    try:
        response = requests.post(URL, json=payload, headers=headers)
        if response.status_code == 201:
            print("Email sent successfully!")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection Error: {e}")

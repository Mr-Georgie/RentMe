import requests
from django.conf import settings

url = "https://api.sendinblue.com/v3/smtp/email"
                

def send_email(data):

    payload = {
        "sender": {
            "name": "George from RentMe",
            "email": "chetamdavies@gmail.com"
        },
        "to": [
            {
                "email": data['send_to'],
            }
        ],
        "headers": {"Authorization": f"Bearer {settings.SIB_API_KEY}"},
        "tags": ["RentMe App"],
        "htmlContent": f"<!DOCTYPE html> <html> <body> {data['email_body']} </body> </html>",
        "subject": data['email_subject']
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": f"{settings.SIB_API_KEY}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)
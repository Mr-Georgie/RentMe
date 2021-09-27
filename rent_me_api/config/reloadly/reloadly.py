import requests
import json
from django.conf import settings

# for live mode, audience = "https://topups.reloadly.com"


def get_authenticated():
    url = "https://auth.reloadly.com/oauth/token"

    payload = json.dumps({
    "client_id": settings.RELOADLY_CLIENT_ID,
    "client_secret": settings.RELOADLY_CLIENT_SECRET,
    "grant_type": "client_credentials",
    "audience": "https://topups-sandbox.reloadly.com" 
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

def topup_product_owner(random_string, operator_id, receiver_num, receiver_country, amount, sender_num, sender_country, access_token):
    
    url = "https://topups-sandbox.reloadly.com/topups"

    payload = json.dumps({
    "operatorId": operator_id,
    "amount": str(amount),
    "customIdentifier": "RentMe-"+random_string,
    "recipientPhone": {
        "countryCode": receiver_country,
        "number": receiver_num
    },
    "senderPhone": {
        "countryCode": sender_country,
        "number": sender_num
    }
    
    })
    headers = {
    'Authorization': 'Bearer '+access_token,
    'Accept': 'application/com.reloadly.topups-v1+json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)
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

def topup_product_owner(random_string,receiver_cty, receiver_num, sender_cty, sender_num, access_token):
    rc = receiver_cty
    sc = sender_cty
    
    url = "https://topups-sandbox.reloadly.com/topups"

    payload = json.dumps({
    "operatorId": "341",
    "amount": "100",
    "customIdentifier": "RentMe-"+random_string,
    "recipientPhone": {
        "countryCode": "NG",
        "number": "08131191073"
    },
    # "recipientPhone": { for live server
    #     "countryCode": receiver_cty,
    #     "number": receiver_num
    # },
    # "senderPhone": { for live server
    #     "countryCode": sender_cty,
    #     "number": sender_num
    # }
    "senderPhone": {
        "countryCode": "NG",
        "number": "08144149628"
    }
    
    })
    headers = {
    'Authorization': 'Bearer '+access_token,
    'Accept': 'application/com.reloadly.topups-v1+json',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)
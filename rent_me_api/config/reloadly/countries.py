import requests
import json
from .reloadly import get_authenticated

def get_countries(token):
    url = f"https://topups-sandbox.reloadly.com/countries?page=1&size=1"

    access_token = token

    payload={}
    headers = {
    'Accept': 'application/com.reloadly.topups-v1+json',
    'Authorization': 'Bearer '+access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_resp = json.loads(response.text)
    
    return json_resp
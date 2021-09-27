import requests
import json

def get_operator(phone,iso_code, token):
    url = (f"https://topups-sandbox.reloadly.com/operators/auto-detect/phone/" +
            f"{phone}/countries/{iso_code}")

    payload={}
    headers = {
    'Authorization': 'Bearer '+ token,
    'Accept': 'application/com.reloadly.topups-v1+json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    json_resp = json.loads(response.text)
    
    print(json_resp["operatorId"])
    print(json_resp["name"])
    
    return json_resp["operatorId"]
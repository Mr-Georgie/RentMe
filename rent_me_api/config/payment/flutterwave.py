import requests



def verify_transaction(id, secret_key):
    api_url = "https://api.flutterwave.com/v3/transactions?transaction_id="+id
    request_type = "GET"
    response = requests.request(request_type, api_url, 
                                    headers={'Authorization': 'Bearer '+ secret_key})
    return response.json()
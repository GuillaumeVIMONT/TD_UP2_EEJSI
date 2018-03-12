import requests
import json

r = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
bitcoin_data = dict(r.json())
bitcoin_value = bitcoin_data["bpi"]["USD"]["rate_float"]
print(bitcoin_value)


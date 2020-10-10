#!/usr/bin/env python
'''
CocoeoSTB b0.02
'''
# Import librarys
# ------------------------------------------------------------------------------
import urllib.request
import requests
import json
from time import time
from datetime import datetime # Get the time and date of computer to set the timer.
try:
    import winsound
except ImportError:
    # Fake winsound lets you call Beep/PlaySound/MessageBeep without doing anything
    winsound = type('', (), {'__getattr__': lambda *a: lambda *a, **kw: None})()
    
# Constants
# ------------------------------------------------------------------------------

ENDPOINTS = {
    'getTimestamp': 'https://api.switcheo.network/v2/exchange/timestamp',
    'getStatus': 'https://api.switcheo.network',
    'postOrder': 'https://api.switcheo.network/v2/orders',
}
RUN = True
posttOrder = 'https://api.switcheo.network/v2/orders'
address = 'AbDZkiytXNAranqEx4E9FiBYVXWZvmjK5m'
privateKey = 'KytWa3tcq1iBmMRD1dGrdomyeULD4p6foi9hB4FHDPdFbcA7M'

# Function definitions
# ------------------------------------------------------------------------------

def get_json(url):
    '''
    Get utf-8-encoded json from a given url, and return a python object
    '''
    with urllib.request.urlopen(url) as req:
        return json.loads(req.read().decode())


# Welcome message and check actual time/date.
# ------------------------------------------------------------------------------

timestamp = get_json(ENDPOINTS['getTimestamp'])
for v in timestamp.values(): # Get the raw value from the dictionary and write it in the value "v";.
        t = int(v/1000) # Convert timestamp to a usable timestamp (switcheo give too precise one to convert in date format without errors).
        timeActual = datetime.fromtimestamp(t) # Get correct transaction timestamp, convert it to date time.
        print('*****     CocoeoSTB b0.02     *****')# Welcome message
        print('CHECK YOUR COMPUTER Time/Date SYNC FOR FULL EFFICIENCY:', timeActual)

status = get_json(ENDPOINTS['getStatus'])
print ('Status of network','-------------',status['status'],'-------------')
print ('')

# Core Code
# ------------------------------------------------------------------------------

myobj = "{"pair": "SWTH_NEO", "blockchain": "neo", "side": "sell",
"price": "0.001601",
  "quantity": "40000000000",
  "use_native_tokens": false,
  "order_type": "limit",
  "timestamp": timestamp['timestamp'],
  "contract_hash": "<contract hash>",
  "address": "87cf67daa0c1e9b6caa1443cf5555b09cb3f8e5f",
  "signature": "<signature>"
}"

r = requests.post(url = posttOrder, data = myobj)
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)


    

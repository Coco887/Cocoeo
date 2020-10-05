#!/usr/bin/env python
'''
CocoeoSTB b0.02
'''
# Import librarys
# ------------------------------------------------------------------------------
import urllib.request
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
    'user.privateKey': 'KytWa3tcq1iBmMRD1dGrdomyeULD4p6foi9hB4FHDPdFbcA7M',
    'getTimestamp': 'https://api.switcheo.network/v2/exchange/timestamp',
    'getStatus': 'https://api.switcheo.network',    
}
RUN = True

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
winsound.Beep(350, 350)
winsound.Beep(250, 250)

# Core Code
# ------------------------------------------------------------------------------
#while RUN:

try:
    function createOrder({
        pair: 'SWTH_NEO',
        blockchain: 'neo',
        address: user.address,
        side: 'buy',
        price: (0.001340).toFixed(8),
        quantity: toAssetAmount(1000, 'SWTH'),
        useNativeTokens: true,
        orderType: 'limit',
        privateKey: user.privateKey
        })
    const signableParams = { pair, blockchain, side, price, quantity,
                             useNativeTokens, orderType, timestamp: getTimestamp(),
                             contractHash: CONTRACT_HASH }
    const signature = signParams(signableParams, privateKey)
    const apiParams = { ...signableParams, address, signature }
    return api.post(https://api.switcheo.network/v2 + '/orders', apiParams)
}
        
    

    

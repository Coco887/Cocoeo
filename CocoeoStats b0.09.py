#!/usr/bin/env python
'''
delegatorsListing b0.09
'''

# Import librarys
# ------------------------------------------------------------------------------
import csv
import time
import json
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import time
try:
    import winsound
except ImportError:
    # Fake winsound lets you call Beep/PlaySound/MessageBeep without doing anything
    winsound = type('', (), {'__getattr__': lambda *a: lambda *a, **kw: None})()


ENDPOINTS = {
    'profile': 'https://tradescan.switcheo.org/get_profile?account=%s',
    'validators': 'https://tradescan.switcheo.org/get_all_validators',
    'validator_delegations': 'https://tradescan.switcheo.org/staking/validators/%s/delegations'
}


def get_json(url):
    with urllib.request.urlopen(url) as req:
        return json.loads(req.read().decode())


def get_profile(k_v):
    addr, total = k_v
    total = int(total / 100000000)
    payload = get_json(ENDPOINTS['profile'] % addr)
    last_seen = datetime.fromisoformat(payload['last_seen_time'][:19])
    return [addr, last_seen, total]


# Init time
# ------------------------------------------------------------------------------
initTime = int(time())
print(initTime)


# Get all delegators from all bonded validators
# ------------------------------------------------------------------------------
validators = [d for d in get_json(ENDPOINTS['validators']) if d['bond_status'] == 'bonded']
delegators = defaultdict(int)

for v in validators:
    for i, d in enumerate(get_json(ENDPOINTS['validator_delegations'] % v['operator_address'])['result']):
        delegators[d['delegator_address']] += float(d['balance']['amount'])
    print(f'+{i+1:4} delegator totals from {v["description"]["moniker"]}')


# Get all delegators profiles to find the last_seen time
# ------------------------------------------------------------------------------
with open('delegator_info.csv', 'w') as f:
    writer = csv.writer(f)

    with ThreadPoolExecutor(max_workers=8) as executor:
        for row in executor.map(get_profile, delegators.items()):
            writer.writerow(row)
            print(*row)


# End of process alerter and duration
# ------------------------------------------------------------------------------
newTimestamp = int(time())
processTime = newTimestamp - initTime
print('Snapshot Duration:', processTime, 'seconds')
winsound.Beep(550, 250)
winsound.Beep(650, 350)

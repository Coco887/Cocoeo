#!/usr/bin/env python
'''
delegatorsListing b0.05
'''

# Import librarys
# ------------------------------------------------------------------------------
import csv
import time
import json
import urllib.request
from datetime import datetime
try:
    import winsound
except ImportError as e: print(e)

ENDPOINTS = {
    'delegations': 'https://tradescan.switcheo.org/staking/delegators/%s/delegations',
    'profile': 'https://tradescan.switcheo.org/get_profile?account=%s',
}
FILENAMES = [
    '03labsDelegators.txt',
    'b2sDelegators.txt',
    'blockhuntersDelegators.txt',
    'degenDelegators.txt',
    'everstakeDelegators.txt',
    'guardiansDelegators.txt',
    'huobiDelegators.txt',
    'intsolDelegators.txt',
    'ioDelegators.txt',
    'iosgDelegators.txt',
    'neoecofundDelegators.txt',
    'neoeconomyDelegators.txt',
    'neofoundationDelegators.txt',
    'sss3Delegators.txt',
    'stakeWithUsDelegators.txt',
    'switcheostakingDelegators.txt',
    'zilliquaDelegators.txt'
]

unique_addresses = set()
for filename in FILENAMES:
    with open(filename) as f:
        unique_addresses.update({L.strip() for i, L in enumerate(f) if not i % 4})

print(len(unique_addresses))

with open('allDelegators.txt', 'w') as f:
    f.write(repr(list(unique_addresses)))


# Get delegator info
# ------------------------------------------------------------------------------
with open('output.csv', 'w') as f:
    writer = csv.writer(f)

    for addr in unique_addresses:
        with urllib.request.urlopen(ENDPOINTS['profile'] % addr) as req:
            payload = json.loads(req.read().decode())
            last_seen = datetime.fromisoformat(payload['last_seen_time'][:19])

        with urllib.request.urlopen(ENDPOINTS['delegations'] % addr) as req:
            payload = json.loads(req.read().decode())
            total = sum(int(r['balance']['amount']) for r in payload['result'])

        print(addr, last_seen, total)
        writer.writerow([addr, last_seen, total])


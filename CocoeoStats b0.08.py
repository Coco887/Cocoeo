#!/usr/bin/env python
'''
CocoeoStats b0.08
'''

# Import librarys
# ------------------------------------------------------------------------------
import csv
import time
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import time 
try:
    import winsound
except ImportError as e: print(e)

# Init time
# ------------------------------------------------------------------------------
initTime = int(time())
print (initTime)

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


def get_row(addr):
    with urllib.request.urlopen(ENDPOINTS['profile'] % addr) as req:
        payload = json.loads(req.read().decode())
        last_seen = datetime.fromisoformat(payload['last_seen_time'][:19])

    with urllib.request.urlopen(ENDPOINTS['delegations'] % addr) as req:
        payload = json.loads(req.read().decode())
        total = sum(float(r['balance']['amount']) for r in payload['result'])
        fulltotal = int(total/100000000)
        
    return [addr, last_seen, fulltotal]


# Get delegator info
# ------------------------------------------------------------------------------
with open('output.csv', 'w') as f:
    writer = csv.writer(f)

    with ThreadPoolExecutor(max_workers=6) as executor:
        for row in executor.map(get_row, unique_addresses):
            writer.writerow(row)
            print(*row)
            
# End of process alerter and duration
# ------------------------------------------------------------------------------
newTimestamp = int(time())
processTime = newTimestamp - initTime
print ('Snapshot Duration:',processTime,'seconds')
winsound.Beep(550, 250)
winsound.Beep(650, 350)

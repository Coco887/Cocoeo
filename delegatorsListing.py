#!/usr/bin/env python
'''
delegatorsListing b0.03
'''

# Import librarys
# ------------------------------------------------------------------------------
import time
import json
import urllib.request
from datetime import datetime
try:
    import winsound
except ImportError as e: print(e)


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
        lines = [L.strip() for L in f]
        
    for i, line in enumerate(lines):
        # Line numbers divisible by 4 (includes 0)
        if not i % 4:
            unique_addresses.add(line)

# Convert to list
unique_addresses = [*unique_addresses]

totalDelegators = len(unique_addresses)
print(totalDelegators)


with open('allDelegators.txt', 'w') as f:
    f.write(str(unique_addresses))


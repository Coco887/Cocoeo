# SwitcheoStats b0.02

# Import librarys
# ------------------------------------------------------------------------------
from datetime import datetime # Get the time and date of computer to set the timer.
import urllib.request, json, winsound, time # Get the urllib class for API, JSON class, Winsound, time class.

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

list_of_dicts = []

for filename in FILENAMES:
    with open(filename) as f:
        it = iter(f.read().splitlines())

    while True:
        try:
            address, amount, _, percentage = next(it), next(it), next(it), next(it)
            list_of_dicts.append({
                'address': address,
            })
        except StopIteration: break
        
unique_addresses = list({d['address'] for d in list_of_dicts})
totalDelegators = len(unique_addresses)
print(totalDelegators)
allDelegators = 'allDelegators.txt'
saveDelegators = open(allDelegators, 'w')
saveDelegators.write(str(unique_addresses))
saveDelegators.close()
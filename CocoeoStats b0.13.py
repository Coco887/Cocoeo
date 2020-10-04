#!/usr/bin/env python
'''
delegatorsListing b0.13
'''

# Imports
# ------------------------------------------------------------------------------
import csv
import json
import re
import shutil
import threading
import urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import time
from pathlib import Path
try:
    import winsound
except ImportError:
    # Fake winsound lets you call Beep/PlaySound/MessageBeep without doing anything
    winsound = type('', (), {'__getattr__': lambda *a: lambda *a, **kw: None})()


# Constants
# ------------------------------------------------------------------------------
CSV_FILE = 'delegations.csv'
ENDPOINTS = {
    'profile': 'https://tradescan.switcheo.org/get_profile?account=%s',
    'validators': 'https://tradescan.switcheo.org/get_all_validators',
    'validator_delegations': 'https://tradescan.switcheo.org/staking/validators/%s/delegations'
}
TESTING = False
THREADS = 8


# Function definitions
# ------------------------------------------------------------------------------
def cprint(string, *, reset='w', end='\n', funcs={}, lock=threading.Lock()):
    '''
    Print colorful text

    Indicate BOLD or normal red yellow green blue cyan magenta & white
    by inserting upper- or lower-cased r y g b c m & w letters surrounded by ;'s

    Example: cprint("These words are ;R;bold red, ;w;white, and ;c;cyan.")
    '''
    if not funcs:
        try:
            from ctypes import windll
            colors = 1,3,2,5,4,6,7,9,11,10,13,12,14,15
            setcolor = (lambda c, f=windll.kernel32.SetConsoleTextAttribute,
                                  s=windll.kernel32.GetStdHandle(-11), **_: f(s, c))
        except ImportError:
            colors = (f'\033[{i};3{c}m' for i in (0,1) for c in (4,6,2,5,1,3,7))
            setcolor = print
        funcs.update({f';{L};': lambda s, c=c, f=setcolor, **kw: f(c, **kw)
                      for L, c in zip('bcgmrywBCGMRYW', colors)})
    with lock:
        for t in re.split(f'(;.;)', f'{string};{reset};{end}'):
            funcs.get(t, print)(t, end='', flush=True)


def get_json(url):
    '''
    Get utf-8-encoded json from a given url, and return a python object
    '''
    with urllib.request.urlopen(url) as req:
        return json.loads(req.read().decode())


def populate_delegator_info(address):
    '''
    This function accepts a delegator address and adds information to its
    dictionary in delegator_info.
    '''
    d = delegator_info[address]

    payload = get_json(ENDPOINTS['profile'] % address)

    d['last_seen'] = datetime.fromisoformat(payload['last_seen_time'][:19])
    d['#name'] = payload.get('username', payload.get('twitter', ''))

    cprint(f';G;{d["#name"] or "anon":>15};Y;@;M;{address} ;C;{d["last_seen"]}')


# Main
# ------------------------------------------------------------------------------
initTime = int(time())


# Get all bonded validators
validators = [d for d in get_json(ENDPOINTS['validators']) if d['bond_status'] == 'bonded']


# Dictionary of dictionaries. It will use delegator addresses as keys.
delegator_info = defaultdict(dict)


# For all bonded validators, add amounts to the dictionary for each delegator.
# After this, each delegator's dictionary will contain validators and amounts:
# delegator_info = {
#   'delegator1_address': {
#       'validator1_name': amount, 
#       'validator2_name': amount,
#   },
#   'delegator2_address': {
#       'validator1_name': amount, 
#       'validator2_name': amount,
#   },
# }
for v in validators:
    vaddr = v['operator_address']
    vname = v['description']['moniker']

    delegations = get_json(ENDPOINTS['validator_delegations'] % vaddr)['result']

    # When testing, only download a small subset of delegation data
    if TESTING:
        delegations = delegations[:3]

    for d in delegations:
        amount = int(d['balance']['amount']) // 100_000_000
        delegator_info[d['delegator_address']][vname] = amount

    cprint(f';Y;+;M;{len(delegations):4} amounts from ;G;{vname}')


# Use multiple threads to download delegator profile information and add it to
# each delegator's dictionary (the logic for this is in populate_delegator_info):
# deleagor_info = {
#   'delegator1_address': {
#       '#name': 'dolan',
#       'last_seen': datetime.datetime(...),
#       'validator1_name': 1111,
#       'validator2_name': 2222,
#   },
#   'delegator2_address': {
#       '#name': 'gooby',
#       'last_seen': datetime.datetime(...),
#       'validator1_name': 1111,
#       'validator2_name': 2222,
#   },
#}
with ThreadPoolExecutor(max_workers=THREADS) as executor:
    [*executor.map(populate_delegator_info, delegator_info)]



# Output
# ------------------------------------------------------------------------------
savefile = Path(CSV_FILE)

           
# Load any existing saved data and make a backup
if savefile.exists():
    with savefile.open(encoding='utf-8') as f:
        old_data = {row['address']: row for row in csv.DictReader(f)}
    shutil.copy(savefile, savefile.with_suffix('.bak'))
else:
    old_data = {}


# TODO: Store data in a way that allows delta calculations
# TODO: Clean up this mess

# Overwrite the savefile
with savefile.open('w', encoding='utf-8') as f:

    # Figure out what the column headers should be
    validator_names = [v['description']['moniker'] for v in validators]

    fieldnames = ['address', '#name', 'last_seen', 'total', 'Δ total']
    for n in validator_names:
        fieldnames.append(n)
        fieldnames.append(f'Δ {n}')

    # Write the column headers
    writer = csv.DictWriter(f, fieldnames, extrasaction='ignore')
    writer.writeheader()

    for address, info in delegator_info.items():

        old_info = old_data.get(address, {})

        # Calculate validator changes
        total = 0
        deltas = {}
        for n in validator_names:
            new_amt = info.get(n, 0)
            old_amt = int(old_info.get(n) or 0)  # Old value can be empty string

            total += new_amt
            deltas[f'Δ {n}'] = 0 if new_amt == old_amt else new_amt - old_amt

        # Calculate total change
        old_total = int(old_info.get('total') or 0)
        deltas['Δ total'] = 0 if total == old_total else total - old_total

        # Save the row
        writer.writerow({
            **info,         # validator columns
            **deltas,       # Δ columns
            'address':      address,
            '#name':        old_info.get('#name', info['#name']),
            'total':        total,
        })


# End of process alerter, duration and timestamp
# ------------------------------------------------------------------------------
newTimestamp = int(time())
processTime = newTimestamp - initTime
print('Snapshot Duration:', processTime, 'seconds - ', str(datetime.now())[:19])
winsound.Beep(666, 333), winsound.Beep(444, 222)

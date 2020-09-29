#!/usr/bin/env python
'''
delegatorsListing b0.11
'''

# Import librarys
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


CSV_FILE = 'delegator_info.csv'
ENDPOINTS = {
    'profile': 'https://tradescan.switcheo.org/get_profile?account=%s',
    'validators': 'https://tradescan.switcheo.org/get_all_validators',
    'validator_delegations': 'https://tradescan.switcheo.org/staking/validators/%s/delegations'
}
TESTING = False


def cprint(string, *, reset='w', end='\n', funcs={}, lock=threading.Lock()):
    '''
    Cross-platform color print function (it's harder than you think)

    Indicate BOLD or normal red yellow green blue cyan magenta & white
    by inserting upper- or lower-cased r y g b c m & w letters surrounded by ;'s

    Example: cprint("These words are ;R;bold red, ;w;normal white, and ;c;cyan.")
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
    with urllib.request.urlopen(url) as req:
        return json.loads(req.read().decode())


def get_profile(k_v):
    addr, balances = k_v
    total = sum(balances)
    payload = get_json(ENDPOINTS['profile'] % addr)
    last_seen = datetime.fromisoformat(payload['last_seen_time'][:19])
    name = payload.get('username', payload.get('twitter', ''))

    # TODO: balance from every validator

    cprint(f';G;{name or "anon":>20};Y;@;R;{addr[:10]}...;w; {last_seen} ;C;-> ;G;{total:>10}')
    return [addr, name, last_seen, total]


# Init time
# ------------------------------------------------------------------------------
initTime = int(time())


# Get all delegators from all bonded validators
# ------------------------------------------------------------------------------
validators = [d for d in get_json(ENDPOINTS['validators']) if d['bond_status'] == 'bonded']
delegators = defaultdict(list)


for v in validators:
    delegations = get_json(ENDPOINTS['validator_delegations'] % v['operator_address'])['result']

    # For testing purposes, limit to 5 delegators per validator
    # Note this will shrink the CSV file 
    if TESTING:
        delegations = delegations[:5]

    for i, d in enumerate(delegations):
        amount = int(d['balance']['amount']) // 100_000_000
        delegators[d['delegator_address']].append(amount)
    cprint(f';Y;+;M;{i+1:4};w; delegator totals from ;G;{v["description"]["moniker"]}')


# Get all delegators profiles
# ------------------------------------------------------------------------------
with ThreadPoolExecutor(max_workers=8) as executor:
    new_rows = {row[0]: row for row in executor.map(get_profile, delegators.items())}


# Get any existing data and make a backup
# ------------------------------------------------------------------------------
savefile = Path(CSV_FILE)
old_rows = {}

if savefile.exists():
    with savefile.open() as f:
        old_rows = {row[0]: row for row in csv.reader(f)}
    shutil.copy(savefile, savefile.with_suffix('.bak'))


# Merge the new data
# ------------------------------------------------------------------------------
# TODO: Use dicts instead of lists
with savefile.open('w') as f:
    writer = csv.writer(f)
    for addr, row in sorted(new_rows.items()):
        # Get the first 4 items of the old row, fallback to new row
        old_row = old_rows.get(addr, row)[:4]
        # Keep old name
        row[1] = old_row[1]
        # Add balance change
        row.append(row[3] - int(old_row[3]))

        writer.writerow(row)


# End of process alerter and duration
# ------------------------------------------------------------------------------
newTimestamp = int(time())
processTime = newTimestamp - initTime
print('Snapshot Duration:', processTime, 'seconds')
winsound.Beep(550, 250)
winsound.Beep(650, 350)

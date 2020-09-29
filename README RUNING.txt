1)change all delagator information by copy/pasta switcheo.org delegation list as u can see on each text files actually.
2)run the bot to get an actual snapshot.


You got the list of rawWalletAdresses on allDelegators.txt
You got an CSV file of wallets adresses / last time seen / total amount stacked on output.csv


***** use max 4 workers or crash:
----------------------------------------------------
with ThreadPoolExecutor(max_workers=4) as executor:
----------------------------------------------------

Snapshot duration estimated time: ~10 minutes
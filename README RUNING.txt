1)change all delagator information by copy/pasta switcheo.org delegation list as u can see on each text files actually.
2)run the bot to get an actual snapshot.

You got the list of rawWalletAdresses on allDelegators.txt
You got an CSV file of wallets adresses / last time seen / total amount stacked on output.csv


***** use max 8 workers or crash, lower it if crash.
--------------------------------------------------------------------------------------------------------
~line 77  --------   with ThreadPoolExecutor(max_workers=8) as executor:
--------------------------------------------------------------------------------------------------------

Snapshot duration estimated time: 3 minutes

********** if you erase content of "xxx.txt" validators u dont want to snapshot, they are not counted, there is the way to get only 1 node informations **********
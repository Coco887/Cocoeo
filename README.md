# Cocoeo 0.11
1)Run the bot to get an actual snapshot</br>
(*your csv file got updated if you run the bot again)</br>


You got an CSV file of "wallets adresses / name / last time seen / total amount stacked / balance changes" on delegator_info.csv
You got an backup of your previous csv on delegator_info.bak

--------------------------------------------------------------------------------------------------------
Use max 8 workers or crash, lower it if crash.
~line 105  --------   with ThreadPoolExecutor(max_workers=8) as executor:

--------------------------------------------------------------------------------------------------------

Snapshot duration estimated time: 3 minutes

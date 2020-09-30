# Cocoeo 0.11
1)Run the bot to get an actual snapshot</br>
(*your csv file got updated if you run the bot again, notice that the names are persistants and stay through an update.)</br>


You got an CSV file of "wallets adresses / names / last time seen / total amount stacked / balance changes" on delegator_info.csv</br>
You got an backup of your previous csv on delegator_info.bak</br>

--------------------------------------------------------------------------------------------------------
Use max 8 workers or crash, lower it if crash.</br>
~line 105  --------   with ThreadPoolExecutor(max_workers=8) as executor:

--------------------------------------------------------------------------------------------------------

Snapshot duration estimated time: 3 minutes

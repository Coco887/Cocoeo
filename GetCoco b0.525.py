# GetCoco b0.525 by Coco87 ©

# Import librarys
# ------------------------------------------------------------------------------
from datetime import datetime # Get the time and date of computer to set the timer.
import urllib.request, json, winsound, time # Get the urllib class for API, JSON class, Winsound, time class.

# Parameters to set:
# ------------------------------------------------------------------------------
RUN = True # Program is set to RUN
# ------------------------------------------------------------------------------

quantitySellAlert = 24000 ##### Set the minimum quantity switcheo buyed to make an alert. #####
quantityBuyAlert  = 24000 ##### Set the minimum quantity switcheo solded to make an alert. #####
quantityEtherChange = 11 ##### Set the minimum quantity ether deposit/withdrawed to make an alert.#####

speedTest = 1 ##### Set to 1 to check test-speed efficiency of the bot, 0 to run normal.
checkEthContractbalanceActive = 1 ##### Set to 1 to check balance ether 0 if not. 

# ------------------------------------------------------------------------------

timeStampComputer = int(time.time()) # Get timetamp of computer.
quantitySoundLengh = 700 # Set base sound lengh.
pastTx = [] # Create a blank list to index transactions.
ethContractBaseValue = 0 # Ether base.
timeNew = 0 # New time.
checked = 0 # Checked.

# ------------------------------------------------------------------------------
# Welcome message and check actual time/date.
# ------------------------------------------------------------------------------
with urllib.request.urlopen("https://api.switcheo.network/v2/exchange/timestamp") as timestamp: # Get timestamp on switcheo API.
    timeActual = json.loads(timestamp.read().decode()) # Decode timestamp from JSON to Python format.
    for v in timeActual.values(): # Get the raw value from the dictionary and write it in the value "v";.
        t = int(v/1000) # Convert timestamp to a usable timestamp (switcheo give too precise one to convert in date format without errors).
        timeActual = datetime.fromtimestamp(t) # Get correct transaction timestamp, convert it to date time.
        print('*****     GetCoco b0.525 by Coco87 with Dwin and Luan collaboration     *****')# Welcome message.
        print('PLEASE CHECK YOUR COMPUTER Time/Date FOR FULL EFFICIENCY:', timeActual)#Timestamp and efficiency.
        print('')
        time.sleep(.3)
# ------------------------------------------------------------------------------
# Get etherscan SWITCHEO contract value and inform on the deposits/withdrawal.
# ------------------------------------------------------------------------------
with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=balance&address=0x7ee7Ca6E75dE79e618e88bDf80d0B1DB136b22D0&tag=latest&apikey=YourApiKeyToken") as ethContract: # Get actual etherscan value
    ethActual = json.loads(ethContract.read().decode()) # Decode ethactual from JSON to Python format
    eth = (str(ethActual['result'])[:4])
    ethContractBaseValue = eth
    winsound.Beep(350, 350)
    winsound.Beep(250, 250)
    print ('Actual value on the ether contract is:')
    print ('-------------',ethContractBaseValue,'ether','-------------')
    print ('')

# Core Code
# ------------------------------------------------------------------------------

print ('Here is the last trades on the market-pair you asked to check:')

while RUN: # While run is true
    if speedTest == 1:
        checked = int(checked + 1)
        print ('Check-Speed=', checked)
    # ------------------------------------------------------------------------------
    # Get timestamp periodicaly
    # ------------------------------------------------------------------------------
    timeNew = int(time.time()) # Convert timestamp to a usable timestamp (switcheo give too precise one to convert in date format without errors)           
    # ------------------------------------------------------------------------------
    # Get data periodicaly
    # ------------------------------------------------------------------------------    
    with urllib.request.urlopen("https://api.switcheo.network/v2/trades/recent?pair=SWTH_ETH") as url: # Get last 20 trades data on switcheo API
        data = json.loads(url.read().decode()) # Decode last 20 trades data from JSON to Python format.
        del data[1:20] # Reduce data to the last trade.
        for d in data:  # Pour d dans data.
            # ------------------------------------------------------------------------------
            # BUY ALERTER
            # ------------------------------------------------------------------------------
            if(d['side'] == "buy" and float(d['quantity']) > quantityBuyAlert): # If there is a buy higher than the quantity set:
                lastTx = [d['id']] # Check the transaction id in transaction index.
                
                while lastTx not in pastTx: # If transaction is not on the index.
                    timeTrade = datetime.fromtimestamp(d['timestamp']) # Get transaction timestamp, convert it to date time.
                    quantity = float(d['quantity']) # Get quantity.
                    print(d['side'],"--",d['quantity'],'/',d['price'],'on',d['pair'],timeTrade) # Print amount, price and time of the trade.
                    pastTx.append(lastTx) # Print the transaction id in transaction index.
                    quantitySoundLengh = int(quantity/150) # Set SoundLengh to quantity/x ms.
                    winsound.Beep(1550, quantitySoundLengh) # 1400 is the frequency of sound, 600 is the duration in ms (1000 = 1 second).
                
            # ------------------------------------------------------------------------------        
            # SELL ALERTER
            # ------------------------------------------------------------------------------  
            if(d['side'] == "sell" and float(d['quantity']) > quantitySellAlert): # If there is a sell higher than the quantity set:
                lastTx = [d['id']] # Check the transaction id in transaction index.

                while lastTx not in pastTx: # If transaction is not on the index.
                    timeTrade = datetime.fromtimestamp(d['timestamp']) # Get transaction timestamp, convert it to date time.
                    quantity = float(d['quantity']) # Get quantity.
                    print(d['side'],"--",d['quantity'],'/',d['price'],'on',d['pair'],timeTrade) # Print amount, price and time of the trade.
                    pastTx.append(lastTx) # Print the transaction id in transaction index.
                    quantitySoundLengh = int(quantity/150) # Set SoundLengh to quantity/x ms.
                    winsound.Beep(350, quantitySoundLengh) # 400 is the frequency of sound, 600 is the duration in ms (1000 = 1 seconds)

    # ------------------------------------------------------------------------------
    # Check etherscan balance change
    # ------------------------------------------------------------------------------
    if checkEthContractbalanceActive == 1:
        if (timeNew >= timeStampComputer+30):
            timeStampComputer = timeNew
            with urllib.request.urlopen("https://api.etherscan.io/api?module=account&action=balance&address=0x7ee7Ca6E75dE79e618e88bDf80d0B1DB136b22D0&tag=latest&apikey=YourApiKeyToken") as ethContract: # Get actual etherscan value
                ethA = json.loads(ethContract.read().decode()) # Decode balance from JSON to Python format
                ethNow = (str(ethA['result'])[:4])
                ethContractActualValue = ethNow
            
            if ((int(ethContractActualValue) + int(quantityEtherChange)) < int(ethContractBaseValue)):
                ethContractBaseValue = ethContractActualValue
                print('-Ether contract decreased to:',ethContractActualValue)
   
            if ((int(ethContractActualValue) - int(quantityEtherChange)) > int(ethContractBaseValue)):
                ethContractBaseValue = ethContractActualValue
                winsound.Beep(550, 250)
                winsound.Beep(650, 350)
                print('-Ether contract increased to:',ethContractActualValue)

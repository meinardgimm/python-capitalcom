# initializations
from config import login, password, API_KEY
from client_demo import *
from aws_live import *

def webhook(ticker,marketside,prices,account):
  event = {
    "open": prices['open'][-1], #Jeweils der letzte / aktuellste Preis ist relevant
    "high": prices['high'][-1],
    "low": prices['low'][-1],
    "close": prices['close'][-1],
    "exchange": "BATS",
    "ticker": ticker,
    "volume": 1,
    "marketside": marketside,
    "Account": account
  }
  lambda_handler(event)
  calc_parameters(event)

def calc_parameters(event):
  #Clienten und Abfrage aktualisieren | nicht sicher ob notwendig :/
  cl = Client( 
    login,
    password,
    API_KEY
  )
  # Accountbalance nochmal abchecken
  subaccounts = cl.all_accounts()
  data = json.loads(subaccounts) 
  subaccount_names = [account["accountName"] for account in data["accounts"]]
  subaccount_balance = [account["balance"]["balance"] for account in data["accounts"]]
  for index in range(0,len(subaccount_names)):
     if subaccount_names[index] == event['Account']:
        balance_index = index
  
  AvailableMoney = subaccount_balance[balance_index]
  Hebel=5 #Möglicherweise in capital.com erhöherbar
  Positionsgrosse = 0.35 #Größe der Position bezogen auf verfügbares Kapital in Prozent
  size=round(AvailableMoney/event['high']*Hebel*Positionsgrosse,2) 
  if event['marketside'] == "BUY":
      stop_level=event['low']*0.96
  if event['marketside'] == "SELL":
      stop_level=event['high']*1.04
      
  direction = event['marketside']
  epic = event['ticker']
  cl.place_the_position(direction, epic, size, stop_level)
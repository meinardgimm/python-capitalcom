# initializations
from config import login, password, API_KEY
from client_demo import *
from aws_live import *

def webhook(ticker,marketside,prices,account, positions_dict):
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
  #lambda_handler(event)
  calc_parameters(event, positions_dict)

def calc_parameters(event, positions_dict):
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
  subaccount_balance = [account["balance"]["available"] for account in data["accounts"]]
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
  if event['marketside'] == 'BUY' or event['marketside'] == 'SELL': 
    # try and catch this mfucker
    deal_reference = cl.place_the_position(direction, epic, round(size), stop_level = round(stop_level,4))
    deal_reference = json.loads(deal_reference)
    deal_success = cl.position_order_confirmation(deal_reference["dealReference"])
    deal_success = json.loads(deal_success)
    if 'dealStatus' in deal_success.keys():
      return deal_success['dealStatus'] 
    else:
      return 'not successful'
    #cl.place_the_order(direction, epic, round(size),level =event['high'],  type = "LIMIT", stop_level = round(stop_level,4))
  if event['marketside'] == 'CLOSE':
    for index in range(0, len(positions_dict[2])):
      if positions_dict[0][index] == epic:
        deal_reference = cl.close_position(positions_dict[2][index])
        deal_reference = json.loads(deal_reference)
        deal_success = cl.position_order_confirmation(deal_reference["dealReference"])
        deal_success = json.loads(deal_success)
        if 'dealStatus' in deal_success.keys():
          return deal_success['dealStatus'] 
        else:
          return 'not successful'


#url = 'https://demo-api-capital.backend-capital.com/api/v1/positions'
#self._get_body_parameters(**kwargs)
#{'direction': 'SELL', 'epic': 'XRPUSD', 'size': 23676.79, 'guaranteedStop': 0.6471608, 
# 'trailingStop': False, 'stopLevel': None, 'stopDistance': None, 'stopAmount': None, 
# 'profitLevel': None, 'profitDistance': None, 'profitAmount': None}
import http.client
import json
import math
## Keys and Destinations
conn = http.client.HTTPSConnection("demo-api-capital.backend-capital.com")
#conn = http.client.HTTPSConnection("api-capital.backend-capital.com")
payload = json.dumps({
  "identifier": "meinardgimm@gmail.com",
  "password": "8nnn45n#U"
})
headers = {
  'X-CAP-API-KEY': 'hIkIH9Ia2wM5uetC',
  'Content-Type': 'application/json'
}
Position_ID = []
Closed_IDs = []

def lambda_handler(event):
  ###############################
  # hier ein try/catch einbauen
  POSITION_headers, Balance, data, POSITION_headers2, AccID = OPEN_SESSION(payload,headers,event) #Open session at broker

  TickerInfoTarget="/api/v1/markets/" + str(event['ticker'])
  conn.request("GET", TickerInfoTarget, '', POSITION_headers)
  TickerInfo = conn.getresponse()
  TickerInfo = TickerInfo.read()
  TickerInfo = json.loads(TickerInfo)
  TickerHIGH = TickerInfo["snapshot"]["high"]
  TickerLOW = TickerInfo["snapshot"]["low"]
  #return data, Balance
  
  if event['marketside'] == 'BUY' or event['marketside'] == 'SELL':
    Position_ID = OPEN_POSITION(Balance, event, POSITION_headers, TickerHIGH, TickerLOW)
    return POSITION_headers, Position_ID, TickerInfo, POSITION_headers2, AccID
  elif event['marketside'] == 'CLOSE' or event['marketside'] == 'StopLoss':
    CLosed_IDs = CLOSE_POSITION(event, POSITION_headers)
    return POSITION_headers, CLosed_IDs, TickerInfo
  else: 
    return TickerInfo #hier einen Fehlerfänger einbauen
  
#####################
def OPEN_POSITION(Balance, event, POSITION_headers, TickerHIGH, TickerLOW):
  ## Aktuell verfügbars Geld abfragen // dazu erstmal Daten Decodieren
  AvailableMoney = Balance['available']
  # Get ticker info for calculating stop loss
  #marketInfoAdress = {"/api/v1/markets?epics=",event[ticker]}
  #marketInfoAdress = "#".join(marketInfoAdress)
  #conn.request("GET", marketInfoAdress, payload, headers)
  #res = conn.getresponse()
  #data = res.read()
  #marketInfo = data
  
  ## Neue Anfrage zum Erstellen einer Position (=! Order)
  #Position hat xx% des gesamt verfügbaren Geldes - Mit Hebel dann "*5"
  Hebel=5 #Möglicherweise in capital.com erhöherbar
  Positionsgrosse = 0.35 #Größe der Position bezogen auf verfügbares Kapital in Prozent
  size=round(AvailableMoney/event['high']*Hebel*Positionsgrosse,2) 
  if event['marketside'] == "BUY":
    stoploss=TickerLOW*0.96
  if event['marketside'] == "SELL":
    stoploss=TickerHIGH*1.04
  NEW_POSITION = json.dumps({
    "epic": event['ticker'],
    "direction": event['marketside'],
    "size": size,
    #"guaranteedStop": True, #never uncomment
    #"level": 200, #for Orders
    #"type": "LIMIT", #for orders
    "stopLevel": stoploss
  })
  conn.request("POST", "/api/v1/positions", NEW_POSITION, POSITION_headers)
  #conn.request("POST", "/api/v1/workingorders", NEW_POSITION, POSITION_headers) # for orders
  res = conn.getresponse()
  Position_ID = res.read() #returns ID of the new Position
  return Position_ID#, marketInfo 
##################### 
def CLOSE_POSITION(event, POSITION_headers):
  ## Offene Positionen schließen
  ## get all open positions
  conn.request("GET", "/api/v1/positions", '', POSITION_headers)
  res = conn.getresponse()
  POSITIONS = res.read() #Enthält Details über alle offenen Positionen
  POSITIONS=json.loads(POSITIONS)
  ## Finden der DealIDs aller offenen Positionen der angefragten Aktie
  deal_ids = []
  for position in POSITIONS['positions']:
    if position['market']['epic'] == event['ticker']:
      deal_id = position['position']['dealId']
      deal_ids.append(deal_id)
  data=[] # Enthält die IDs der geschlossenen Positionen
  ## Alle offenen Positionen einzeln schließen (i.d.R. sollte nur eine offen sein)
  for id in deal_ids:
    RestClient_Delete="/api/v1/positions/" + str(id)
    conn.request("DELETE", RestClient_Delete, '', POSITION_headers)
    res = conn.getresponse()
    res_read=res.read()
    data.append(res_read)
  if Closed_IDs:
    return Closed_IDs
  else: 
    return "Verkauf nicht möglich."
#####################
def OPEN_SESSION(payload,headers,event):
  ## Session eröffnen
  conn.request("POST", "/api/v1/session", payload, headers)
  res = conn.getresponse()
  AccData = res.read()
  resheads = res.getheaders()
  ## Suche nach Session Keys in den Headers der response
  CST_value = None
  X_SECURITY_TOKEN_value = None
  for reshead in resheads:
      key, value = reshead
      if key == "CST":
          CST_value = value
      if key == "X-SECURITY-TOKEN":
          X_SECURITY_TOKEN_value = value
  POSITION_headers = {
    'X-SECURITY-TOKEN': X_SECURITY_TOKEN_value,
    'CST': CST_value,
    'Content-Type': 'application/json'
  }
  # switch to targeted trading account
  Balance, data, POSITION_headers, POSITION_headers2, AccID = SWITCH_TRADING_ACCOUNT(AccData, POSITION_headers,event)
  return POSITION_headers, Balance, data, POSITION_headers2, AccID
#####################
def SWITCH_TRADING_ACCOUNT(AccData, POSITION_headers,event):
  print(AccData)
  #Find ID of desired trading account (part of webhook)
  AccID = []
  AccData = json.loads(AccData)
  for Accs in AccData['accounts']:
    if Accs['accountName'] == event['Account']:
      AccID = Accs['accountId']
  #Switch account
  payload = json.dumps({
  "accountId": AccID
  })
  conn.request("PUT", "/api/v1/session", payload, POSITION_headers)
  res = conn.getresponse()
  dataID = res.read()
  # New request headers for new Account
  resheads = res.getheaders()
  ## Suche nach Session Keys in den Headers der response
  CST_value = None
  X_SECURITY_TOKEN_value = None
  for reshead in resheads:
      key, value = reshead
      if key == "CST":
          CST_value = value
      if key == "X-SECURITY-TOKEN":
          X_SECURITY_TOKEN_value = value
  POSITION_headers2 = {
    'X-SECURITY-TOKEN': X_SECURITY_TOKEN_value,
    'CST': CST_value,
    'Content-Type': 'application/json'
  }
  #get Account Balances
  conn.request("GET", "/api/v1/accounts", '', POSITION_headers) #gets balance of all accounts
  res = conn.getresponse()
  data = res.read()
  data=json.loads(data)
  Balance = []
  for Accs in data['accounts']:
    if Accs['accountName'] == event['Account']:
      Balance = Accs['balance'] #JSON with multiple entries
      
  conn.request("GET", "/api/v1/session", '', POSITION_headers)
  res = conn.getresponse()
  POSITION_headers2 = res.read()
  POSITION_headers2 = json.loads(POSITION_headers2)
  AccID = dataID
  #print(data.decode("utf-8"))
      
  return Balance, data, POSITION_headers, POSITION_headers2, AccID
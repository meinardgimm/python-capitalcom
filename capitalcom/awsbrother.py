## Initializations
from config import login, password, API_KEY
from client_demo import *
cl = Client(
    login,
    password,
    API_KEY
)
event = {
    "open": price,
    "high": price,
    "low": price,
    "close": price,
    "exchange": "BATS",
    "ticker": ticker,
    "volume": 1,
    "marketside": marketside,
    "Account": account
  }

def calc_parameters():
## Aktuell verfügbars Geld abfragen // dazu erstmal Daten Decodieren
    AvailableMoney = Balance['available']
    Hebel=5 #Möglicherweise in capital.com erhöherbar
    Positionsgrosse = 0.35 #Größe der Position bezogen auf verfügbares Kapital in Prozent
    size=round(AvailableMoney/event['high']*Hebel*Positionsgrosse,2) 
    if event['marketside'] == "BUY":
        stop_level=TickerLOW*0.96
    if event['marketside'] == "SELL":
        stop_level=TickerHIGH*1.04
        
    direction = event['marketside']
    epic = event['ticker']

    cl.place_the_position(direction, epic, size, stop_level)

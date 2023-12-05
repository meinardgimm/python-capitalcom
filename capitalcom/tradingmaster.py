from config import login, password, API_KEY
from client_demo import *
from tradingscrips import *
from webhook_simulatior import *

cl = Client(
    login,
    password,
    API_KEY
)

#loop through time
# loop through tickers

# get prices

# check Scripts

# open GUI

epic = 'BTCUSD'
resolution = ResolutionType.MINUTE
max = 100

prices = cl.historical_prices(epic,resolution, max)
data = json.loads(prices) 
snapshot_times = [entry['snapshotTime'] for entry in data['prices']]
bid_prices = [entry['openPrice']['bid'] for entry in data['prices']]
ask_prices = [entry['openPrice']['ask'] for entry in data['prices']]

action = Scripts.simpletest(bid_prices)
account = "Demo_1"
if action == "BUY":
    webhook(epic,action,bid_prices[-1],account)

subaccounts = cl.all_accounts()
data = json.loads(subaccounts) 
subaccount_names = [account["accountName"] for account in data["accounts"]]
subaccount_balance = [account["balance"]["balance"] for account in data["accounts"]]
subaccount_profitloss = [account["balance"]["profitLoss"] for account in data["accounts"]]


print(subaccount_names)
print(subaccount_balance)
print(subaccount_profitloss)
print(action)


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
while True:
    subaccounts = cl.all_accounts()
    data = json.loads(subaccounts) 
    subaccount_names = [account["accountName"] for account in data["accounts"]]
    subaccount_balance = [account["balance"]["balance"] for account in data["accounts"]]
    subaccount_profitloss = [account["balance"]["profitLoss"] for account in data["accounts"]]
    #print(subaccount_names)
    #print(subaccount_balance)
    #print(subaccount_profitloss)

    watchlists = cl.watchlist_stockwatch()
    data = json.loads(watchlists)
    tickers = [entry['epic'] for entry in data['markets']]

    for ticker in tickers:
        epic = ticker
        resolution = ResolutionType.MINUTE
        max = 100
        # get prices
        prices = cl.historical_prices(epic,resolution, max)
        data = json.loads(prices) 
        snapshot_times = [entry['snapshotTime'] for entry in data['prices']]
        bid_prices = [entry['openPrice']['bid'] for entry in data['prices']]
        ask_prices = [entry['openPrice']['ask'] for entry in data['prices']]

        # check Scripts
        action = Scripts.simpletest(bid_prices)
        account = "Demo_1"
        if action == "BUY":
            webhook(epic,action,bid_prices[-1],account)

        action = Scripts.GPT_intuitive(bid_prices) #bullshit, zehn Mal die gleiche action dann 
        account = "Demo_2"
        if action == "BUY":
            webhook(epic,action,bid_prices[-1],account)
        if action == "SELL":
            webhook(epic,action,bid_prices[-1],account)

        print(action)
        print(ticker)
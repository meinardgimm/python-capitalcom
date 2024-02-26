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
    # Update current Balances
    subaccounts = cl.all_accounts()
    data = json.loads(subaccounts) 
    subaccount_names = [account["accountName"] for account in data["accounts"]]
    subaccount_balance = [account["balance"]["balance"] for account in data["accounts"]]
    subaccount_profitloss = [account["balance"]["profitLoss"] for account in data["accounts"]]
    subaccount_IDs = [account["accountId"] for account in data["accounts"]]

    # Tickers of interest are found in the watchlist
    watchlists = cl.watchlist_stockwatch()
    data = json.loads(watchlists)
    tickers = [entry['epic'] for entry in data['markets']]
    # delete all tickers with open positions 
    positions_open = []
    all_positions_tickers = []
    for account in subaccount_IDs:
        cl.switch_account(account)
        plh = json.loads(cl.all_positions())
        if plh.get("positions"):
            positions_open.extend([entry['market']['epic'] for entry in plh['positions']])
            #all_positions_tickers = [entry['market']['epic'] for entry in positions_open['positions']]

    # Remove elements from A that are also in B
    if positions_open:
        unique_positions = list(set(positions_open)) 
        tickers = [x for x in tickers if x not in unique_positions]
    print(tickers)

    # Make trading decisions

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

        # prints out actions even if unsuccessful
        print(action)
        print(ticker)
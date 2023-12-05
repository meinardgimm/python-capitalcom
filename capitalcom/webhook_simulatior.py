from aws_live import *

def webhook(ticker,marketside,price,account):

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

  lambda_handler(event)
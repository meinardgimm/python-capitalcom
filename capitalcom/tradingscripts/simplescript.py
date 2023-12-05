from client_demo import *
from config import login, password, API_KEY


cl = Client(
    login,
    password,
    API_KEY
)

epic = 'BTCUSD'
resolution = ResolutionType.MINUTE
max = 100

prices = cl.historical_prices(epic,resolution,max)
print('prices')
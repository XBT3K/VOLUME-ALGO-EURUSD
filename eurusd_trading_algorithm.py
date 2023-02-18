import oandapyV20
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.exceptions import V20Error
import pandas as pd
import ta

# Set up your Oanda account access
client = oandapyV20.API(access_token='your_access_token_here', environment='practice')

# Define the currency pair you want to trade and the number of units you want to buy or sell
instrument = 'EUR_USD'
units = 10000

# Define the time frame for your data and the period for calculating the moving average
timeframe = 'M5'
ma_period = 20

# Retrieve historical candlestick data from Oanda
params = {
    'count': 100,
    'granularity': timeframe
}
candles = client.instrument.candles(instrument, params=params)
candles = candles.get('candles')
candles = pd.DataFrame.from_dict(candles)
candles['time'] = pd.to_datetime(candles['time'])
candles.set_index('time', inplace=True)

# Calculate the moving average of the candlestick data
ma = candles['mid']['c'].rolling(window=ma_period).mean()

# Calculate the On-Balance Volume (OBV) and Chaikin Money Flow (CMF) indicators
obv = ta.volume.on_balance_volume(candles['mid']['c'], candles['volume'])
cmf = ta.volume.chaikin_money_flow(candles['high'], candles['low'], candles['mid']['c'], candles['volume'])

# Determine if the current price is above or below the moving average and if the OBV and CMF are also signaling a buy or sell
current_price = candles['mid']['c'].iloc[-1]
last_price = candles['mid']['c'].iloc[-2]
current_obv = obv.iloc[-1]
last_obv = obv.iloc[-2]
current_cmf = cmf.iloc[-1]
last_cmf = cmf.iloc[-2]

if current_price > ma.iloc[-1] and last_price < ma.iloc[-2] and current_obv > last_obv and current_cmf > last_cmf:
    # Buy units of the currency pair if the price crosses above the moving average and the OBV and CMF are signaling a buy
    try:
        order = MarketOrderRequest(instrument=instrument, units=units)
        response = orders.OrderCreate(accountID='your_account_id_here', data=order.data).execute(client)
        print(response)
    except V20Error as e:
        print(e)
elif current_price < ma.iloc[-1] and last_price > ma.iloc[-2] and current_obv < last_obv and current_cmf < last_cmf:
    # Sell units of the currency pair if the price crosses below the moving average and the OBV and CMF are signaling a sell
    try:
        order = MarketOrderRequest(instrument=instrument, units=-units)
        response = orders.OrderCreate(accountID='your_account_id_here', data=order.data).execute(client)
        print(response)
    except V20Error as e:
        print(e)
else:
    # Do nothing if the current price is not crossing the moving average or the OBV and CMF are not signaling a trade
    pass

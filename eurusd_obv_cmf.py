import json
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import pandas as pd

# Load configuration from file
with open('config.json') as f:
    config = json.load(f)

# Oanda API access credentials
access_token = config['access_token']
accountID = config['accountID']

# Trading parameters
pair = config['pair']
pos_size = config['pos_size']
take_profit = config['take_profit']
stop_loss = config['stop_loss']

# Connect to Oanda API
client = oandapyV20.API(access_token=access_token)

# Get latest 100 15-minute candlesticks of EUR/USD data
params = {
    'count': 100,
    'granularity': 'M15'
}
r = instruments.InstrumentsCandles(instrument=pair, params=params)
data = client.request(r)

# Convert data to Pandas DataFrame
df = pd.DataFrame([[candle['time'], candle['mid']['o'], candle['mid']['h'], candle['mid']['l'], candle['mid']['c'], candle['volume']] for candle in data['candles']])
df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
df['time'] = pd.to_datetime(df['time'])
df = df.set_index('time')

# Calculate OBV and CMF indicators
df['obv'] = df['volume'].cumsum()
df['cmf'] = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low']) * df['volume']
df['cmf'] = df['cmf'].rolling(20).sum() / df['volume'].rolling(20).sum()

# Execute trade based on OBV and CMF signals
if df['obv'].iloc[-1] > df['obv'].iloc[-2] and df['cmf'].iloc[-1] > 0:
    units = pos_size
    side = 'buy'
elif df['obv'].iloc[-1] < df['obv'].iloc[-2] and df['cmf'].iloc[-1] < 0:
    units = -pos_size
    side = 'sell'
else:
    units = 0
    side = 'hold'

if units != 0:
    # Create market order
    order_data = {
        'order': {
            'units': str(units),
            'instrument': pair,
            'timeInForce': 'FOK',
            'type': 'MARKET',
            'positionFill': 'DEFAULT',
            'side': side,
            'takeProfitOnFill': {
                'price': str(df['close'].iloc[-1] + units * take_profit)
            },
            'stopLossOnFill': {
                'price': str(df['close'].iloc[-1] - units * stop_loss)
            }
        }
    }
    r = oandapyV20.endpoints.orders.OrderCreate(accountID, data=order_data)
    client.request(r)

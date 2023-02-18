import oandapyV20
import oandapyV20.endpoints.orders as orders
import pandas as pd

def obv(df):
    obv_values = []
    obv = 0
    for index, row in df.iterrows():
        if row['Close'] > row['Close'].shift(1):
            obv += row['Volume']
        elif row['Close'] < row['Close'].shift(1):
            obv -= row['Volume']
        obv_values.append(obv)
    return pd.Series(obv_values, index=df.index)

def cmf(df, period=20):
    mfv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
    mfv *= df['Volume']
    cmf = mfv.rolling(period).sum() / df['Volume'].rolling(period).sum()
    return cmf

# Initialize the Oanda API client
access_token = "YOUR_ACCESS_TOKEN"
accountID = "YOUR_ACCOUNT_ID"
client = oandapyV20.API(access_token=access_token)

# Define trading parameters
pair = "EUR_USD"
units = 10000
take_profit = 0.0010
stop_loss = 0.0010

# Get historical candlestick data from Oanda
params = {"count": 100, "granularity": "M15"}
r = instruments.InstrumentsCandles(instrument=pair, params=params)
response = client.request(r)
candles = response.get("candles")
df = pd.DataFrame([(candle["time"], candle["mid"]["o"], candle["mid"]["h"], candle["mid"]["l"], candle["mid"]["c"], candle["volume"]) for candle in candles])
df.columns = ["Time", "Open", "High", "Low", "Close", "Volume"]
df["Time"] = pd.to_datetime(df["Time"])
df = df.set_index("Time")

# Calculate the OBV and CMF values
df["OBV"] = obv(df)
df["CMF"] = cmf(df)

# Define the trading strategy based on the OBV and CMF values
if df["OBV"].iloc[-1] > df["OBV"].iloc[-2] and df["CMF"].iloc[-1] > df["CMF"].iloc[-2]:
    order_type = "buy"
elif df["OBV"].iloc[-1] < df["OBV"].iloc[-2] and df["CMF"].iloc[-1] < df["CMF"].iloc[-2]:
    order_type = "sell"
else:
    order_type = "hold"

# Execute the trade if the trading strategy signals a buy or sell order
if order_type == "buy":
    data = {
        "order": {
            "instrument": pair,
            "units": units,
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "takeProfitOnFill": {
                "price": df["Close"].iloc[-1] + take_profit
            },
            "stopLossOnFill": {
                "price": df["Close"].iloc[-1] - stop_loss
            }
        }
    }
    r = orders.OrderCreate(accountID, data=data)
    response = client.request(r)
    print(response)
elif order_type == "sell":
    data = {
        "order": {
            "instrument": pair

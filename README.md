# OBV and CMF Trading Algorithm for EUR/USD

This is a simple trading algorithm that uses the On-Balance Volume (OBV) and Chaikin Money Flow (CMF) indicators to execute trades on the EUR/USD currency pair using the Oanda API.

## Requirements

- Python 3
- `oandapyV20` library for accessing the Oanda API
- `pandas` library for data manipulation

## Installation

You can install the required libraries using `pip`:

pip install oandapyV20 pandas

## Configuration

To use the algorithm, you need an Oanda account and API access token. You should set the `access_token` and `accountID` variables in the code to your own values.

You can also customize the trading parameters, such as the currency pair, position size, take profit, and stop loss levels.

## Usage

You can run the algorithm by executing the `eurusd_obv_cmf.py` file in a Python environment, such as:

python eurusd_obv_cmf.py

The algorithm will fetch the latest 100 15-minute candlesticks of EUR/USD data from Oanda, calculate the OBV and CMF values, and execute a buy, sell, or hold order based on the OBV and CMF signals.

## Disclaimer

This algorithm is for educational purposes only and should not be used for real trading without proper testing and risk management. The author and publisher are not responsible for any losses incurred using this code or any trading algorithm based on it.

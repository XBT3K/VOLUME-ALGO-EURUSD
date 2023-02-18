# Forex Trading Algorithm

This algorithm uses a combination of volume, OBV, and CMF indicators to execute trades in the EUR/USD market. It is designed to run on Python 3.8 and requires the following libraries: `pandas`, `numpy`, `backtrader`, `ta`, and `pyyaml`.

## Getting Started

1. Install the required libraries by running `pip install -r requirements.txt` in your terminal.

2. Create a `config.yml` file with your desired parameters, including your trading strategy, time frame, and risk management.

3. Run `main.py` to start trading live, or run `backtest.py` to backtest your strategy on historical data.

## Configuration

The `config.yml` file contains the following parameters:

- `strategy`: The trading strategy to use. Options include `MA_cross`, `RSI`, and `MACD`.
- `timeframe`: The time frame to trade on. Options include `1m`, `5m`, `15m`, `1h`, and `1d`.
- `risk_management`: The risk management parameters. Options include `fixed` or `dynamic`, and include the `stop_loss` and `take_profit` parameters.

## Backtesting

To backtest your trading strategy, run `backtest.py` in your terminal. The results will be saved to a `backtest_results.csv` file.

## Live Trading

To start trading live, run `main.py` in your terminal. Make sure to adjust the `config.yml` parameters to suit your needs, and monitor the trading activity closely.

## Disclaimer

Trading forex carries a high level of risk and may not be suitable for all investors. The algorithm provided is for educational purposes only and should not be considered financial advice. Always do your own research before making any investment decisions.

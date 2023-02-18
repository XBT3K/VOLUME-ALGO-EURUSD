# Volume OBV CMF Trading Algorithm

This is a trading algorithm that uses a combination of volume, On Balance Volume (OBV), and Chaikin Money Flow (CMF) indicators to generate trading signals for the EUR/USD forex pair.

## Overview

The algorithm is implemented in Python and uses the following libraries:

- `backtrader` for backtesting and trading simulation
- `pandas` for data manipulation and analysis
- `requests` for retrieving forex data from an API
- `PyYAML` for parsing the configuration file

The algorithm consists of the following files:

- `config.yml`: Configuration file for the algorithm
- `main.py`: Main script for running the algorithm
- `backtest.py`: Module for backtesting the algorithm

## Usage

To use the algorithm, follow these steps:

1. Install the required libraries by running `pip install -r requirements.txt` in your terminal.
2. Modify the `config.yml` file to match your desired settings for the algorithm.
3. Run the algorithm by running `python main.py` in your terminal.

The algorithm will generate trading signals based on the configuration settings and print the results to the console.

## Disclaimer

This algorithm is for educational and informational purposes only and should not be construed as investment advice. Use the algorithm at your own risk and always do your own research and due diligence before making any investment decisions.

## License

This code is licensed under the MIT License. 

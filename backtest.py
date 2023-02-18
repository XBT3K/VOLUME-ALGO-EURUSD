import backtrader as bt
from VolumeOBVCMF import VolumeOBVCMF
import json

# Load our config file
with open('config.json') as f:
    config = json.load(f)

# Create a new instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy with the params from the config file
cerebro.addstrategy(VolumeOBVCM

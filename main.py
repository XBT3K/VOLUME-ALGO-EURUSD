import backtrader as bt
from VolumeOBVCMF import VolumeOBVCMF

# Create a new instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy
cerebro.addstrategy(VolumeOBVCMF)

# Add our data feed
data = bt.feeds.GenericCSVData(
    dataname='https://raw.githubusercontent.com/Alphapulse/forex/master/data/EURUSD.csv',
    nullvalue=0.0,
    dtformat='%Y-%m-%d %H:%M:%S',
    datetime=0,
    time=-1,
    high=2,
    low=3,
    open=1,
    close=4,
    volume=5,
    openinterest=-1,
    timeframe=bt.TimeFrame.Minutes,
    compression=15
)

cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(100000.0)

# Set our desired commission
cerebro.broker.setcommission(commission=0.001)

# Run the backtest
cerebro.run()

# Print the final portfolio value
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

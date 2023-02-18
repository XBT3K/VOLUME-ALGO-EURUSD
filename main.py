import os
import backtrader as bt
import pandas as pd
import yfinance as yf

class OBV(bt.Indicator):
    lines = ('obv',)
    params = (('period', 21),)
    plotinfo = dict(subplot=False)
    plotlines = dict(obv=dict(color='purple', alpha=0.75))

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        price = self.data.close
        volume = self.data.volume
        obv = self.lines.obv
        obv[0] = self.lines.obv[-1]
        if price > price[-1]:
            obv[0] += volume
        elif price < price[-1]:
            obv[0] -= volume
        else:
            obv[0] = self.lines.obv[-1]

class CMF(bt.Indicator):
    lines = ('cmf',)
    params = (('period', 20),)
    plotinfo = dict(subplot=True)
    plotlines = dict(cmf=dict(color='red', alpha=0.75))

    def __init__(self):
        self.addminperiod(self.p.period)

    def next(self):
        price = self.data.close
        high = self.data.high
        low = self.data.low
        volume = self.data.volume
        cmf = self.lines.cmf
        ad = (2*price - high - low) / (high - low) * volume
        ad_sum = bt.ind.SumN(ad, period=self.p.period)
        volume_sum = bt.ind.SumN(volume, period=self.p.period)
        cmf[0] = ad_sum[0] / volume_sum[0]

class MyStrategy(bt.Strategy):
    params = dict(
        period_obv=21,
        period_cmf=20,
        upper=0.05,
        lower=-0.05,
        printlog=True,
    )

    def __init__(self):
        self.obv = OBV(period=self.params.period_obv)
        self.cmf = CMF(period=self.params.period_cmf)
        self.buy_signal = bt.ind.CrossUp(self.obv, self.cmf * (1 + self.params.upper))
        self.sell_signal = bt.ind.CrossDown(self.obv, self.cmf * (1 + self.params.lower))
        if self.params.printlog:
            bt.indicators.Print(self.obv.obv, self.cmf.cmf, self.buy_signal, self.sell_signal)

    def next(self):
        if not self.position:
            if self.buy_signal[0]:
                self.buy()
        else:
            if self.sell_signal[0]:
                self.close()

if __name__ == '__main__':
    # Get the data
    data = yf.download('EURUSD=X', start='2019-01-01', end='2022-01-01')

    # Create a cerebro instance
    cerebro = bt.Cerebro()

    # Add our strategy
    cerebro.addstrategy(MyStrategy)

    # Add the data to cerebro
    cerebro.adddata(bt.feeds.PandasData(dataname=data))

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Set the commission
    cerebro.broker.setcommission(commission=0.001)

    # Print out the starting conditions
    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():,.2f} USD')

    # Run the strategy
    cere

import backtrader as bt
import pandas as pd

class OBVCMFStrategy(bt.Strategy):
    params = (
        ('period', 20),
        ('devfactor', 2),
        ('obv_period', 14),
        ('cmf_period', 20),
        ('cmf_threshold', 0.05),
    )

    def __init__(self):
        self.cmf = bt.talib.CHAIKIN_ADX()
        self.obv = bt.talib.OBV()
        self.buysig = btind.CrossUp(self.obv, self.obv.ma(period=self.p.obv_period))
        self.sellsig = btind.CrossDown(self.obv, self.obv.ma(period=self.p.obv_period))
        self.buyprice = None
        self.sellprice = None
        self.order = None
        self.order_placed = False

    def next(self):
        if not self.position:
            if self.buysig:
                self.buyprice = self.data.close[0]
                self.order = self.buy()
        else:
            if self.sellsig:
                self.sellprice = self.data.close[0]
                self.order = self.sell()

        if self.order:
            self.order_placed = True

        if self.order_placed and not self.order.status == bt.Order.Accepted:
            self.order = None
            self.order_placed = False

    def stop(self):
        self.log('OBV-CMF period: %d, devfactor: %.2f' % (self.p.period, self.p.devfactor))
        self.log('OBV period: %d' % self.p.obv_period)
        self.log('CMF period: %d, threshold: %.2f' % (self.p.cmf_period, self.p.cmf_threshold))

    def log(self, txt, dt=None):
        dt = self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    data = bt.feeds.YahooFinanceData(dataname='EURUSD=X', fromdate=pd.Timestamp('2019-01-01'),
                                     todate=pd.Timestamp('2021-01-01'), reverse=False)
    cerebro.adddata(data)
    cerebro.addstrategy(OBVCMFStrategy)
    cerebro.run()
    cerebro.plot()

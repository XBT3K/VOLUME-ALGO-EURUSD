import backtrader as bt
import backtrader.indicators as btind

class VolumeOBVCMF(bt.Strategy):
    params = (
        ('period', 20),
        ('cmf_level', 0.0),
        ('obv_level', 0.0)
    )

    def __init__(self):
        self.cmf = btind.ChaikinMoneyFlow(self.data, period=self.params.period)
        self.obv = btind.OnBalanceVolume(self.data)

    def next(self):
        if not self.position:
            if self.cmf > self.params.cmf_level and self.obv > self.params.obv_level:
                self.buy()
        else:
            if self.cmf < self.params.cmf_level and self.obv < self.params.obv_level:
                self.sell()

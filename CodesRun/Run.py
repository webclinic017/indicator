import sys

sys.path.insert(0, "BacktraderBots")
from Backtrader import *



bt = Backtrader(
               exchange='binance',
               symbol1='ETHUSDT',
               symbol2='BTCUSDT',
               candletype='spot',
               timeframe='1h',
               start_date=None,
               end_date=None,
               dayslength=30,
               tp_stop=0.03,
               sl_stop=0.01,
               fees=0.001,
               R_high=4,
               R_low=1,
               showPlots=False,
               )

print(bt.BackTrading())

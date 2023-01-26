import numpy as np
import vectorbt as vbt
import pandas as pd
import numpy as np
import talib
from numba import njit
import warnings
import time
import sys


sys.path.insert(0, "IndicatorBots")
from Indicators import *



class Backtrader():


    """
    Indicator class: A class that use forvest data and build some indicators. 

            Attributes:
                    Indicator: exchange of candlestick data, must be str like 'binance'
                    tp_stop: symbol of candlestick data, must be str like 'BTCUSDT'
                    candletype: candletype of candlestick data, 
                                    must be str and should selected between 'spot' or 'futures'
                    timeframe: timeframe of candlestick data and should selected between
                                    '1h', '4h', '1d', '1w','1M'.
                    start_date: start_date of candlestick data and must be datetime.datetime format.
                    end_date: end_date of candlestick data and must be datetime.datetime format.
                    dayslength: dayslength of candlestick data and is an int number.
                    symboldata: containing a DataFrame of requested symbol, which indexed with timestamp
                    close: a pandas Series with timestamp index, contained close price.
                    open: a pandas Series with timestamp index, contained open price
                    low: a pandas Series with timestamp index, contained low price
                    high:a pandas Series with timestamp index, contained high price
                    volume:a pandas Series with timestamp index, contained volume price

            Methods:
                    Create __init__: 
                            Inputs: dataFrame
                            Functionality: prepare self attributes and reade and prepare date from Forvest database.
                            Output: None
                    
    """

    def __init__(self, exchange='binance', symbol1='ETHUSDT', symbol2='BTCUSDT', candletype='spot'
                    , timeframe='1h', start_date=None, end_date=None, dayslength=30
                    , tp_stop=0.03, sl_stop=0.01, fees=0.001, R_high=4, R_low=1, showPlots=False):
        
        self.Indicator = Indicator(exchange=exchange, symbol1=symbol1, symbol2=symbol2, candletype=candletype
                    , timeframe=timeframe, start_date=start_date, end_date=end_date, dayslength=dayslength)        
        self.tp_stop = tp_stop
        self.sl_stop = sl_stop
        self.fees = fees
        self.R_high = R_high
        self.R_low = R_low
        self.showPlots = showPlots
    
    def produce_signal(symbol1_close,state_6h,state_6D, R_high, R_low):
        trend = np.where((state_6D-state_6h>R_high), -1, 0)
        trend = np.where((state_6D-state_6h<R_low), 1, trend)
        return trend



    def BackTrading(self):

        symbol1_close=self.Indicator.AltcoinBTC()['symbol1_close']
        symbol1_close_length = len(symbol1_close)
        state_6h=self.Indicator.AltcoinBTC()['normalized_volume_6h']
        state_6h = np.asarray([np.nan]*(symbol1_close_length-len(state_6h))+list(state_6h))
        state_6D=self.Indicator.AltcoinBTC()['normalized_volume_6D']
        state_6D = np.asarray([np.nan]*(symbol1_close_length-len(state_6D))+list(state_6D))


        start_time = time.time()
        warnings.filterwarnings('ignore')
        
        ind = vbt.IndicatorFactory(
            class_name = 'Combination',
            short_name = 'comb',
            param_names= ['R_high','R_low'],
            input_names = ['symbol1_close','state_6h','state_6D'],
            output_names = ['value']
            ).from_custom_func(
                Backtrader.produce_signal,
                R_high = self.R_high,
                R_low = self.R_low,
                )
        res = ind.run(
            symbol1_close,
            state_6h,
            state_6D,
            R_high = self.R_high,
            R_low = self.R_low,
            )

        entries = res.value==1
        exits = res.value==-1

        pf=vbt.Portfolio.from_signals(symbol1_close,
                                        entries=entries,
                                        exits=exits,
                                        tp_stop=self.tp_stop,
                                        sl_stop=self.sl_stop,
                                        fees=self.fees,
                                        )

        returns = pf.total_return()
        end_time = time.time()
        print(returns)
        print(pf.stats())
        print(pf.orders.stats())
        print(pf.trades.records_readable)
        if self.showPlots==True:
            pf.plot().show()
        print(f'\n Backtest_elapsed_time = {end_time-start_time}')

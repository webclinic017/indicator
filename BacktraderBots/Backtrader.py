import numpy as np
import vectorbt as vbt
import pandas as pd
import numpy as np
import talib
from numba import njit
import warnings
import time
import sys
import os

sys.path.insert(0, "IndicatorBots")
from Indicators import AltcoinBTC

def produce_signal(symbols_exchange='binance', symbol1_name='ETHUSDT', symbol2_name='BTCUSDT', symbols_candletype='spot'
                , symbols_timeframe='1h', symbols_start_date=None, symbols_end_date=None, symbols_dayslength=30
                , ):
    
    altcoinBTC = AltcoinBTC(symbols_exchange=symbols_exchange, symbol1_name=symbol1_name, symbol2_name=symbol2_name
                            , symbols_candletype=symbols_candletype, symbols_timeframe=symbols_timeframe
                            , symbols_start_date=symbols_start_date, symbols_end_date=symbols_end_date
                            , symbols_dayslength=symbols_dayslength)
    state_6h = altcoinBTC['normalized_volume_6h']
    # state_6h = np.concatenate(state_6h)
    state_6h = np.asarray(state_6h)
    state_6D = altcoinBTC['normalized_volume_6D']
    # state_6D = np.concatenate(state_6D)
    state_6h_length = len(state_6h)
    state_6D = np.asarray([np.nan]*(state_6h_length-len(state_6D))+list(state_6D))
    trend = np.where((state_6D-state_6h>4), -1, 0)
    trend = np.where((state_6D-state_6h<1), 1, trend)
    trend = np.array([0]*(len(altcoinBTC['symbol1_close'])-state_6h_length)+list(trend))
    symbol1_close = altcoinBTC['symbol1_close']
    return trend, symbol1_close


def BackTrader(symbols_exchange='binance', symbol1_name='ETHUSDT', symbol2_name='BTCUSDT', symbols_candletype='spot'
                , symbols_timeframe='1h', symbols_start_date=None, symbols_end_date=None, symbols_dayslength=30
                , tp_stop=0.03, sl_stop=0.01, fees=0.001):


    start_time = time.time()
    warnings.filterwarnings('ignore')
    
    ind = vbt.IndicatorFactory(
        class_name = 'Combination',
        short_name = 'comb',
        param_names= ['tp_stop','sl_stop','fees'],
        input_names = ['symbols_exchange','symbol1_name','symbol2_name'
                        , 'symbols_candletype', 'symbols_timeframe'
                        , 'symbols_start_date', 'symbols_end_date'
                        , 'symbols_dayslength'],
        
        output_names = ['trend', 'symbol1_close']
        ).from_custom_func(
            produce_signal,
            tp_stop = tp_stop,
            sl_stop = sl_stop,
            fees = fees,
            )
    res = ind.run(

        symbols_exchange=symbols_exchange,
        symbol1_name=symbol1_name,
        symbol2_name=symbol2_name,
        symbols_candletype=symbols_candletype,
        symbols_timeframe=symbols_timeframe,
        symbols_start_date=symbols_start_date,
        symbols_end_date=symbols_end_date,
        symbols_dayslength=symbols_dayslength,
        tp_stop = tp_stop,
        sl_stop = sl_stop,
        fees = fees,
        
        )

    entries = res.value==1
    exits = res.value==-1

    pf=vbt.Portfolio.from_signals(res.symbol1_close,
                                    entries=entries,
                                    exits=exits,
                                    tp_stop=tp_stop,
                                    sl_stop=sl_stop,
                                    fees=fees,
                                    )

    returns = pf.total_return()
    end_time = time.time()
    print(returns)
    print(pf.stats())
    print(pf.orders.stats())
    print(pf.trades.records_readable)
    pf.plot().show()
    print(f'\n Backtest_elapsed_time = {end_time-start_time}')





BackTrader(symbols_exchange='binance', symbol1_name='ETHUSDT', symbol2_name='BTCUSDT', symbols_candletype='spot'
                , symbols_timeframe='1h', symbols_start_date=None, symbols_end_date=None, symbols_dayslength=30
                , tp_stop=0.03, sl_stop=0.01, fees=0.001)



# print(produce_signal(symbols_exchange='binance', symbol1_name='ETHUSDT', symbol2_name='BTCUSDT', symbols_candletype='spot'
                # , symbols_timeframe='1h', symbols_start_date=None, symbols_end_date=None, symbols_dayslength=30))
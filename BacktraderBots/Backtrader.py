import numpy as np
import vectorbt as vbt
import pandas as pd
import numpy as np
import talib
from numba import njit
import warnings
import time
import sys

sys.path.insert(0, "E:\\TradingBot\\indicator\\DataClasses")
from ForvestData import *


def AltcoinBTC(symbol1_closes, symbol2_closes, symbol1_volumes, symbol2_volumes):

    period6h = 6
    period1D = 24
    period6D = 144
    '''Calculating volume and close reates'''
    close_rate1_2_6h = [(symbol1_closes[i+period6h]/symbol1_closes[i]-1)-(symbol2_closes[i+period6h]/symbol2_closes[i]-1) for i in reversed(range(len(symbol1_closes)-period6h))]
    close_rate1_2_1D = [(symbol1_closes[i+period1D]/symbol1_closes[i]-1)-(symbol2_closes[i+period1D]/symbol2_closes[i]-1) for i in reversed(range(len(symbol1_closes)-period1D))]
    close_rate1_2_6D = [(symbol1_closes[i+period6D]/symbol1_closes[i]-1)-(symbol2_closes[i+period6D]/symbol2_closes[i]-1) for i in reversed(range(len(symbol1_closes)-period6D))]
    volume_rate1_2_6h = [(symbol1_volumes[i+period6h]/symbol1_volumes[i]-1)-(symbol2_volumes[i+period6h]/symbol2_volumes[i]-1) for i in reversed(range(len(symbol1_volumes)-period6h))]
    volume_rate1_2_1D = [(symbol1_volumes[i+period1D]/symbol1_volumes[i]-1)-(symbol2_volumes[i+period1D]/symbol2_volumes[i]-1) for i in reversed(range(len(symbol1_volumes)-period1D))]
    volume_rate1_2_6D = [(symbol1_volumes[i+period6D]/symbol1_volumes[i]-1)-(symbol2_volumes[i+period6D]/symbol2_volumes[i]-1) for i in reversed(range(len(symbol1_volumes)-period6D))]
   
    '''Calculating normalized close of different timeframes '''
    mean_close_6h = np.mean(close_rate1_2_6h)
    sd_close_6h = np.sqrt(np.var(close_rate1_2_6h))
    normalized_close_6h = [(_-mean_close_6h)/sd_close_6h for _ in close_rate1_2_6h]
    mean_close_1D = np.mean(close_rate1_2_1D)
    sd_close_1D = np.sqrt(np.var(close_rate1_2_1D))
    normalized_close_1D = [(_-mean_close_1D)/sd_close_1D for _ in close_rate1_2_1D]
    mean_close_6D = np.mean(close_rate1_2_6D)
    sd_close_6D = np.sqrt(np.var(close_rate1_2_6D))
    normalized_close_6D = [(_-mean_close_6D)/sd_close_6D for _ in close_rate1_2_6D]
   
    '''Calculating normalized volume of different timeframes '''
    mean_volume_6h = np.mean(volume_rate1_2_6h)
    sd_volume_6h = np.sqrt(np.var(volume_rate1_2_6h))
    normalized_volume_6h = [(_-mean_volume_6h)/sd_volume_6h for _ in volume_rate1_2_6h]
    mean_volume_1D = np.mean(volume_rate1_2_1D)
    sd_volume_1D = np.sqrt(np.var(volume_rate1_2_1D))
    normalized_volume_1D = [(_-mean_volume_1D)/sd_volume_1D for _ in volume_rate1_2_1D]
    mean_volume_6D = np.mean(volume_rate1_2_6D)
    sd_volume_6D = np.sqrt(np.var(volume_rate1_2_6D))
    normalized_volume_6D = [(_-mean_volume_6D)/sd_volume_6D for _ in volume_rate1_2_6D]

    multiple_normalized_colse_volume_6h =[normalized_close_6h[_]+normalized_volume_6h[_] for _ in range(len(normalized_close_6h))]
    multiple_normalized_colse_volume_1D =[normalized_close_1D[_]+normalized_volume_1D[_] for _ in range(len(normalized_close_1D))]
    multiple_normalized_colse_volume_6D =[normalized_close_6D[_]+normalized_volume_6D[_] for _ in range(len(normalized_close_6D))]
    result = { 
            # 'l_close_inteval':min(normalized_close_6h+normalized_close_1D+normalized_close_6D),
            # 'U_close_interval': max(normalized_close_6h+normalized_close_1D+normalized_close_6D),
            'state_close_6h':normalized_close_6h[-1],
            'state_close_1D':normalized_close_1D[-1],
            'state_close_6D':normalized_close_6D[-1],
            'normalized_close_6h': normalized_close_6h,
            'normalized_close_1D': normalized_close_1D,
            'normalized_close_6D': normalized_close_6D,
            # 'l_volume_inteval':min(normalized_volume_6h+normalized_volume_1D+normalized_volume_6D),
            # 'U_volume_interval': max(normalized_volume_6h+normalized_volume_1D+normalized_volume_6D),
            'state_volume_6h':normalized_volume_6h[-1],
            'state_volume_1D':normalized_volume_1D[-1],
            'state_volume_6D':normalized_volume_6D[-1],
            'normalized_volume_6h': normalized_volume_6h,
            'normalized_volume_1D': normalized_volume_1D,
            'normalized_volume_6D': normalized_volume_6D,
            # 'l_multiple_normalized_colse_volume_inteval':min(multiple_normalized_colse_volume_6h+multiple_normalized_colse_volume_1D+multiple_normalized_colse_volume_6D),
            # 'U_multiple_normalized_colse_volume_interval': max(multiple_normalized_colse_volume_6h+multiple_normalized_colse_volume_1D+multiple_normalized_colse_volume_6h),
            'state_multiple_colse_volume_6h': multiple_normalized_colse_volume_6h[-1],
            'state_multiple_colse_volume_1D': multiple_normalized_colse_volume_1D[-1],
            'state_multiple_colse_volume_6D': multiple_normalized_colse_volume_6D[-1],
            # 'multiple_normalized_colse_volume_6h':multiple_normalized_colse_volume_6h,
            # 'multiple_normalized_colse_volume_1D':multiple_normalized_colse_volume_1D,
            # 'multiple_normalized_colse_volume_6D':multiple_normalized_colse_volume_6D,
            
            }
    return result


start_time = time.time()
warnings.filterwarnings('ignore')




# @njit
def produce_signal(close1, close2,volume1, volume2):
    altcoinBTC = AltcoinBTC(close1, close2,volume1, volume2)
    state_6h = altcoinBTC['normalized_volume_6h']
    state_6h = np.concatenate(state_6h)
    state_6h = np.asarray(state_6h)
    state_6D = altcoinBTC['normalized_volume_6D']
    state_6D = np.concatenate(state_6D)
    state_6h_length = len(state_6h)
    state_6D = np.asarray([np.nan]*(state_6h_length-len(state_6D))+list(state_6D))
    trend = np.where((state_6D-state_6h>4), -1, 0)
    trend = np.where((state_6D-state_6h<1), 1, trend)
    trend = np.array([0]*(len(close1)-state_6h_length)+list(trend))
    return trend


ind = vbt.IndicatorFactory(
    class_name = 'Combination',
    short_name = 'comb',
    input_names = ['close1','close2','volume1', 'volume2'],
    output_names = ['value']
    ).from_custom_func(
        produce_signal,
        ) 
res = ind.run(
    symbol1_closes,
    symbol2_closes,
    symbol1_volumes,
    symbol2_volumes,
    
    )
# print(sum(res.value!=0))
entries = res.value==1
exits = res.value==-1

pf=vbt.Portfolio.from_signals(symbol1_closes,
                                entries=entries,
                                exits=exits,
                                # tp_stop=0.03,
                                # sl_stop=0.01,
                                fees=0.001,
                                
                                )

returns = pf.total_return()
print(returns)
# print(returns.to_string(),
#      '\n',
#      returns.max(),
#      returns.idxmax(),
#      )

print(pf.stats())
print(pf.orders.stats())
print(pf.trades.records_readable)
pf.plot().show()

#  f'\n elapsed_time = {end_time-start_time}'
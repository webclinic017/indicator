import pandas as pd
import numpy as np
import requests
import sys

# def AltcoinBTC(symbol1='ETHUSDT', symbol2='BTCUSDT'):

#     timeframe = '1h'
#     period1 = 6
#     period2 = 24
#     period3 = 144
#     symbol1_address=f'https://candles-forvest.iran.liara.run/api/v1/candles2?exchange=binance&symbol={symbol1}&type=spot&tf={timeframe}'
#     symbol2_address = f'https://candles-forvest.iran.liara.run/api/v1/candles2?exchange=binance&symbol={symbol2}&type=spot&tf={timeframe}'
#     symbol1_request = requests.get(symbol1_address,timeout=(120,120)).json()
#     symbol2_request = requests.get(symbol2_address,timeout=(120,120)).json()
#     symbol1_data = pd.DataFrame(dict(symbol1_request)['data'])
#     symbol2_data = pd.DataFrame(dict(symbol2_request)['data'])
#     symbol1_values = [float(_) for _ in symbol1_data['close']]
#     symbol2_values = [float(_) for _ in symbol2_data['close']]
#     rate1_2_1 = [(symbol1_values[i+period1]/symbol1_values[i]-1)-(symbol2_values[i+period1]/symbol2_values[i]-1) for i in reversed(range(min(len(symbol1_values),len(symbol2_values))-period1))]
#     rate1_2_2 = [(symbol1_values[i+period2]/symbol1_values[i]-1)-(symbol2_values[i+period2]/symbol2_values[i]-1) for i in reversed(range(min(len(symbol1_values),len(symbol2_values))-period2))]
#     rate1_2_3 = [(symbol1_values[i+period3]/symbol1_values[i]-1)-(symbol2_values[i+period3]/symbol2_values[i]-1) for i in reversed(range(min(len(symbol1_values),len(symbol2_values))-period3))]
#     mean1 = np.mean(rate1_2_1)
#     sd1 = np.sqrt(np.var(rate1_2_1))
#     normalized1 = [(_-mean1)/sd1 for _ in rate1_2_1]
#     mean2 = np.mean(rate1_2_2)
#     sd2 = np.sqrt(np.var(rate1_2_2))
#     normalized2 = [(_-mean2)/sd2 for _ in rate1_2_2]
#     mean3 = np.mean(rate1_2_3)
#     sd3 = np.sqrt(np.var(rate1_2_3))
#     normalized3 = [(_-mean3)/sd3 for _ in rate1_2_3]
#     result = { 'l_interval':min(normalized1+normalized2+normalized3),
#             'U_interval': max(normalized1+normalized2+normalized3),
#             'state_6h':normalized1[-1],
#             'state_1D':normalized2[-1],
#             'state_6D':normalized3[-1],
#             }
#     return result
sys.path.insert(0, "DataClasses")
from ForvestData import SymbolData




def AltcoinBTC(symbols_exchange='binance', symbol1_name='ETHUSDT', symbol2_name='BTCUSDT', symbols_candletype='spot'
                , symbols_timeframe='1h', symbols_start_date=None, symbols_end_date=None, symbols_dayslength=30
                , ):
        '''Loading and preparing data from Forvest database for two requesred symbols'''
        symbol1_data = SymbolData(exchange=symbols_exchange, symbol=symbol1_name, candletype=symbols_candletype
                        , timeframe=symbols_timeframe, start_date=symbols_start_date, end_date=symbols_end_date
                        , dayslength=symbols_dayslength)

        symbol2_data = SymbolData(exchange=symbols_exchange, symbol=symbol2_name, candletype=symbols_candletype
                        , timeframe=symbols_timeframe, start_date=symbols_start_date, end_date=symbols_end_date
                        , dayslength=symbols_dayslength)

        symbol1_close = symbol1_data.close
        symbol2_close = symbol2_data.close
        symbol1_volume = symbol1_data.volume
        symbol2_volume = symbol2_data.volume



        if type(symbol1_close) != list:
                symbol1_close = list(symbol1_close)
        if type(symbol2_close) != list:
                symbol2_close = list(symbol2_close)
        if type(symbol1_volume) != list:
                symbol1_volume = list(symbol1_volume)
        if type(symbol2_volume) != list:
                symbol2_volume = list(symbol2_volume)
        
        
        period6h = 6
        period1D = 24
        period6D = 144
        '''Calculating volume and close reates'''
        close_rate1_2_6h = [(symbol1_close[i+period6h]/symbol1_close[i]-1)-(symbol2_close[i+period6h]/symbol2_close[i]-1) for i in reversed(range(len(symbol1_close)-period6h))]
        close_rate1_2_1D = [(symbol1_close[i+period1D]/symbol1_close[i]-1)-(symbol2_close[i+period1D]/symbol2_close[i]-1) for i in reversed(range(len(symbol1_close)-period1D))]
        close_rate1_2_6D = [(symbol1_close[i+period6D]/symbol1_close[i]-1)-(symbol2_close[i+period6D]/symbol2_close[i]-1) for i in reversed(range(len(symbol1_close)-period6D))]
        volume_rate1_2_6h = [(symbol1_volume[i+period6h]/symbol1_volume[i]-1)-(symbol2_volume[i+period6h]/symbol2_volume[i]-1) for i in reversed(range(len(symbol1_volume)-period6h))]
        volume_rate1_2_1D = [(symbol1_volume[i+period1D]/symbol1_volume[i]-1)-(symbol2_volume[i+period1D]/symbol2_volume[i]-1) for i in reversed(range(len(symbol1_volume)-period1D))]
        volume_rate1_2_6D = [(symbol1_volume[i+period6D]/symbol1_volume[i]-1)-(symbol2_volume[i+period6D]/symbol2_volume[i]-1) for i in reversed(range(len(symbol1_volume)-period6D))]

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
                'symbol1_close': symbol1_close,
                'symbol2_close': symbol2_close,
                'symbol1_volume': symbol1_volume,
                'symbol2_volume': symbol2_volume,

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


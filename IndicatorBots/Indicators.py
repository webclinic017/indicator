import pandas as pd
import numpy as np
import sys
sys.path.insert(0, "DataReaderBots")
from ForvestData import SymbolData



class Indicator():
        """
        Indicator class: A class that use forvest data and build some indicators. 

                Attributes:
                        exchange: exchange of candlestick data, must be str like 'binance'
                        symbol: symbol of candlestick data, must be str like 'BTCUSDT'
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
                        , timeframe='1h', start_date=None, end_date=None, dayslength=30):
                
                symbol1 = SymbolData(exchange=exchange, symbol=symbol1, candletype=candletype
                                , timeframe=timeframe, start_date=start_date, end_date=end_date
                                , dayslength=dayslength)
                symbol2 = SymbolData(exchange=exchange, symbol=symbol2, candletype=candletype
                                , timeframe=timeframe, start_date=start_date, end_date=end_date
                                , dayslength=dayslength)


                
                
                ## Attributes
                self.symbol1_data = symbol1.symboldata
                self.symbol2_data = symbol2.symboldata
                self.symbol1_close = symbol1.close
                self.symbol2_close = symbol2.close
                self.symbol1_volume = symbol1.volume
                self.symbol2_volume = symbol2.volume




        def AltcoinBTC(self):

                        
                '''Loading and preparing data from Forvest database for two requesred symbols'''
                

                symbol1_close = self.symbol1_close
                symbol2_close = self.symbol2_close
                symbol1_volume = self.symbol1_volume
                symbol2_volume = self.symbol2_volume



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

import requests
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import datetime




class ForvestData():
     """
     TVdata class: A class that read data from an api forvest address, then changes it to a pandas dataframe. 

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


          Methods:
                    Create __init__: 
                         Inputs: dataFrame
                         Functionality: prepare self attributes
                         Output: None

                    SymbolData(self):
                         Inputs: None
                         Functionality: reade and prepare date from Forvest database.
                         Output: symbol data as a pandas DataFrome.
                    
     """

     def __init__(self, exchange='binance', symbol='BTCUSDT', candletype='spot'
                    , timeframe='1h', start_date=None, end_date=None, dayslength=30):
          ## Attributes
          self.exchange = exchange
          self.symbol = symbol
          self.candletype = candletype
          self.timeframe = timeframe
          self.start_date = start_date
          self.end_date = end_date
          self.dayslength = dayslength
        


     def SymbolData(self):

          lengthdays = self.dayslength
          candletype = self.candletype
          timeframe = self.timeframe
          symbol = self.symbol
          exchange = self.exchange
          
          if self.end_date is None:
               end_date = datetime.datetime.now()
          else:
               end_date = self.end_date
          
          if self.start_date is None:
               start_date = end_date - datetime.timedelta(days=lengthdays)
          else:
               start_date = self.start_date

          if candletype!='futures' or candletype!='spot':
               raise Exception("Candletype is incorrect. it must be 'futures' or 'spot' ")
          if timeframe not in ['1h', '4h', '1d', '1w','1M']:
               raise Exception("Timeframe is incorrect. it must be '1h', '4h', '1d', '1w' or '1M'.") 
          if not isinstance(symbol, str):
               raise Exception("Symbol is incorrect. it must be str.") 
          if not isinstance(exchange, str):
               raise Exception("Exchange is incorrect. it must be str.") 

          end_timestamp = int(end_date.timestamp())*1000
          start_timestamp = int(start_date.timestamp())*1000

          symbol_address = f'https://candles-forvest.iran.liara.run/api/v1/candles?exchange={exchange}&symbol={symbol}&type={candletype}&tf={timeframe}&startTime={start_timestamp}&endTime={end_timestamp}'
          symbol_request = requests.get(symbol_address,timeout=(120,120)).json()
          symbol_data = pd.DataFrame(dict(symbol_request)['data'])
          return symbol_data


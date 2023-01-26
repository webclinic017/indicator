import requests
import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import datetime




class SymbolData():
     """
     SymbolData class: A class that read data from an api forvest address, then changes it to a pandas dataframe. 

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
          self.symboldata = None
          self.close = None
          self.open = None
          self.low = None
          self.high = None
          self.volume = None

          
          if self.end_date is None:
               end_date = datetime.datetime.now()
          else:
               end_date = self.end_date
          
          if self.start_date is None:
               start_date = end_date - datetime.timedelta(days=self.dayslength)
          else:
               start_date = self.start_date

          if self.candletype not in ['futures', 'spot']:
               raise Exception("Candletype is incorrect. it must be 'futures' or 'spot' ")
          if self.timeframe not in ['1h', '4h', '1d', '1w','1M']:
               raise Exception("Timeframe is incorrect. it must be '1h', '4h', '1d', '1w' or '1M'.") 
          if not isinstance(self.symbol, str):
               raise Exception("Symbol is incorrect. it must be str.") 
          if not isinstance(self.exchange, str):
               raise Exception("Exchange is incorrect. it must be str.") 

          end_timestamp = int(end_date.timestamp())*1000
          start_timestamp = int(start_date.timestamp())*1000

          symbol_address = f'https://candles-forvest.iran.liara.run/api/v1/candles?exchange={self.exchange}&symbol={self.symbol}&type={self.candletype}&tf={self.timeframe}&startTime={start_timestamp}&endTime={end_timestamp}'
          symbol_request = requests.get(symbol_address,timeout=(120,120)).json()
          self.symboldata = pd.DataFrame(dict(symbol_request)['data'])
          timestamp = self.symboldata['openTime'].apply(lambda x: datetime.datetime.fromtimestamp(x/1000))
          self.symboldata.index = timestamp
          self.high = pd.to_numeric(self.symboldata['high'])
          self.open = pd.to_numeric(self.symboldata['open'])
          self.close = pd.to_numeric(self.symboldata['close'])
          self.low = pd.to_numeric(self.symboldata['low'])
          self.volume = pd.to_numeric(self.symboldata['volume'])



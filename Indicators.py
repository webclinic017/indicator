import pandas as pd
import numpy as np
import requests

def AltcoinBTC(symbol1='ETHUSDT', symbol2='BTCUSDT'):

    timeframe = '1h'
    period1 = 6
    period2 = 24
    period3 = 144
    symbol1_address=f'https://candles-forvest.iran.liara.run/api/v1/candles2?exchange=binance&symbol={symbol1}&type=spot&tf={timeframe}'
    symbol2_address = f'https://candles-forvest.iran.liara.run/api/v1/candles2?exchange=binance&symbol={symbol2}&type=spot&tf={timeframe}'
    symbol1_request = requests.get(symbol1_address,timeout=(120,120)).json()
    symbol2_request = requests.get(symbol2_address,timeout=(120,120)).json()
    symbol1_data = pd.DataFrame(dict(symbol1_request)['data'])
    symbol2_data = pd.DataFrame(dict(symbol2_request)['data'])
    symbol1_values = [float(_) for _ in symbol1_data['close']]
    symbol2_values = [float(_) for _ in symbol2_data['close']]
    rate1_2_1 = [(symbol1_values[i+period1]/symbol1_values[i]-1)-(symbol2_values[i+period1]/symbol2_values[i]-1) for i in reversed(range(min(len(symbol1_values),len(symbol2_values))-period1))]
    rate1_2_2 = [(symbol1_values[i+period2]/symbol1_values[i]-1)-(symbol2_values[i+period2]/symbol2_values[i]-1) for i in reversed(range(min(len(symbol1_values),len(symbol2_values))-period2))]
    rate1_2_3 = [(symbol1_values[i+period3]/symbol1_values[i]-1)-(symbol2_values[i+period3]/symbol2_values[i]-1) for i in reversed(range(min(len(symbol1_values),len(symbol2_values))-period3))]
    mean1 = np.mean(rate1_2_1)
    sd1 = np.sqrt(np.var(rate1_2_1))
    normalized1 = [(_-mean1)/sd1 for _ in rate1_2_1]
    mean2 = np.mean(rate1_2_2)
    sd2 = np.sqrt(np.var(rate1_2_2))
    normalized2 = [(_-mean2)/sd2 for _ in rate1_2_2]
    mean3 = np.mean(rate1_2_3)
    sd3 = np.sqrt(np.var(rate1_2_3))
    normalized3 = [(_-mean3)/sd3 for _ in rate1_2_3]
    result = { 'l_interval':min(normalized1+normalized2+normalized3),
            'U_interval': max(normalized1+normalized2+normalized3),
            'state_6h':normalized1[-1],
            'state_1D':normalized2[-1],
            'state_6D':normalized3[-1],
            }
    return result


def IndicatorNeedlePointer(symbol1='ETHUSDT', symbol2='BTCUSDT'):
        altcoinBTC = AltcoinBTC(symbol1='ETHUSDT', symbol2='BTCUSDT')
        l_interval = altcoinBTC['l_interval']
        U_interval = altcoinBTC['U_interval']
        state_6h = altcoinBTC['state_6h']
        state_1D = altcoinBTC['state_1D']
        state_6D = altcoinBTC['state_6D']

        scaler = round(abs(l_interval-U_interval)/8)/10
        if max(abs(l_interval),abs(U_interval))==abs(l_interval):
                edited_U_interval = round(l_interval+(8*scaler*10))
                edited_l_interval = round(l_interval)
        else:
                edited_l_interval = round(U_interval-(8*scaler*10))
                edited_U_interval = round(U_interval)
        
        str_6h = list(str(state_6h))
        pointindex_6h = str_6h.index('.')
        if int(str_6h[pointindex_6h+1])%2==0:
                edited_state_6h = float(''.join(str_6h[0:pointindex_6h+2]))
        else:
                str_6h[pointindex_6h+1] = str(int(str_6h[pointindex_6h+1])+1)
                edited_state_6h = float(''.join(str_6h[0:pointindex_6h+2]))
        
        str_1D = list(str(state_1D))
        pointindex_1D = str_1D.index('.')
        if int(str_1D[pointindex_1D+1])%2==0:
                edited_state_1D = float(''.join(str_1D[0:pointindex_1D+2]))
        else:
                str_1D[pointindex_1D+1] = str(int(str_1D[pointindex_1D+1])+1)
                edited_state_1D = float(''.join(str_1D[0:pointindex_1D+2]))
        
        str_6D = list(str(state_6D))
        pointindex_6D = str_6D.index('.')
        if int(str_6D[pointindex_6D+1])%2==0:
                edited_state_6D = float(''.join(str_6D[0:pointindex_6D+2]))
        else:
                str_6D[pointindex_6D+1] = str(int(str_6D[pointindex_6D+1])+1)
                edited_state_6D = float(''.join(str_6D[0:pointindex_6D+2]))

        result = { 'l_interval':edited_l_interval,
            'U_interval': edited_U_interval,
            'state_6h':edited_state_6h,
            'state_1D':edited_state_1D,
            'state_6D':edited_state_6D,
            'scaler':scaler
            }
        return result


print(IndicatorNeedlePointer(symbol1='ETHUSDT', symbol2='BTCUSDT'),AltcoinBTC(symbol1='ETHUSDT', symbol2='BTCUSDT'))
import sys
sys.path.insert(0, "IndicatorBots")
from Indicators import AltcoinBTC

def IndicatorNeedlePointer(symbol1='ETHUSDT', symbol2='BTCUSDT'):
        altcoinBTC = AltcoinBTC(symbol1=symbol1, symbol2=symbol2)
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
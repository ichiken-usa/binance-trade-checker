import numpy as np
import pandas as pd
import mplfinance as mpf

# 期間
data_range = pd.date_range('2021/01/01', '2021/12/31 23:59', freq='T')
print(data_range)

# 単純ランダムウォーク
dn = np.random.randint(2, size=len(data_range))*2 - 1
print(dn)
print(dn.size)

p0 = 100 # 初期値
vol = 1.5 # ボラティリティ

# ボラティリティを分変動率に変換
vol_m = vol/np.sqrt(365*24*60) 
print(vol_m)

# 累積積
gwalk = np.cumprod(np.exp(vol_m*dn))*p0
print(gwalk)

# 4本値データ算出
df = pd.Series(gwalk, index=data_range).resample('1W').ohlc().dropna()
print(df)

# ローソク足表示
mpf.plot(df, type='candle')
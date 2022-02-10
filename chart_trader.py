import pandas as pd
import mplfinance as mpf
from glob import glob

def read_csvs_as_df(dir):

    # 引数のパスからファイルのリスト作成
    csv_files_dir = glob(dir)
    print(csv_files_dir)

    # CSVファイルごとのDF配列
    marged_csv = [pd.read_csv(f, header=None, usecols=[0,1], index_col=[0], parse_dates=True) for f in csv_files_dir]

    # CSVファイルごとのDFを結合（インデックスをリセット）
    df = pd.concat(marged_csv, ignore_index=False)

    return df

# ファイルパス
dir = './Data'

# フォルダ内のCSVをワイルドカード指定し、全部読み込んで一つのDFに結合
csv_dir = dir+'/v14_*.csv'
df = read_csvs_as_df(csv_dir)
print(df)

# CSVデータ読み込み
print(df)
print(df.index)

# 4本値データ算出
df_ohlc = df[1].resample('1D').ohlc()
print(df_ohlc)

# ローソク足表示
mpf.plot(df_ohlc, type='candle', style='binance', title='\n\nPortfolio Value')
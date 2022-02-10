import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
# Excelの取り込みはopenpyxl

# BinanceのExcelデータ読み込み
dir = './Data/Trade_History-202202.xlsx'
df = pd.read_excel(dir, index_col=[0])
print('--- 取引履歴Excelファイルの中身 ---')
print(df)

# 末尾のUSDとUSDTを消去
a = pd.Series(df['Market'])
a = a.str.replace('USDT', '')
df['Market'] = a.str.replace('USD', '')
print(df)

# 通貨ごとに売買の合計を算出
df_pivot_sum = pd.pivot_table(df, index='Market', columns='Type', values='Total', aggfunc='sum')
print('--- 通貨ごとの売買合計ピボット ---')
print(df_pivot_sum)

# SELLとBUYの差分計算
df_pivot_sum['DIFF'] = df_pivot_sum['SELL'] - df_pivot_sum['BUY']
print('--- 売りと買いの差分列を追加 ---')
print(df_pivot_sum)

# 損益計算
order_diff = df_pivot_sum['DIFF'].sum()
buy_total = df_pivot_sum['BUY'].sum()
sell_total = df_pivot_sum['SELL'].sum()
fee = (buy_total + sell_total) * 0.075 * 0.01 # 手数料0.075%をBNB支払い
profit = order_diff - fee

# 各通貨ペアごとの取引回数
df_pivot_count = pd.pivot_table(df, index='Market', columns='Type', values='Total', aggfunc='count', margins=True, margins_name='TTL')
df_pivot_count2 = pd.pivot_table(df, index='Market', columns='Type', values='Total', aggfunc='count', margins=False)


print('--- 各オーダー回数 ---')
print(df_pivot_count)

print('--- 評価 ---')
print(f'BUY TTL:    $ {buy_total}')
print(f'SELL TTL:   $ {sell_total}')
print(f'Diff:       $ {order_diff}')
print(f'Fee:        $ {fee}')
print(f'Profit:     $ {profit}')

# グラフウィンドウ1
fig1 = plt.figure(figsize=(6,6))

# グラフ1
ax1 = fig1.add_subplot(2,1,1)
ax1.bar(df_pivot_sum.index, df_pivot_sum['DIFF'])
ax1.set_xlabel('Market')
ax1.set_ylabel('Profit ($)')
ax1.set_title('Profit of each cryptocurrency')
ax1.grid(axis='y')

# グラフ2
ax2 = fig1.add_subplot(2,1,2)
ax2.bar(df_pivot_count2.index, df_pivot_count2['BUY'], align='edge', width=-0.3, label='Buy')
ax2.bar(df_pivot_count2.index, df_pivot_count2['SELL'], align='edge', width=0.3, label='Sell')
ax2.set_xlabel('Market')
ax2.set_ylabel('Times')
ax2.set_title('Number of buys and sells of each cryptocurrency')
ax2.legend()
ax2.grid(axis='y')

plt.subplots_adjust(hspace=0.6)
plt.show()


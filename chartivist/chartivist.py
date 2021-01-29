import yfinance as yf 
import pandas as pd 
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
from talib import MFI, MACD, RSI
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

print('Chartivist v2.0')
symbol = input("Symbol (AAPL / DVAX / TSLA): ")
ticker = yf.Ticker(symbol)
history = ticker.history(period="1y", interval="1d")
  
open_prices = history['Open']
close_prices = history['Close']
high_prices = history['High']
low_prices = history['Low']
volume = history['Volume']
macd, macd_signal, macd_hist = MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
rsi = RSI(close_prices)
mfi = MFI(high_prices, low_prices, close_prices, volume)

plt.figure(figsize=[20,15])
plt.suptitle(symbol)

price = plt.subplot(4, 1, 1)
price.plot(close_prices.index, close_prices, label='Price')
price.grid(True)
price.legend(loc=2)
price.set_yscale("log")
price.yaxis.set_major_formatter(ScalarFormatter())
price.yaxis.set_minor_formatter(ScalarFormatter())

volume_ax = plt.subplot(4, 1, 2, sharex = price)
pos = open_prices - close_prices < 0
neg = open_prices - close_prices > 0
volume_ax.bar(close_prices.index.to_numpy()[pos], volume[pos], color='green', width=1, align='center')
volume_ax.bar(close_prices.index.to_numpy()[neg], volume[neg], color='red', width=1, align='center')

macd_ax = plt.subplot(4, 1, 3, sharex = price)
macd_ax.plot(close_prices.index, macd, label='MACD:26:12')
macd_ax.plot(close_prices.index, macd_signal, label='MACD Signal:9')
macd_ax.legend(loc=2)

rsi_ax = plt.subplot(4, 1, 4, sharex = price)
rsi_ax.plot(close_prices.index, rsi, label='RSI:14')
rsi_ax.plot(close_prices.index, mfi, label='MFI:14')
rsi_ax.legend(loc=2)

plt.tight_layout()
plt.show()
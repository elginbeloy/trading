import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import ScalarFormatter
import datetime

# Calculates the SMA/EMA RSI (Relative Strength Index)
def get_rsi(close_prices, period = 14, ema=False):
  deltas = close_prices.diff()
  positive_deltas, negative_deltas = deltas.copy(), deltas.copy()
  positive_deltas[positive_deltas<0] = 0.0
  negative_deltas[negative_deltas>0] = 0.0

  if ema:
    avg_gain = positive_deltas.ewm(span=period).mean()
    avg_loss = negative_deltas.abs().ewm(span=period).mean()
  else:
    avg_gain = positive_deltas.rolling(window=period).mean()
    avg_loss = negative_deltas.abs().rolling(window=period).mean()

  return 100 - 100 / (1 + avg_gain / avg_loss)

# Calculates Wilders Smoothed RSI (Relative Strength Index)
def get_wilder_rsi(close_prices, period = 14):
  deltas = close_prices.diff().to_numpy()
  rsi_array = np.empty(deltas.shape[0])
  index = period + 1

  smoothed_avg_gain = np.sum(deltas[1:index].clip(0)) / period
  smoothed_avg_loss = -np.sum(deltas[1:index].clip(-1000, 0)) / period

  # Calculates RSI using the Wilder smoothing method
  for delta in deltas[index:]:
    smoothed_avg_gain = ((smoothed_avg_gain * (period-1)) + delta if delta > 0 else 0) / period
    smoothed_avg_loss = ((smoothed_avg_loss * (period-1)) + delta if delta < 0 else 0) / period
    if smoothed_avg_loss != 0:
      relative_strength = smoothed_avg_gain / smoothed_avg_loss
      rsi_array[index] = 100 - (100 / (1 + relative_strength))
    else:
      rsi_array[index] = 100
    
    index += 1

  return pd.Series(rsi_array)

# Calculates the MFI (Money Flow Index)
def get_mfi(close_prices, high_prices, low_prices, volume, period = 14):
  typical_price = (close_prices + high_prices + low_prices) / 3
  raw_money_flow = typical_price * volume
  rmf_deltas = raw_money_flow.diff()
  positive_deltas, negative_deltas = rmf_deltas.copy(), rmf_deltas.copy()
  positive_deltas[positive_deltas<0] = 0.0
  negative_deltas[negative_deltas>0] = 0.0

  period_gain = positive_deltas.rolling(window=period).sum()
  period_loss = negative_deltas.abs().rolling(window=period).sum()

  return 100 - 100 / (1 + period_gain / period_loss)

def encode_date_arr_as_day_of_week(dates):
  arr = np.zeros((len(dates), 7), dtype=float)
  for date_index, date in enumerate(dates):
    converted_datetime = pd.Timestamp(date).to_pydatetime()
    arr[date_index][converted_datetime.weekday()] = 1.0
  return arr.transpose()

def encode_date_arr_as_month_of_year(dates):
  arr = np.zeros((len(dates), 12), dtype=float)
  for date_index, date in enumerate(dates):
    converted_datetime = pd.Timestamp(date).to_pydatetime()
    arr[date_index][converted_datetime.month - 1] = 1.0
  return arr.transpose()

def log_normalize_arr(arr):
  # to avoid its log being undefined
  arr = arr.fillna(0.00001)
  arr = arr.replace([0], 0.0001)
  return np.log(arr)

def append_ticker_to_x_y(ticker, x, y, lookback_period=30, n=1, p=2, plot=False):
  # TODO: Account for stock-splits, dividends and other price
  daily = ticker.history(period="2y", interval="1d")
  open_prices = daily.iloc[:,0]
  high_prices = daily.iloc[:,1]
  low_prices = daily.iloc[:,2]
  close_prices = daily.iloc[:,3]
  volume = daily.iloc[:,4]
  
  # Averages
  close_6day_sma = close_prices.rolling(window=6).mean()
  close_12day_sma = close_prices.rolling(window=12).mean()
  close_26day_sma = close_prices.rolling(window=26).mean()
  close_50day_sma = close_prices.rolling(window=50).mean()
  close_6day_ema = close_prices.ewm(span=12).mean()
  close_12day_ema = close_prices.ewm(span=12).mean()
  close_26day_ema = close_prices.ewm(span=26).mean()
  close_50day_ema = close_prices.ewm(span=50).mean()

  # MACD - Mean Average Convergence Divergence 
  macd = close_12day_ema - close_26day_ema
  signal = macd.ewm(span=9).mean()

  # RSI - Relative Strength Index
  rsi_5day = get_rsi(close_prices, period=5)
  rsi = get_rsi(close_prices)
  rsi_ema = get_rsi(close_prices, ema=True)

  # MFI - Money Flow Index (Volume Weighted RSI)
  money_flow_index = get_mfi(
    close_prices, 
    high_prices, 
    low_prices,
    volume)

  if plot:
    print('Graphing metrics for sanity/validity check...')

    # Plot all metrics for a sanity check prior to adding to training data
    plt.figure(figsize=[20,15])
    plt.suptitle(ticker)

    price = plt.subplot(4, 1, 1)
    price.plot(close_prices.index, close_prices, label='Price')
    price.plot(close_prices.index, close_6day_sma, label='6-Day SMA')
    price.plot(close_prices.index, close_50day_sma, label='50-Day SMA')
    price.plot(close_prices.index, close_6day_ema, label='6-Day EMA')
    price.plot(close_prices.index, close_50day_ema, label='50-Day EMA')
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
    macd_ax.plot(close_prices.index, signal, label='MACD Signal:9')
    macd_ax.legend(loc=2)

    rsi_ax = plt.subplot(4, 1, 4, sharex = price)
    rsi_ax.plot(close_prices.index, rsi_5day, label='RSI:5')
    rsi_ax.plot(close_prices.index, rsi, label='RSI:14')
    rsi_ax.plot(close_prices.index, rsi_ema, label='RSI-EMA:14')
    rsi_ax.plot(close_prices.index, money_flow_index, label='MFI:14')
    rsi_ax.legend(loc=2)

    plt.tight_layout()
    plt.show()

    correct = input('Look correct? y/N')
    if correct != 'y':
      print(open_prices.head(20))
      print(high_prices.head(20))
      print(low_prices.head(20))
      print(close_prices.head(20))
      print(volume.head(20))

      print('6 DAY SMA:')
      print(close_6day_sma.head(20))
      print('12 DAY SMA:')
      print(close_12day_sma.head(20))
      print('26 DAY SMA:')
      print(close_26day_sma.head(20))
      print('50 DAY SMA:')
      print(close_50day_sma.head(20))

      print('6 DAY EMA:')
      print(close_6day_ema.head(20))
      print('12 DAY EMA:')
      print(close_12day_ema.head(20))
      print('26 DAY EMA:')
      print(close_26day_ema.head(20))
      print('50 DAY EMA:')
      print(close_50day_ema.head(20))
    
      print('MACD')
      print(macd.head(20))
      print('MACD Signal')
      print(signal.head(20))

      print('RSI:5')
      print(rsi_5day.head(20))
      print('RSI:14')
      print(rsi.head(20))
      print('RSI:14 EMA')
      print(rsi_ema.head(20))
      print('MFI:14')
      print(money_flow_index.head(20))

      exit()
  
  for day in range(50, len(close_prices), lookback_period): 
    x.append(np.array([
      *encode_date_arr_as_day_of_week(close_prices.index.values[day-lookback_period:day]),
      *encode_date_arr_as_month_of_year(close_prices.index.values[day-lookback_period:day]),
      log_normalize_arr(open_prices[day-lookback_period:day]),
      log_normalize_arr(close_prices[day-lookback_period:day]),
      log_normalize_arr(low_prices[day-lookback_period:day]),
      log_normalize_arr(high_prices[day-lookback_period:day]),
      log_normalize_arr(volume[day-lookback_period:day] / 10000),
      log_normalize_arr(close_6day_sma[day-lookback_period:day]),
      log_normalize_arr(close_12day_sma[day-lookback_period:day]),
      log_normalize_arr(close_26day_sma[day-lookback_period:day]),
      log_normalize_arr(close_50day_sma[day-lookback_period:day]),
      log_normalize_arr(close_6day_ema[day-lookback_period:day]),
      log_normalize_arr(close_12day_ema[day-lookback_period:day]),
      log_normalize_arr(close_26day_ema[day-lookback_period:day]),
      log_normalize_arr(close_50day_ema[day-lookback_period:day]),
      macd[day-lookback_period:day].to_numpy() / 10,
      signal[day-lookback_period:day].to_numpy() / 10,
      rsi[day-lookback_period:day].to_numpy() / 100,
      rsi_ema[day-lookback_period:day].to_numpy() / 100,
      rsi_5day[day-lookback_period:day].to_numpy() / 100,
      money_flow_index[day-lookback_period:day].to_numpy() / 100
    ]).transpose())
    
    # True if there was a high representing n% asset appreciation within the period
    increased_over_n = [(high_price - open_prices[day]) >= (open_prices[day] * n / 100) for high_price in high_prices[day:day+p]]
    decreased_over_n = [(open_prices[day] - low_price) >= (open_prices[day] * n / 100) for low_price in low_prices[day:day+p]]
    should_buy = 1 if sum(increased_over_n) > 0 and sum(decreased_over_n) == 0 else 0
    y.append([should_buy])
import pandas as pd
import numpy as np

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


def zero_mean_center(series):
  # to avoid its log being undefined
  series = series.fillna(0.0)
  return ((series - series.mean()) / series.std()).to_numpy()


def get_training_data(symbol_bars, lookback_bar_amount, target_appreciation_percentage, max_depreciation_percentage, max_holding_period_bars, evaluation=False):
  x = []
  y = []

  for symbol in symbol_bars:
    bars = symbol_bars[symbol]
    
    open_prices = bars['open']
    high_prices = bars['high']
    low_prices = bars['low']
    close_prices = bars['close']
    vwa_prices = bars['vwap']
    volume = bars['volume']
    proportion_buy_ticks = bars['proportion_buy_ticks']
    buy_dollar_volume = bars['buy_dollar_volume']
    sell_dollar_volume = bars['buy_dollar_volume']

    bar_range = range(
      lookback_bar_amount, 
      len(close_prices) - (max_holding_period_bars + 1), 
      lookback_bar_amount)
    for period_end_bar in bar_range:
      period_start_bar = period_end_bar-lookback_bar_amount
      period_open_prices = open_prices.iloc[period_start_bar:period_end_bar] 
      period_close_prices = close_prices.iloc[period_start_bar:period_end_bar]
      period_low_prices = low_prices.iloc[period_start_bar:period_end_bar]
      period_high_prices = high_prices.iloc[period_start_bar:period_end_bar]
      period_vwa_prices = vwa_prices.iloc[period_start_bar:period_end_bar]
      period_volume = volume.iloc[period_start_bar:period_end_bar]
      period_proportion_buy_ticks = proportion_buy_ticks.iloc[period_start_bar:period_end_bar]
      period_buy_dollar_volume = buy_dollar_volume.iloc[period_start_bar:period_end_bar]
      period_sell_dollar_volume = sell_dollar_volume.iloc[period_start_bar:period_end_bar]

      if (period_open_prices.std() == 0 or period_close_prices.std() == 0 or
        period_low_prices.std() == 0 or period_high_prices.std() == 0 or 
        period_vwa_prices.std() == 0 or period_proportion_buy_ticks.std() == 0 or 
        period_volume.std() == 0 or period_buy_dollar_volume.std() == 0 or
        period_sell_dollar_volume.std() == 0):
        print(f'{symbol}: Cant use this cuz std is 0')
        continue

      x.append(np.array([
        *encode_date_arr_as_day_of_week(period_close_prices.index.values),
        *encode_date_arr_as_month_of_year(period_close_prices.index.values),
        zero_mean_center(period_open_prices),
        zero_mean_center(period_close_prices),
        zero_mean_center(period_low_prices),
        zero_mean_center(period_high_prices),
        zero_mean_center(period_vwa_prices),
        zero_mean_center(period_volume),
        period_proportion_buy_ticks,
        zero_mean_center(period_buy_dollar_volume),
        zero_mean_center(period_sell_dollar_volume),
      ]).transpose())

      y_i = 0.0
      for bar in range(period_end_bar, period_end_bar+max_holding_period_bars):
        appreciation = high_prices.iloc[bar] - open_prices.iloc[period_end_bar]
        depreciation = open_prices.iloc[period_end_bar] - low_prices.iloc[bar]

        # True if there was a high representing n% asset appreciation within the period
        if appreciation >= (open_prices.iloc[period_end_bar] * target_appreciation_percentage / 100):
          y_i = 1.0
          break

        # False if there was a low representing d% asset depreciation within the period
        if depreciation >= (open_prices.iloc[period_end_bar] * max_depreciation_percentage / 100):
          y_i = 0.0
          break

      y.append([y_i])

  x, y = np.array(x), np.array(y)

  return x, y
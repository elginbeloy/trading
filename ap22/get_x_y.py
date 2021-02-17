import pandas as pd
import numpy as np
from util import log_to_file
from data_util import (
  real_value_scaled_minute_of_hour,
  one_hot_hour_of_day, 
  one_hot_day_of_week, 
  one_hot_day_of_month,
  one_hot_month_of_year,
  standardize_series,
)

def get_model_data(symbol_bars, lookback_bars, max_holding_period_bars, target_appreciation_percentage, max_depreciation_percentage, max_class_imbalance_percentage, evaluation=False):
  x = []
  y = []

  for symbol in symbol_bars:
    bars = symbol_bars[symbol]
    log_to_file(f"Symbol {symbol} has {len(bars)} bars!")
    
    open_prices = bars['o']
    high_prices = bars['h']
    low_prices = bars['l']
    close_prices = bars['c']
    volume = bars['v']
    vwa_prices = bars['vw']
    total_trades = bars['n']
    timestamps = bars['t']

    bar_range = range(
      lookback_bars, 
      len(close_prices) - (max_holding_period_bars + 1), 
      lookback_bars)
    for period_end_bar in bar_range:
      period_start_bar = period_end_bar-lookback_bars
      period_open_prices = open_prices.iloc[period_start_bar:period_end_bar] 
      period_close_prices = close_prices.iloc[period_start_bar:period_end_bar]
      period_low_prices = low_prices.iloc[period_start_bar:period_end_bar]
      period_high_prices = high_prices.iloc[period_start_bar:period_end_bar]
      period_volume = volume.iloc[period_start_bar:period_end_bar]
      period_vwa_prices = vwa_prices.iloc[period_start_bar:period_end_bar]
      period_total_trades = total_trades.iloc[period_start_bar:period_end_bar]
      period_timestamps = timestamps.iloc[period_start_bar:period_end_bar]

      if (period_open_prices.std() == 0 or period_close_prices.std() == 0 or
        period_low_prices.std() == 0 or period_high_prices.std() == 0 or 
        period_vwa_prices.std() == 0 or period_volume.std() == 0 or
        period_total_trades.std() == 0):
        log_to_file(f'{symbol}: Cant use a bar due to 0 std in data.')
        continue

      x_i = np.array([
        *real_value_scaled_minute_of_hour(period_timestamps),
        *one_hot_hour_of_day(period_timestamps),
        *one_hot_day_of_week(period_timestamps),
        *one_hot_day_of_month(period_timestamps),
        *one_hot_month_of_year(period_timestamps),
        standardize_series(period_open_prices),
        standardize_series(period_close_prices),
        standardize_series(period_low_prices),
        standardize_series(period_high_prices),
        standardize_series(period_volume),
        standardize_series(period_vwa_prices),
        standardize_series(period_total_trades)
      ]).transpose()

      y_i = 0.0
      for bar in range(period_end_bar, period_end_bar+max_holding_period_bars):
        appreciation = high_prices.iloc[bar] - open_prices.iloc[period_end_bar]
        depreciation = open_prices.iloc[period_end_bar] - low_prices.iloc[bar]

        # False if there was a low representing d% asset depreciation within the period
        if depreciation >= (open_prices.iloc[period_end_bar] * max_depreciation_percentage / 100):
          y_i = 0.0
          break

        # True if there was a high representing n% appreciation within the period
        if appreciation >= (open_prices.iloc[period_end_bar] * target_appreciation_percentage / 100):
          y_i = 1.0
          break

      if sum(y)/(len(y)+0.001) < max_class_imbalance_percentage / 100 and y_i == 1.0:
        x.append(x_i)
        y.append(y_i)

      if 1-(sum(y)/(len(y)+0.001)) < max_class_imbalance_percentage / 100 and y_i == 0.0:
        x.append(x_i)
        y.append(y_i)

  x, y = np.array(x), np.array(y).reshape(len(y), 1)

  return x, y
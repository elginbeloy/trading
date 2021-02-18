import numpy as np
from util import log_to_file
from get_model_data_util import (
  real_value_minute_of_day,
  real_value_day_of_year,
  one_hot_day_of_week, 
  standardize_series,
)

'''
Returns a dictionary containing sequence arrays of various values and the
accompanying triple barrier method label for the sequence.

Each returned array is 2 dimensional where each row contains the data of a 
single sequence, and there are sequence_length_bars rows.

Data returned:
==============
bar_values_arr: bar values (OHLCV+) for each bar in a sequence
minute_of_day_arr: minute of day values for each bar in a sequence
day_of_week_arr: one-hot day of week values for each bar in a sequence
day_of_year_arr: day of year values for each bar in a sequence
labels_arr: triple barrier method labels for the sequences

NOTE: sequence lengths are measured in bars, however bar size is dependent 
on the aggregation method used (time, tick, volume, imbalance, etc...)

NOTE: the different sequence values will be concatenated by the final model 
to create one final sequence to feed to the LSTM. We return the values 
seperately for two reasons:
1) to allow the model to have multiple inputs for embeddings/transformations
2) so we can add/remove new data without having to edit some big concat array,
instead we simply add a new model input and let it concat for us before feeding
the sequence to the LSTM
'''
def get_model_data(
  symbol_bars, 
  sequence_length_bars, 
  max_holding_period_bars, 
  target_appreciation_percentage, 
  max_depreciation_percentage, 
  max_class_imbalance_percentage):

  # Initialize empty arrays for each return value
  bar_values_arr = []
  minute_of_day_arr = []
  day_of_week_arr = []
  day_of_year_arr = []
  labels_arr = []

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

    # Iterate through bars grabbing a period of size sequence_length_bars 
    bar_range = range(
      sequence_length_bars, 
      len(open_prices) - (max_holding_period_bars + 1), 
      sequence_length_bars)
    for period_end_bar in bar_range:
      period_start_bar = period_end_bar-sequence_length_bars

      # Get array of bar values and timestamps for the period
      period_open_prices = open_prices.iloc[period_start_bar:period_end_bar] 
      period_close_prices = close_prices.iloc[period_start_bar:period_end_bar]
      period_low_prices = low_prices.iloc[period_start_bar:period_end_bar]
      period_high_prices = high_prices.iloc[period_start_bar:period_end_bar]
      period_volume = volume.iloc[period_start_bar:period_end_bar]
      period_vwa_prices = vwa_prices.iloc[period_start_bar:period_end_bar]
      period_total_trades = total_trades.iloc[period_start_bar:period_end_bar]
      period_timestamps = timestamps.iloc[period_start_bar:period_end_bar]

      # Verify standard_deviation is not zero, if it is we can't normalize
      if (period_open_prices.std() == 0 or period_close_prices.std() == 0 or
        period_low_prices.std() == 0 or period_high_prices.std() == 0 or 
        period_vwa_prices.std() == 0 or period_volume.std() == 0 or
        period_total_trades.std() == 0):
        log_to_file(f'{symbol}: Cant use a bar due to 0 std in data.')
        continue

      # Build period_bar_values by transposing the combined arrays
      period_bar_values = np.array([
        standardize_series(period_open_prices),
        standardize_series(period_close_prices),
        standardize_series(period_low_prices),
        standardize_series(period_high_prices),
        standardize_series(period_volume),
        standardize_series(period_vwa_prices),
        standardize_series(period_total_trades)
      ]).transpose()

      period_label = 0.0
      for bar in range(period_end_bar, period_end_bar+max_holding_period_bars):
        appreciation = high_prices.iloc[bar] - open_prices.iloc[period_end_bar]
        depreciation = open_prices.iloc[period_end_bar] - low_prices.iloc[bar]

        # False if there was a low representing d% asset depreciation within the period
        if depreciation >= (open_prices.iloc[period_end_bar] * max_depreciation_percentage / 100):
          period_label = 0.0
          break

        # True if there was a high representing n% appreciation within the period
        if appreciation >= (open_prices.iloc[period_end_bar] * target_appreciation_percentage / 100):
          period_label = 1.0
          break

      # TODO: make this more readable
      if ((sum(labels_arr)/(len(labels_arr)+0.001) < max_class_imbalance_percentage / 100 and period_label == 1.0) or
        (1-(sum(labels_arr)/(len(labels_arr)+0.001)) < max_class_imbalance_percentage / 100 and period_label == 0.0)):
        bar_values_arr.append(period_bar_values)
        minute_of_day_arr.append(real_value_minute_of_day(period_timestamps))
        day_of_week_arr.append(one_hot_day_of_week(period_timestamps))
        day_of_year_arr.append(real_value_day_of_year(period_timestamps))
        labels_arr.append(period_label)

  bar_values_arr = np.array(bar_values_arr)
  minute_of_day_arr = np.array(minute_of_day_arr)
  day_of_week_arr = np.array(day_of_week_arr)
  day_of_year_arr = np.array(day_of_year_arr)
  labels_arr = np.array(labels_arr).reshape(len(labels_arr), 1)

  return {
    'bar_values_arr': bar_values_arr,
    'minute_of_day_arr': minute_of_day_arr,
    'day_of_week_arr': day_of_week_arr,
    'day_of_year_arr': day_of_year_arr,
    'labels_arr': labels_arr
  }
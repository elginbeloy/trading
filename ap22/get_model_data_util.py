import pandas as pd
import numpy as np

# Encode an array of unix timestamps into an array of real number values
# representing the minute of the day the timestamp fell on.
def real_value_minute_of_day(dates):
  arr = np.zeros((len(dates), 1), dtype=float)
  for date_index, date in enumerate(dates):
    converted_datetime = pd.Timestamp(date).to_pydatetime()
    arr[date_index] = converted_datetime.minute + (converted_datetime.hour * 60)
  return arr

# Encode an array of unix timestamps into an array of real number values
# representing the day of the year the timestamp fell on.
def real_value_day_of_year(dates):
  arr = np.zeros((len(dates), 1), dtype=float)
  for date_index, date in enumerate(dates):
    converted_datetime = pd.Timestamp(date).to_pydatetime()
    arr[date_index] = converted_datetime.timetuple().tm_yday
  return arr

# Encode an array of unix timestamps into an array of one-hot arrays
# representing the day of the week the timestamp fell on.
def one_hot_day_of_week(dates):
  arr = np.zeros((len(dates), 7), dtype=float)
  for date_index, date in enumerate(dates):
    converted_datetime = pd.Timestamp(date).to_pydatetime()
    arr[date_index][converted_datetime.weekday()] = 1.0
  return arr

# Standardize a series, I.E zero mean center and divide by standard deviation.
def standardize_series(series):
  series = series.fillna(0.0)
  arr = ((series - series.mean()) / series.std()).to_numpy()
  return arr
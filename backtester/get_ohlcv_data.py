import pytz
import pandas as pd
from datetime import datetime
from polygon import RESTClient
from requests.exceptions import HTTPError

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"

# Queries time-interval bars from polygon directly
def get_time_interval_bars(symbol, interval, interval_multiplier, 
  start_date, end_date):

  print(f'[{symbol}-BARS] Fetching data from {start_date} to {end_date}...')

  with RESTClient(api_key) as client:
    results = []
    current_start_date = start_date
    while current_start_date != None:
      try:
        response = client.stocks_equities_aggregates(symbol, 
          interval_multiplier, interval, current_start_date, 
          end_date, limit=50000, unadjusted=False)

        if response.status != "OK":
          print(f"[STATUSError] Failed to fetch bars for {symbol}.")
          current_start_date = None
          continue
      except HTTPError as e:
        print(f"[HTTPError] Failed to fetch bars for {symbol}.")
        print(e)
        current_start_date = None
        continue

      # Hacky, but a response with less than 100 bars is likely the final period
      # so we can set the current_start_date back to None and end the loop.
      if response.resultsCount < 100:
        current_start_date = None
        continue

      results += response.results
      response_end_date = datetime.utcfromtimestamp(results[-1]['t'] // 1000)
      if response_end_date < datetime.strptime(end_date, '%Y-%m-%d'):
        current_start_date = response_end_date.strftime('%Y-%m-%d')
        print(f"[{symbol}-BARS] Hit 50k limit at {current_start_date} going to {end_date} (last appended {response.resultsCount})")
      else:
        current_start_date = None

    if len(results) < 0:
      print('No results!')
      exit()

    for result in results:
      result['t'] = datetime.utcfromtimestamp(result['t'] // 1000).astimezone(pytz.timezone("US/Eastern")).strftime('%Y-%m-%d')

    first_result_time = results[0]['t']
    final_result_time = results[-1]['t']

    print(f"[{symbol}-BARS] Queried {len(results)} bars {first_result_time} -> {final_result_time}")
    
    results = pd.DataFrame(results)
    results.columns = ['Volume', 'VolumeWeightedAvg', 'Open', 'Close', 'High', 'Low', 'Time', 'TickNumber']
    results['Time'] = pd.to_datetime(results['Time'])
    results.set_index('Time', inplace=True)
    print(f'[{symbol}-BARS] Complete!')

  return results
import os
import pandas as pd
import json
from tqdm import tqdm
from polygon import RESTClient
from util import log_to_file
from requests.exceptions import HTTPError

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"


'''
Downloads trade data (with bid/ask if included) to SSD to be used for 
aggregate bar creation.
'''
def download_trade_data(symbols, start_date, end_date, include_bid_ask=True,
  data_dir='./trade_data'):
  # Create the data directory if not doesn't already exist
  if not os.path.exists(data_dir):
    os.makedirs(data_dir)

  # Generate array of business day (weekday) dates from start_date to end_date
  days = pd.bdate_range(start=start_date, end=end_date).strftime("%Y-%m-%d")
  days = days.tolist()
  
  print("Downloading data...")
  with RESTClient(api_key) as client:
    for symbol in symbols:
      trades = []
      nbbos = []
      
      for day in tqdm(days):
        try:
          response = client.historic_trades_v2(symbol, day, limit=50000)
          if not response.success or not response.results_count:
            log_to_file(f"Failed to fetch {symbol} on {day}.")
            continue
          
          for trade in response.results:
            trades.append({'p': trade['p'], 's': trade['s'], 't': trade['t']})
          
          # If there are more than 50,000 trades, paginate through.
          while response.results_count == 50000:
            last_trade_timestamp = response.results[-1]['t']
            response = client.historic_trades_v2(symbol, day, 
              limit=50000, timestamp=last_trade_timestamp)
            for trade in response.results:
              trades.append({'p': trade['p'], 's': trade['s'], 't': trade['t']})

          # Get bid_ask data if included
          if include_bid_ask:
            response = client.historic_n___bbo_quotes_v2(symbol, day, limit=50000)
            if not response.success or not response.results_count:
              log_to_file(f"Failed to fetch {symbol} on {day}.")
              continue
            
            for nbbo in response.results:
              nbbos.append({
                'p': nbbo['p'], 's': nbbo['s'], 'P': nbbo['P'], 
                'S': nbbo['S'], 't': nbbo['t']})
            
            # If there are more than 50,000 trades, paginate through.
            while response.results_count == 50000:
              last_trade_timestamp = response.results[-1]['t']
              response = client.historic_n___bbo_quotes_v2(symbol, day, 
                limit=50000, timestamp=last_trade_timestamp)
              for nbbo in response.results:
                nbbos.append({
                  'p': nbbo['p'], 's': nbbo['s'], 'P': nbbo['P'], 
                  'S': nbbo['S'], 't': nbbo['t']})

        except HTTPError:
          log_to_file(f"Failed to fetch {symbol} on {day}.")
          pass

      with open(f"{data_dir}/{symbol}_trades.txt", 'w') as file:
        json.dump(trades, file)

      with open(f"{data_dir}/{symbol}_nbbos.txt", 'w') as file:
        json.dump(nbbos, file)
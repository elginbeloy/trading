import os
import pandas as pd
import json
from tqdm import tqdm
from datetime import datetime
from polygon import RESTClient
from util import log_to_file
from requests.exceptions import HTTPError

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"

# Get splits for a list of symbols 
def get_splits(symbols, start_date, end_date):
  start_date = datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")
  
  splits = {symbol: dict() for symbol in symbols}

  with RESTClient(api_key) as client:
    for symbol in symbols:
      response = client.reference_stock_splits(symbol)
      if len(response.results) == 0:
        log_to_file(f"Found no splits for {symbol}.")
        continue

      for result in response.results:
        splitDate = datetime.strptime(result["exDate"], "%Y-%m-%d")
        if splitDate > start_date and splitDate < end_date:
          splits[symbol][result["exDate"]] = {
            "date": splitDate, 
            "ratio": result["ratio"]}
  
  return splits

# Get dividends for a list of symbols 
def get_dividends(symbols, start_date, end_date):
  start_date = datetime.strptime(start_date, "%Y-%m-%d")
  end_date = datetime.strptime(end_date, "%Y-%m-%d")

  dividends = {symbol: dict() for symbol in symbols}
  
  with RESTClient(api_key) as client:
    for symbol in symbols:
      response = client.reference_stock_dividends(symbol)
      if len(response.results) == 0:
        log_to_file(f"Found no dividends for {symbol}.")
        continue
      
      for result in response.results:
        dividendDate = datetime.strptime(result["exDate"], "%Y-%m-%d")

        if dividendDate > start_date and dividendDate < end_date:
          dividends[symbol][result["exDate"]] = {
            "date": dividendDate, 
            "amount": result["amount"]}

  
  return dividends

# Downloads trade data (with bid/ask if included) to SSD for bar creation
def download_trade_data(symbols, start_date, end_date, include_bid_ask=True,
  data_dir='./trade_data'):
  # Create the data directory if not doesn't already exist
  if not os.path.exists(data_dir):
    os.makedirs(data_dir)

  # Generate array of weekday dates from start_date to end_date
  days = pd.bdate_range(
    start=start_date, end=end_date).strftime("%Y-%m-%d").tolist()

  dividends = get_dividends(symbols, start_date, end_date)
  splits = get_splits(symbols, start_date, end_date)
  
  print("Downloading data...")
  with RESTClient(api_key) as client:
    for symbol in symbols:
      trades = []
      nbbos = []
      
      for day in tqdm(days):
        dividend_amount, split_ratio = 0, 1
        if day in dividends[symbol]:
          dividend_amount = dividends[symbol][day]["amount"]

        if day in splits[symbol]:
          split_ratio = splits[symbol][day]["ratio"]

        try:
          response = client.historic_trades_v2(symbol, day, limit=50000)
          if not response.success or not response.results_count:
            log_to_file(f"Failed to fetch {symbol} on {day}.")
            continue
          
          for trade in response.results:
            trade_price = (trade['p'] / split_ratio) + dividend_amount
            trades.append({'p': trade_price, 's': trade['s'], 't': trade['t']})
          
          # If there are more than 50,000 trades, paginate through
          while response.results_count == 50000:
            last_trade_timestamp = response.results[-1]['t']
            response = client.historic_trades_v2(symbol, day, 
              limit=50000, timestamp=last_trade_timestamp)
            for trade in response.results:
              trade_price = (trade['p'] / split_ratio) + dividend_amount
              trades.append({'p': trade_price, 's': trade['s'], 't': trade['t']})

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
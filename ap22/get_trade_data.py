import pandas as pd
import numpy as np
from tqdm import tqdm
from polygon import RESTClient
from requests.exceptions import HTTPError

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"

# Returns trade data and average daily trading dollars for a list of symbols
def get_trades(symbols, start_date, end_date):
  trades = dict()
  average_dollars_traded_daily = dict()
  days = pd.bdate_range(start = start_date, end = end_date).strftime("%Y-%m-%d").tolist()

  with RESTClient(api_key) as client:
    for i in tqdm(range(len(symbols))):
      symbol = symbols[i]
      trades[symbol] = [[]]
      average_dollars_traded_daily[symbol] = 0.0
      valid_days = 0
      for day in days:
        try:
          response = client.historic_trades_v2(symbol, day, limit=50000)
          if not response.success or not response.results_count:
            print(f"Failed to fetch {symbol} on {day}.")
            continue

          valid_days += 1
          
          for trade in response.results:
            trades[symbol].append([trade['p'], trade['s'], trade['t']])
            average_dollars_traded_daily[symbol] += trade['p'] * trade['s']
          
          # If there are more than 50,000 trades, paginate through.
          while response.results_count == 50000:
            last_trade_timestamp = response.results[-1]['t']
            response = client.historic_trades_v2(symbol, day, 
              limit=50000, timestamp=last_trade_timestamp)
            for trade in response.results:
              trades[symbol].append([trade['p'], trade['s'], trade['t']])
              average_dollars_traded_daily[symbol] += trade['p'] * trade['s']
        
        except HTTPError as e:
          # print(f"Failed to fetch {symbol} on {day}.")
          pass

      average_dollars_traded_daily[symbol] /= valid_days
      trades[symbol] = np.array([trade for trade in trades[symbol] if len(trade) == 3])
      
      output = f"Queried {symbol} from {days[0]} to {days[-1]} | "
      output += f"Trade Total: {len(trades[symbol])} | "
      output += f"Traded $/Day: {average_dollars_traded_daily[symbol]}"
      print(output)

  return trades, average_dollars_traded_daily

def get_expected_dollars_per_bar(average_dollars_traded, desired_bars_per_day):
  expected_dollars_per_bar = dict()
  for symbol in average_dollars_traded:
    expected_dollars_per_bar[symbol] = average_dollars_traded[symbol] / desired_bars_per_day
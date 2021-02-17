import os
import pandas as pd
import numpy as np
import datetime as dt
from tqdm import tqdm
from polygon import RESTClient
from requests.exceptions import HTTPError

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"

symbols = input("Enter Comma-Seperated Symbols: ").split(',')
start_date = dt.datetime.strptime(input("Enter Start Date (%Y-%m-%d): "), "%Y-%m-%d")
end_date = dt.datetime.strptime(input("Enter End Date (%Y-%m-%d): "), "%Y-%m-%d")
data_dir = input('Enter Directory For Saving Data: ')

# Create data dir if it doesn't yet exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

days = pd.bdate_range(start = start_date, end = end_date).strftime("%Y-%m-%d").tolist()
with RESTClient(api_key) as client:
  for symbol in symbols:
    trades = [[]]
    average_dollars_traded_daily = 0.0
    valid_days = 0
    for day in tqdm(days):
      try:
        response = client.historic_trades_v2(symbol, day, limit=50000)
        if not response.success or not response.results_count:
          print(f"Failed to fetch {symbol} on {day}.")
          continue

        valid_days += 1
        
        for trade in response.results:
          trades.append([trade['p'], trade['s'], trade['t']])
          average_dollars_traded_daily += trade['p'] * trade['s']
        
        # If there are more than 50,000 trades, paginate through.
        while response.results_count == 50000:
          last_trade_timestamp = response.results[-1]['t']
          response = client.historic_trades_v2(symbol, day, 
            limit=50000, timestamp=last_trade_timestamp)
          for trade in response.results:
            trades.append([trade['p'], trade['s'], trade['t']])
            average_dollars_traded_daily += trade['p'] * trade['s']

      except HTTPError as e:
        # print(f"Failed to fetch {symbol} on {day}.")
        pass

    average_dollars_traded_daily /= valid_days
    trades = np.array([trade for trade in trades if len(trade) == 3])
      
    np.save(f'{data_dir}/{symbol}_{days[0]}_{days[-1]}', trades)
      
    output = f"Queried {symbol} from {days[0]} to {days[-1]} | "
    output += f"Trades: {len(trades)} | "
    output += f"Trade $/Day: {average_dollars_traded_daily}"
    print(output)
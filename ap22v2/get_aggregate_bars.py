import datetime as dt
import pandas as pd
import numpy as np
from tqdm import tqdm
from polygon import RESTClient
from requests.exceptions import HTTPError

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"

def get_time_interval_bars(symbols, multiplier, interval, start_date, end_date):
  symbol_bars = dict()

  with RESTClient(api_key) as client:
    for symbol in tqdm(symbols):
      try:
        response = client.stocks_equities_aggregates(symbol, multiplier, interval, start_date, end_date)
        if response.status != "OK" or not response.resultsCount:
          print(f"Failed to fetch bars for {symbol}.")
          continue
      except HTTPError:
        print(f"Failed to fetch bars for {symbol}.")

      symbol_bars[symbol] = pd.DataFrame(response.results)

  return symbol_bars

'''
def get_trade_imbalance_bars(symbol_trades, expected_bars_per_day):
  bars = dict()

  for symbol in symbol_trades:
    trades = symbol_trades[symbol]
    last_bar_trade_index = 0
    last_bar_was_buy = True
    buy_volume = 0.0
    sell_volume = 0.0
    total_buy_ticks = 0.0
    total_sell_ticks = 0.0
    threshold = expected_bar_sizes[symbol]
    bars[symbol] = pd.DataFrame(columns=[
      'start_time',
      'end_time',
      'open',
      'high',
      'low',
      'close',
      'vwap',
      'volume',
      'proportion_buy_ticks',
      'buy_dollar_volume',
      'sell_dollar_volume',
    ])

    for index in range(10, len(symbol_trades[symbol])):
      if symbol_trades[symbol][index - 1,0] > symbol_trades[symbol][index,0]:
        buy_volume += symbol_trades[symbol][index,0] * symbol_trades[symbol][index,1]
        total_buy_ticks += 1
        last_bar_was_buy = True
      elif symbol_trades[symbol][index - 1,0] < symbol_trades[symbol][index,0]:
        sell_volume += symbol_trades[symbol][index,0] * symbol_trades[symbol][index,1]
        total_sell_ticks += 1
        last_bar_was_buy = False
      else:
        if last_bar_was_buy:
          buy_volume += symbol_trades[symbol][index,0] * symbol_trades[symbol][index,1]
          total_buy_ticks += 1
        else:
          sell_volume += symbol_trades[symbol][index,0] * trasymbol_tradesdes[symbol][index,1]
          total_sell_ticks += 1

      bar_inflow = max(buy_volume, sell_volume)
      if bar_inflow >= threshold:
        # Get the indicators for this bar and append the bar
        volume_weighted_avg_price = (
          symbol_trades[symbol][last_bar_trade_index:index,0] * 
          symbol_trades[symbol][last_bar_trade_index:index,1]
        ).sum() / symbol_trades[symbol][last_bar_trade_index:index,1].sum()
        high_price = np.amax(symbol_trades[symbol][last_bar_trade_index:index,0], axis=0)
        low_price = np.amin(symbol_trades[symbol][last_bar_trade_index:index,0], axis=0)
        open_price = symbol_trades[symbol][last_bar_trade_index,0]
        close_price = symbol_trades[symbol][index,0]
        volume = symbol_trades[symbol][last_bar_trade_index:index,1].sum()

        start_timestamp = symbol_trades[symbol][last_bar_trade_index,2]
        end_timestamp = symbol_trades[symbol][index,2]

        start_time = dt.datetime.fromtimestamp(start_timestamp // 1000000000).strftime('%Y-%m-%d %H:%M:%S')
        end_time = dt.datetime.fromtimestamp(end_timestamp // 1000000000).strftime('%Y-%m-%d %H:%M:%S')
        
        # Append the bar to the pandas dataframe
        bars[symbol] = bars[symbol].append(pd.DataFrame({
          't': [start_time],
          'n': [number_of_trades_in_bar],
          'o': [open_price], 
          'h': [high_price], 
          'l': [low_price], 
          'c': [close_price], 
          'v': [volume],
          'vw' : [volume_weighted_avg_price]
        }))

        # Reset the bar trade index, buy volume, and sell volume
        last_bar_trade_index = index
        buy_volume = 0.0
        sell_volume = 0.0
        total_buy_ticks = 0.0
        total_sell_ticks = 0.0

        # Recalculate the threshold
        threshold = max(
          bars[symbol]["proportion_buy_ticks"].mean()*bars[symbol]["buy_dollar_volume"].mean(),
          (1-bars[symbol]["proportion_buy_ticks"]).mean()*bars[symbol]["sell_dollar_volume"].mean(),
        )

  return bars
'''

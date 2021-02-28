import pandas as pd
import numpy as np
from json import load
import pytz
from datetime import datetime
from os import listdir
from tqdm import tqdm
from polygon import RESTClient
from requests.exceptions import HTTPError
from util import log_to_file

api_key = "ESnn_eXGO4gk57uOohD6H7yfqB5_huCq"

# Queries time-interval bars from polygon directly
def get_time_interval_bars(symbols, interval, interval_multiplier, 
  start_date, end_date):
  symbol_bars = dict()

  with RESTClient(api_key) as client:
    for symbol in tqdm(symbols):
      results = []
      current_start_date = start_date
      while current_start_date != None:
        try:
          response = client.stocks_equities_aggregates(symbol, 
            interval_multiplier, interval, current_start_date, 
            end_date, limit=50000)

          if response.status != "OK":
            log_to_file(f"[STATUSError] Failed to fetch bars for {symbol}.")
            current_start_date = None
            continue
        except HTTPError as e:
          log_to_file(f"[HTTPError] Failed to fetch bars for {symbol}.")
          log_to_file(e)
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
          log_to_file(f"[{symbol}-BARS] Hit 50k limit at {current_start_date} going to {end_date} (last appended {response.resultsCount})")
        else:
          current_start_date = None

      if len(results) > 0:
        first_result_time = datetime.utcfromtimestamp(results[0]['t'] // 1000).astimezone(pytz.timezone("US/Eastern")).strftime('%Y-%m-%d %H-%M-%S')
        final_result_time = datetime.utcfromtimestamp(results[-1]['t'] // 1000).astimezone(pytz.timezone("US/Eastern")).strftime('%Y-%m-%d %H-%M-%S')

        log_to_file(f"[{symbol}-BARS] Queried {len(results)} bars {first_result_time} -> {final_result_time}")
        log_to_file(f"[{symbol}-BARS] {results[:3]} ... {results[-3:]}")
        symbol_bars[symbol] = pd.DataFrame(results)

  return symbol_bars

# Builds tick-interval bars from locally downloaded trade data
def get_tick_interval_bars(bar_size_ticks=1000, data_dir='./trade_data'):
  symbol_bars = dict()
  symbol_nbbos = dict()

  symbol_trade_files = [f for f in listdir(data_dir) if f.endswith('_trades.txt')]
  for symbol_file in symbol_trade_files:
    with open(f"{data_dir}/{symbol_file}") as file:
      symbol_trades = load(file)

    results = []
    for trade_index in range(0, len(symbol_trades), bar_size_ticks):
      bar_trades = symbol_trades[trade_index:trade_index+1000]
      bar_trade_prices = [trade['p'] for trade in bar_trades]
      bar_trade_sizes = [trade['s'] for trade in bar_trades]

      results.append({
        'o': bar_trade_prices[0],
        'h': max(bar_trade_prices),
        'l': min(bar_trade_prices),
        'c': bar_trade_prices[-1],
        'v': sum(bar_trade_sizes),
        'vw': sum(bar_trade_sizes) / 1000, # TODO: fix this
        't': symbol_trades[trade_index]['t']
      })

    if len(results) > 5:
      symbol_bars[symbol_file.split("_")[0]] = pd.DataFrame(results)

  return symbol_bars

# Builds volume-interval bars from locally downloaded trade data
# TODO: fix this
def get_volume_interval_bars(data_dir='./trade_data'):
  symbol_bars = dict()
  symbol_nbbos = dict()

  symbol_trade_files = [f for f in listdir(data_dir) if f.endswith('_trades.txt')]
  for symbol_file in symbol_trade_files:
    with open(f"{data_dir}/{symbol_file}") as file:
      symbol_trades = load(file)

    results = []
    for trade_index in range(0, len(symbol_trades), bar_size_ticks):
      bar_trades = symbol_trades[trade_index:trade_index+1000]
      bar_trade_prices = [trade['p'] for trade in bar_trades]
      bar_trade_sizes = [trade['s'] for trade in bar_trades]

      results.append({
        'o': bar_trade_prices[0],
        'h': max(bar_trade_prices),
        'l': min(bar_trade_prices),
        'c': bar_trade_prices[-1],
        'v': sum(bar_trade_sizes),
        'vw': sum(bar_trade_sizes) / 1000, # TODO: fix this
        't': symbol_trades[trade_index]['t']
      })

    symbol_bars[symbol_file.split("_")[0]] = pd.DataFrame(results)

  return symbol_bars

# Builds dollar-interval bars from locally downloaded trade data
# TODO: fix this
def get_dollar_interval_bars(data_dir='./trade_data'):
  symbol_bars = dict()
  symbol_nbbos = dict()

  symbol_trade_files = [f for f in listdir(data_dir) if f.endswith('_trades.txt')]
  for symbol_file in symbol_trade_files:
    with open(f"{data_dir}/{symbol_file}") as file:
      symbol_trades = load(file)

    results = []
    for trade_index in range(0, len(symbol_trades), bar_size_ticks):
      bar_trades = symbol_trades[trade_index:trade_index+1000]
      bar_trade_prices = [trade['p'] for trade in bar_trades]
      bar_trade_sizes = [trade['s'] for trade in bar_trades]

      results.append({
        'o': bar_trade_prices[0],
        'h': max(bar_trade_prices),
        'l': min(bar_trade_prices),
        'c': bar_trade_prices[-1],
        'v': sum(bar_trade_sizes),
        'vw': sum(bar_trade_sizes) / 1000, # TODO: fix this
        't': symbol_trades[trade_index]['t']
      })

    symbol_bars[symbol_file.split("_")[0]] = pd.DataFrame(results)

  return symbol_bars

'''
def get_imbalance_interval_bars(symbol_trades, expected_bars_per_day):
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

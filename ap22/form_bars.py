import datetime as dt
import pandas as pd
import numpy as np

def get_bars_from_trades(trades, expected_bar_sizes):
  bars = dict()

  for symbol in trades:
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

    for index in range(10, len(trades[symbol])):
      if trades[symbol][index - 1,0] > trades[symbol][index,0]:
        buy_volume += trades[symbol][index,0] * trades[symbol][index,1]
        total_buy_ticks += 1
        last_bar_was_buy = True
      elif trades[symbol][index - 1,0] < trades[symbol][index,0]:
        sell_volume += trades[symbol][index,0] * trades[symbol][index,1]
        total_sell_ticks += 1
        last_bar_was_buy = False
      else:
        if last_bar_was_buy:
          buy_volume += trades[symbol][index,0] * trades[symbol][index,1]
          total_buy_ticks += 1
        else:
          sell_volume += trades[symbol][index,0] * trades[symbol][index,1]
          total_sell_ticks += 1

      bar_inflow = max(buy_volume, sell_volume)
      if bar_inflow >= threshold:
        # Get the indicators for this bar and append the bar
        volume_weighted_avg_price = (
          trades[symbol][last_bar_trade_index:index,0] * 
          trades[symbol][last_bar_trade_index:index,1]
        ).sum() / trades[symbol][last_bar_trade_index:index,1].sum()
        high_price = np.amax(trades[symbol][last_bar_trade_index:index,0], axis=0)
        low_price = np.amin(trades[symbol][last_bar_trade_index:index,0], axis=0)
        open_price = trades[symbol][last_bar_trade_index,0]
        close_price = trades[symbol][index,0]
        volume = trades[symbol][last_bar_trade_index:index,1].sum()

        start_timestamp = trades[symbol][last_bar_trade_index,2]
        end_timestamp = trades[symbol][index,2]

        start_time = dt.datetime.fromtimestamp(start_timestamp // 1000000000).strftime('%Y-%m-%d %H:%M:%S')
        end_time = dt.datetime.fromtimestamp(end_timestamp // 1000000000).strftime('%Y-%m-%d %H:%M:%S')
        
        # Append the bar to the pandas dataframe
        bars[symbol] = bars[symbol].append(pd.DataFrame({
          'start_time': [start_time],
          'end_time': [end_time],
          'open': [open_price], 
          'high': [high_price], 
          'low': [low_price], 
          'close': [close_price], 
          'vwap' : [volume_weighted_avg_price],
          'volume': [volume],
          'proportion_buy_ticks': [(total_buy_ticks / (total_sell_ticks + 0.0001))],
          'buy_dollar_volume': [buy_volume],
          'sell_dollar_volume': [sell_volume]
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
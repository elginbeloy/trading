import os
from json import load
from datetime import datetime, timedelta, timezone
import pandas as pd
from get_trade_data import download_trade_data
import yfinance as yf

SYMBOLS_TO_DOWNLOAD = ['PLTR', 'PYPL', 'ZM']
# TODO: Ensure this accounts for a split/dividend day at some point for testing
DOWNLOAD_START_DATE = '2021-01-01'
DOWNLOAD_END_DATE = '2021-02-01'
TEST_DOWNLOAD_DIRECTORY = './test_trade_data'

# Verify the list of symbols are downloaded to the correct directory
def verify_trade_data_downloads():
  download_trade_data(
    SYMBOLS_TO_DOWNLOAD, 
    DOWNLOAD_START_DATE, 
    DOWNLOAD_END_DATE,
    include_bid_ask=False,
    data_dir=TEST_DOWNLOAD_DIRECTORY)

  # TEST_DOWNLOAD_DIRECTORY path should be created
  if not os.path.exists(TEST_DOWNLOAD_DIRECTORY):
    raise Exception("TEST_DOWNLOAD_DIRECTORY not created!")

  trade_files = []
  for f in os.listdir(TEST_DOWNLOAD_DIRECTORY):
    if f.endswith('_trades.txt'):
      trade_files.append(f)

  # Correct number of trade data files are downloaded
  if len(trade_files) != len(SYMBOLS_TO_DOWNLOAD):
    raise Exception("Incorrect number of trade files downloaded! " +
      f"Expected {len(SYMBOLS_TO_DOWNLOAD)} but found {len(trade_files)}.")
  
  # Each file has populated content as expected
  for file_name in trade_files:
    with open(f"{TEST_DOWNLOAD_DIRECTORY}/{file_name}") as f:
      content = load(f)
      if len(content) == 0:
        raise Exception(f"Content not loaded for {file_name}! Found: {content}")

# Verify the authenticity and adjustment of downloaded trade data
def verify_trade_data_authenticity(allowed_daily_disagreement=10):
  symbol_trades = dict()
  for symbol in SYMBOLS_TO_DOWNLOAD:
    with open(f"{TEST_DOWNLOAD_DIRECTORY}/{symbol}_trades.txt") as f:
      symbol_trades[symbol] = load(f)
  
  for symbol in symbol_trades:
    history = yf.Ticker(symbol).history(
      interval="1d", start=DOWNLOAD_START_DATE, end=DOWNLOAD_END_DATE)
    days = history.index.strftime("%Y-%m-%d").to_list()

    disagreement_amount = 0

    for day in days:
      day_trade_prices = []
      for trade in symbol_trades[symbol]:
        # Convert nanosecond timestamp to utc datetime object
        trade_dt = datetime.utcfromtimestamp(trade["t"] // 1000000000)
        day_dt = datetime.strptime(day, "%Y-%m-%d")
        if trade_dt > day_dt and trade_dt < day_dt + timedelta(days=1):
          day_trade_prices.append(trade["p"])

      high_price = max(day_trade_prices)
      low_price = min(day_trade_prices)
      open_price = day_trade_prices[0]
      close_price = day_trade_prices[-1]

      disagreement_amount += abs(high_price - history.loc[day]["High"])
      disagreement_amount += abs(low_price - history.loc[day]["Low"])
      disagreement_amount += abs(open_price - history.loc[day]["Open"])
      disagreement_amount += abs(close_price - history.loc[day]["Close"])

      if history.loc[day]["High"] != high_price:
        print(f"WARNING: {symbol} high on {day} ({high_price}) doesn't match yahoo ({history.loc[day]['High']})!")
      if history.loc[day]["Low"] != low_price:
        print(f"WARNING: {symbol} low on {day} ({low_price}) doesn't match yahoo ({history.loc[day]['Low']})!")
      if history.loc[day]["Open"] != open_price:
        print(f"WARNING: {symbol} open on {day} ({open_price}) doesn't match yahoo ({history.loc[day]['Open']})!")
      if history.loc[day]["Close"] != close_price:
        print(f"WARNING: {symbol} close on {day} ({close_price}) doesn't match yahoo ({history.loc[day]['Close']})!")

    allowed_disagreement = allowed_daily_disagreement * len(days)
    if disagreement_amount > allowed_disagreement:
      raise Exception(f"Disagreement amount for {symbol} exceeds ${allowed_disagreement} threshold.")

def verify_nbbo_data_download():
  return True

def verify_nbbo_data_adjustment():
  return True
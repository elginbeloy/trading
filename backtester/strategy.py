import pandas as pd
from pyfiglet import figlet_format
from termcolor import colored

'''
The Strategy class to be inherited and used when creating a backtest strategy.

Implements buy and sell functionality as well as data availability and metrics.
'''
class Strategy:
  def __init__(self, all_asset_dfs, initial_cash, commission_slippage):
    self.all_asset_dfs = all_asset_dfs
    self.initial_cash = initial_cash
    self.available_cash = initial_cash
    self.commission_slippage = commission_slippage

    self.asset_dfs = dict()
    self.current_day = str()
    self.trades = []

  # Returns a dictionary of available equity per symbol based on trade history
  def get_available_equity(self):
    equity = {symbol: 0 for symbol in self.all_asset_dfs.keys()}
    for trade in self.trades:
      if trade["type"] == "buy":
        equity[trade["symbol"]] += trade["amount"]
      elif trade["type"] == "sell":
        equity[trade["symbol"]] -= trade["amount"]

    return equity

  # TODO: Make work with short selling
  # Returns the average purchase price of an asset for calculating return
  def get_avg_asset_purchase_price(self, asset_symbol, amount):
    # Iterate through trades to determine the sum price of the asset trades
    # not yet "returned" - I.E not accounted for in a returning trade
    asset_sum_price = 0
    amount_to_return = amount
    for trade in self.trades:
      if trade["symbol"] == asset_symbol and trade["type"] == "buy":
        if trade["amount_returned"] != trade["amount"]:
          amount_returned = min(amount_to_return, trade["amount"] - trade["amount_returned"])
          trade["amount_returned"] += amount_returned
          amount_to_return -= amount_returned
          asset_sum_price += trade["total_price"] * (amount_returned / trade["amount"])

          if amount_to_return == 0:
            return asset_sum_price / amount

  def buy(self, asset_symbol, amount):
    asset_price = self.all_asset_dfs[asset_symbol].loc[self.current_day]["Close"]
    purchase_price = amount * asset_price
    purchase_price *= 1 + self.commission_slippage
    
    msg = f"{self.current_day}: {amount}x{asset_symbol} @ ${asset_price}"
    msg += f" | Total: ${purchase_price}"
    
    if self.available_cash >= purchase_price:
      print(f"Buy {msg}")
      self.available_cash -= purchase_price
      self.trades.append({
        "type": "buy",
        "day": self.current_day, 
        "symbol": asset_symbol, 
        "amount": amount, 
        "asset_price": asset_price, 
        "total_price": purchase_price,
        "amount_returned": 0})
    else:
      print(f"Insufficient funds to purchase {msg}")

  # TODO: Fix short functionality to account for loaning/calling
  def sell(self, asset_symbol, amount, short=False):
    asset_price = self.all_asset_dfs[asset_symbol].loc[self.current_day]["Close"]
    sale_price = amount * asset_price
    sale_price *= 1 - self.commission_slippage
    
    msg = f"{self.current_day}: {amount}x{asset_symbol} @ ${asset_price}"
    msg += f" | Total: ${sale_price}"
    
    if self.get_available_equity()[asset_symbol] >= amount or short:
      print(f"Sell {msg}")
      self.available_cash += sale_price
      avg_purchase_price = self.get_avg_asset_purchase_price(
            asset_symbol, amount)
      self.trades.append({
        "type": "sell",
        "day": self.current_day, 
        "symbol": asset_symbol, 
        "amount": amount, 
        "asset_price": asset_price, 
        "total_price": sale_price,
        "return": sale_price - (avg_purchase_price * amount),
        "return_percentage": ((sale_price / (avg_purchase_price * amount)) - 1) * 100})
    else:
      print(f"Insufficient equity to sell {msg}")

  # Advances current_day and updates the asset_dfs list
  def advance_to_day(self, day):
    self.current_day = day
    
    # Get list of assets with available data on the day
    self.asset_dfs = dict()
    for asset_symbol in self.all_asset_dfs.keys():
      if day in self.all_asset_dfs[asset_symbol].index:
        self.asset_dfs[asset_symbol] = self.all_asset_dfs[asset_symbol].loc[:day]

    self.next()

  def backtest(self, start_date, end_date):
    days = pd.bdate_range(start=start_date, end=end_date).strftime("%Y-%m-%d")
    for day in days.to_list():
      self.advance_to_day(day)

    # Liquidate all assets to get final metrics
    available_equity = self.get_available_equity()
    for asset_symbol in available_equity:
      if available_equity[asset_symbol] != 0:
        asset_price = self.all_asset_dfs[asset_symbol]["Close"][-1]
        sale_price = available_equity[asset_symbol] * asset_price
        sale_price *= 1 - self.commission_slippage
        self.available_cash += sale_price
        avg_purchase_price = self.get_avg_asset_purchase_price(
            asset_symbol, available_equity[asset_symbol])
        self.trades.append({
          "type": "sell",
          "day": self.current_day, 
          "symbol": asset_symbol, 
          "amount": available_equity[asset_symbol], 
          "asset_price": asset_price, 
          "total_price": sale_price,
          "return": sale_price - (avg_purchase_price * available_equity[asset_symbol]),
          "return_percentage": ((sale_price / (avg_purchase_price * available_equity[asset_symbol])) - 1) * 100})

    # Calculate metrics
    trade_sizes = [trade["total_price"] for trade in self.trades if "return" in trade]
    avg_trade_size = sum(trade_sizes) / len(trade_sizes)
    trade_returns = [trade["return"] for trade in self.trades if "return" in trade]
    avg_trade_return = sum(trade_returns) / len(trade_returns)
    highest_trade_return = max(trade_returns)
    lowest_trade_return = min(trade_returns)
    number_winning_trades = len([t for t in trade_returns if t >= 0])
    number_losing_trades = len([t for t in trade_returns if t < 0])

    trade_return_percentages = [trade["return_percentage"] for trade in self.trades if "return_percentage" in trade]
    avg_trade_return_percentage = sum(trade_return_percentages) / len(trade_return_percentages) 

    print()
    print(colored(figlet_format("Metrics"), "magenta"))
    print(f"Period: {start_date} - {end_date} ({len(days)} days)")
    print(f"Starting balance: ${self.initial_cash}")
    print(f"Final balance: ${self.available_cash}")
    print(f"Return [%]: {self.available_cash / self.initial_cash}")
    print(f"N-Over-A Buy-Hold Return [%]: ")
    print(f"Sharpe Ratio: ")
    # NOTE: Number of trades considers only closed out trades. 
    # I.E Buy 1xAAPL, 2xAAPL, 3xAAPL, Sell 6xAAPL is one "trade".
    # Note that commissions will be accounted for in each buy/sell.
    print(f"Number of Trades: {len(trade_returns)}")
    print(f"Number of Winning Trades: {number_winning_trades}")
    print(f"Number of Losing Trades: {number_losing_trades}")
    print(f"Probability of Win: {(number_winning_trades + 1) / (number_losing_trades + 1)}")
    print(f"Average Trade Return: ${avg_trade_return}")
    print(f"Average Trade Size: ${avg_trade_size}")
    print(f"Average Trade Return [%]: {avg_trade_return_percentage}")
    print(f"Highest Trade Return: ${highest_trade_return}")
    print(f"Lowest Trade Return: ${lowest_trade_return}")
    print(f"Trade Returns: {trade_returns}")
    print(f"Trade Sizes: {trade_sizes}")
    print(f"Trade Returns [%]: {trade_return_percentages}")

  # Get any buy/sell signals for present day data
  def extrapolate_future_predictions(self, cash, equity_positions, prediction_date, tradeable_asset_dfs):
    self.all_asset_dfs = tradeable_asset_dfs
    self.trades = []
    self.available_cash = cash
    for position in equity_positions:
      self.trades.append({})
    
    # Will print out buy/sell signals
    self.advance_to_day(prediction_date)

  # To be defined in the implemented subclass, called on advance_to_day
  def next(self):
    pass
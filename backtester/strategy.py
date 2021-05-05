import pandas as pd
from pyfiglet import figlet_format
from termcolor import colored
from utils import get_n_over_a_returns, add_column_to_asset_dfs, plot_asset_dfs

'''
The base strategy class inherited by strategy subclasses that implement 
specific create_signals and init logic.

A strategy takes in a dictionary of asset dataframes containing the OHLCV 
data for each asset. These can be for any time period and for any asset type. 
As long as the asset has a string identifier and a OHLCV dataframe it works.

Example assets_df: {'AAPL': pd.df, 'MSFT': pd.df}

A strategy subclass is simply a set of rules coded into the create_signals
function that will run everytime we advance in time - either in a backtest or 
in a live prediction scenario.

The create_signals function can call self.buy and self.sell to buy and sell
assets present in the assets_df at the current time.

>> NOTE: Only supports long-only strategies as short-selling is not yet possible.

>> NOTE: Only supports single time frame data availability.

>> NOTE: Only supports daily advancement in backtesting.
'''
class Strategy:
  def __init__(self, all_asset_dfs):
    self.all_asset_dfs = all_asset_dfs
    self.initial_cash = 0
    self.available_cash = 0
    self.commission_slippage = 0

    self.asset_dfs = dict()
    self.current_day = str()
    self.trades = []

    self.init()

  # To be defined in the implemented subclass, called on __init__
  def init(self):
    pass

  # To be defined in the implemented subclass, called on advance_to_day during
  # backtest or extrapolation
  def create_signals(self):
    pass

  # Add a column to all asset dataframes, created using values from input_columns
  # passed to assign_val_func - used to add indicators and other signals 
  def add_column_to_all_assets(self, column_name, input_columns, assign_val_func):
    add_column_to_asset_dfs(self.all_asset_dfs, column_name, 
      input_columns, assign_val_func)

  # Returns a dictionary of available equity per symbol based on trade history
  def get_available_equity(self):
    equity = {symbol: 0 for symbol in self.all_asset_dfs.keys()}
    for trade in self.trades:
      if trade["type"] == "buy":
        equity[trade["symbol"]] += trade["amount"]
      elif trade["type"] == "sell":
        equity[trade["symbol"]] -= trade["amount"]

    return equity

  '''
  Returns the purchase information of an asset for a "return" trade.

  Iterates through trades not yet "returned" - I.E not accounted for in a
  trade that returned liquidity and has a "return" associated with it -
  to get information like average purchase price and asset purchase dates.

  Ex. BUY 5xAAPL, BUY 5xAAPL, BUY 3xAAPL, SELL 13xAAPL 
  The one 13xAAPL sale has 3 associated purchase dates, amounts, and costs. 
  Thus, the return of the sale is calculated via the total purchase price of 
  the first purchase trades of the asset not yet returned.
  '''
  def get_asset_purchase_info(self, asset_symbol, return_trade_size):
    asset_sum_price = 0
    amount_to_return = return_trade_size
    purchase_trades = []
    for trade in self.trades:
      if trade["symbol"] == asset_symbol and trade["type"] == "buy":
        if trade["amount_returned"] != trade["amount"]:
          amount_returned = min(amount_to_return, trade["amount"] - trade["amount_returned"])
          trade["amount_returned"] += amount_returned
          amount_to_return -= amount_returned
          asset_sum_price += trade["total_price"] * (amount_returned / trade["amount"])
          purchase_trades.append(trade)

          # Check return amount is less than some small value.
          # With Python imprecision there will be issues sometimes.
          if amount_to_return <= 0.001:
            return {
              'purchase_trades': purchase_trades,
              'avg_purchase_price': asset_sum_price / return_trade_size,
              'total_purchase_price': asset_sum_price
            }
    
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

  def sell(self, asset_symbol, amount):
    if amount <= 0:
      print(f"[SELL-{asset_symbol}] Amount must be greater than zero!")
      return

    asset_price = self.all_asset_dfs[asset_symbol].loc[self.current_day]["Close"]
    sale_price = amount * asset_price
    sale_price *= 1 - self.commission_slippage
    
    msg = f"{self.current_day}: {amount}x{asset_symbol} @ ${asset_price}"
    msg += f" | Total: ${sale_price}"
    
    if self.get_available_equity()[asset_symbol] >= amount:
      print(f"Sell {msg}")
      self.available_cash += sale_price
      purchase_info = self.get_asset_purchase_info(
            asset_symbol, amount)
      self.trades.append({
        "type": "sell",
        "day": self.current_day, 
        "symbol": asset_symbol, 
        "amount": amount, 
        "asset_price": asset_price, 
        "total_price": sale_price,
        "purchase_trades": purchase_info["purchase_trades"],
        "avg_purchase_price": purchase_info['avg_purchase_price'],
        "total_purchase_price": purchase_info['total_purchase_price'],
        "entry_day": purchase_info["purchase_trades"][0]["day"],
        "return": sale_price - (purchase_info['avg_purchase_price'] * amount),
        "return_percentage": ((sale_price / (purchase_info['avg_purchase_price'] * amount)) - 1) * 100})
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

    self.create_signals()

  def backtest(self, start_date, end_date, starting_cash, commission_slippage):
    print(colored(figlet_format("Backtest"), "green"))

    self.initial_cash = starting_cash
    self.available_cash = starting_cash
    self.commission_slippage = commission_slippage
    self.trades = []

    days = pd.bdate_range(start=start_date, end=end_date).strftime("%Y-%m-%d")
    for day in days.to_list():
      self.advance_to_day(day)

    # Liquidate all assets to get final metrics
    available_equity = self.get_available_equity()
    for asset_symbol in available_equity:
      if available_equity[asset_symbol] != 0:
        self.sell(asset_symbol, available_equity[asset_symbol])

    # Calculate metrics
    if len(self.trades) == 0:
      print("No trades made!")
      return
      
    trade_sizes = [trade["total_purchase_price"] for trade in self.trades if "return" in trade]
    avg_trade_size = sum(trade_sizes) / len(trade_sizes)
    trade_returns = [trade["return"] for trade in self.trades if "return" in trade]
    avg_trade_return = sum(trade_returns) / len(trade_returns)
    highest_trade_return = max(trade_returns)
    lowest_trade_return = min(trade_returns)
    number_winning_trades = len([t for t in trade_returns if t >= 0])
    number_losing_trades = len([t for t in trade_returns if t < 0])
    probability_of_win = (number_winning_trades + 1) / (number_winning_trades + number_losing_trades + 2)

    trade_return_percentages = [trade["return_percentage"] for trade in self.trades if "return_percentage" in trade]
    avg_trade_return_percentage = sum(trade_return_percentages) / len(trade_return_percentages) 

    n_over_a_returns = get_n_over_a_returns(self.all_asset_dfs, starting_cash, commission_slippage, start_date, end_date)
    n_over_a_return = n_over_a_returns / starting_cash * 100

    sharpe_ratio = 0

    print()
    print(colored(figlet_format("Metrics"), "red"))
    print(f"Period: {start_date} - {end_date} ({len(days)} days)")
    print(f"Starting balance: ${self.initial_cash}")
    print(f"Final balance: ${self.available_cash}")
    print(f"Return [%]: {self.available_cash / self.initial_cash * 100}")
    print(f"Asset Market (C/N) Return: ${n_over_a_returns}")
    print(f"Asset Market (C/N) Return [%]: {n_over_a_return}")
    print(f"Sharpe Ratio: {sharpe_ratio}")
    print(f"Number of Trades: {len(trade_returns)}")
    print(f"Number of Winning Trades: {number_winning_trades}")
    print(f"Number of Losing Trades: {number_losing_trades}")
    print(f"Probability of Win: {probability_of_win}")
    print(f"Average Trade Return: ${avg_trade_return}")
    print(f"Average Trade Size: ${avg_trade_size}")
    print(f"Average Trade Return [%]: {avg_trade_return_percentage}")
    print(f"Highest Trade Return: ${highest_trade_return}")
    print(f"Lowest Trade Return: ${lowest_trade_return}")
    print()
    print(colored(figlet_format("Trades"), "blue"))
    for trade in self.trades:
      if "return_percentage" in trade:
        print(colored(f"{trade['symbol']} | {trade['entry_day']} - {trade['day']}", "blue"))
        print(f"Average Purchase Price: ${trade['avg_purchase_price']}")
        print(f"Total Purchase Price: ${trade['total_purchase_price']}")
        print(f"Total Sale Price: ${trade['total_price']}")
        print(f"Return: ${trade['return']}")
        print(f"Return [%]: {trade['return_percentage']}")
        print("Purchases:")
        for trade_purchase in trade["purchase_trades"]:
          buy_msg = f"  [{trade_purchase['day']}]  "
          buy_msg += f"{trade_purchase['amount']}x{trade['symbol']} @ "
          buy_msg += f"${trade_purchase['asset_price']} for "
          buy_msg += f"${trade_purchase['total_price']}."
          print(buy_msg)
        
        print("\n\n")

    return {
      "return": self.available_cash / self.initial_cash
    }

  # Get any buy/sell signals for present day data
  # TODO: Make existing equity_positions work as intended
  def extrapolate_future_predictions(self, prediction_date, starting_cash, commission_slippage, equity_positions=[]):
    self.initial_cash = starting_cash
    self.available_cash = starting_cash
    self.commission_slippage = commission_slippage
    self.trades = []

    for position in equity_positions:
      self.trades.append({})
    
    # Will print out buy/sell signals
    self.advance_to_day(prediction_date)

  # Goes trade by trade and prints a plot of the asset with a number of column
  # values to graph alongside for analysis
  def show_trade_plots(self, to_graph):
    asset_dfs_to_plot = dict()
    for trade in self.trades:
      if "return" in trade:
        asset_dfs_to_plot[trade['symbol']] = self.all_asset_dfs[trade['symbol']]

    plot_asset_dfs(asset_dfs_to_plot, to_graph=to_graph)

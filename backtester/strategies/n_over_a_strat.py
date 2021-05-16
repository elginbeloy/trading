from strategy import Strategy

class NOverAStrategy(Strategy):
  def backtest_init(self):
    self.total_assets = len(self.all_asset_dfs.keys())
    if self.total_assets > 0:
      self.amount_to_invest_per_symbol = self.initial_cash / (self.total_assets * (1 + self.commission_slippage))
      print(self.total_assets)
      print(self.amount_to_invest_per_symbol)

  def create_signals(self):
    if self.amount_to_invest_per_symbol:
      for symbol in self.asset_dfs.keys():
        if self.get_available_equity()[symbol] == 0:
          last_close_price = self.asset_dfs[symbol]["Close"].iloc[-1]
          amount_to_buy = self.amount_to_invest_per_symbol / last_close_price
          self.buy(symbol, amount_to_buy)
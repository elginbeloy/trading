from strategy import Strategy

# Risk 5% of capital per trade by default (weighted by probability)
DEFAULT_RISK_PER_TRADE = 0.05

class NOverAStrategy(Strategy):
  def create_signals(self):
    total_assets = len(self.all_asset_dfs)
    if total_assets > 0:
      amount_to_invest_per_symbol = self.initial_cash / (total_assets * (1 + self.commission_slippage))

      for symbol in self.asset_dfs.keys():
        if self.get_available_equity()[symbol] == 0:
          first_close_price = self.asset_dfs[symbol]["Close"].iloc[-1]
          amount_to_buy = amount_to_invest_per_symbol / (first_close_price + (0.001))
          self.buy(symbol, amount_to_buy)
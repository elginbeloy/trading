from strategy import Strategy
from utils import has_n_days_data

class TrendStrat(Strategy):
  def next(self):
    for symbol in self.asset_dfs.keys():
      if has_n_days_data(self.asset_dfs[symbol], self.current_day, 51):
        close_prices = self.asset_dfs[symbol]["Close"].to_list()

        if close_prices[-1] > close_prices[-2]:
          if close_prices[-2] > close_prices[-3]:
            if close_prices[-3] > close_prices[-25] * 1.1:
              if close_prices[-25] > close_prices[-50] * 1.1:
                self.buy(symbol, 1)
        elif close_prices[-2] > close_prices[-1] * 1.1 and self.get_available_equity()[symbol]:
          self.sell(symbol, self.get_available_equity()[symbol])
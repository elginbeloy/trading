from ta.trend import SMAIndicator
from strategy import Strategy
from utils import has_n_days_data

# Risk 5% of capital per trade by default (weighted by probability)
DEFAULT_RISK_PER_TRADE = 0.05

# Only ever risk 50% of capital to prevent wipe-outs
# TODO: make a check for this
MAX_PERCENT_CAPITAL_AT_RISK = 0.5

class MATrends(Strategy):
  def init(self):
    self.add_column_to_all_assets("SMA_10", ["Close"], lambda c: SMAIndicator(c, window=10).sma_indicator())
    self.add_column_to_all_assets("SMA_50", ["Close"], lambda c: SMAIndicator(c, window=50).sma_indicator())
    self.add_column_to_all_assets("SMA_200", ["Close"], lambda c: SMAIndicator(c, window=200).sma_indicator())

  def create_signals(self):
    typical_bet_size = self.available_cash * DEFAULT_RISK_PER_TRADE

    for symbol in self.asset_dfs.keys():
      if has_n_days_data(self.asset_dfs[symbol], self.current_day, 201):
        close_price = self.asset_dfs[symbol]["Close"].iloc[-1]
        sma_10_price = self.asset_dfs[symbol]["SMA_10"].iloc[-1]
        sma_50_price = self.asset_dfs[symbol]["SMA_50"].iloc[-1]
        sma_200_price = self.asset_dfs[symbol]["SMA_200"].iloc[-1]

        if close_price > sma_10_price * 1.05:
          if sma_10_price > sma_50_price * 1.1:
            if sma_50_price > sma_200_price * 1.15:
              if self.get_available_equity()[symbol] == 0:
                amount_to_buy = round(close_price / typical_bet_size * (1 + ((close_price - sma_200_price) / sma_200_price)))
                if amount_to_buy > 1:
                  self.buy(symbol, amount_to_buy)
        elif self.get_available_equity()[symbol]:
          self.sell(symbol, self.get_available_equity()[symbol])
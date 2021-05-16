from ta.trend import SMAIndicator
from strategy import Strategy
from utils import has_n_days_data

# Risk 5% of capital per trade by default (weighted by probability)
DEFAULT_RISK_PER_TRADE = 0.05

class GavsStrat(Strategy):
  def init(self):
    self.add_column_to_all_assets("SMA_10", ["Close"], lambda c: SMAIndicator(c, window=10).sma_indicator())
    self.add_column_to_all_assets("SMA_20", ["Close"], lambda c: SMAIndicator(c, window=10).sma_indicator())
    self.add_column_to_all_assets("SMA_50", ["Close"], lambda c: SMAIndicator(c, window=50).sma_indicator())

  def create_signals(self):
    typical_bet_size = self.available_cash * DEFAULT_RISK_PER_TRADE

    for symbol in self.asset_dfs.keys():
      if has_n_days_data(self.asset_dfs[symbol], self.current_day, 51):
        close_price = self.asset_dfs[symbol]["Close"].iloc[-1]
        sma_10_price = self.asset_dfs[symbol]["SMA_10"].iloc[-1]
        sma_20_price = self.asset_dfs[symbol]["SMA_20"].iloc[-1]
        sma_50_price = self.asset_dfs[symbol]["SMA_50"].iloc[-1]

        # Entry Signals

        if close_price > sma_10_price * 1.1:
          # MFI is not already overbought
          if sma_10_price > sma_50_price * 1.1:
            amount_to_buy = close_price / typical_bet_size
            if amount_to_buy > 0.1:
              self.buy(symbol, amount_to_buy)

        # Exit Signals

        # MFI indicates we're leaving overbought territory
        if sma_20_price > sma_10_price:
          if self.get_available_equity()[symbol]:
            self.sell(symbol, self.get_available_equity()[symbol])
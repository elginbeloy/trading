from ta.trend import SMAIndicator
from ta.volume import MFIIndicator, money_flow_index
from strategy import Strategy
from utils import has_n_days_data

# Risk 5% of capital per trade by default (weighted by probability)
DEFAULT_RISK_PER_TRADE = 0.05

class TrendMFIStrat(Strategy):
  def init(self):
    self.add_column_to_all_assets("SMA_10", ["Close"], lambda c: SMAIndicator(c, window=10).sma_indicator())
    self.add_column_to_all_assets("SMA_20", ["Close"], lambda c: SMAIndicator(c, window=20).sma_indicator())
    self.add_column_to_all_assets("SMA_50", ["Close"], lambda c: SMAIndicator(c, window=50).sma_indicator())
    self.add_column_to_all_assets("SMA_200", ["Close"], lambda c: SMAIndicator(c, window=200).sma_indicator())
    self.add_column_to_all_assets("MFI", ["High", "Low", "Close", "Volume"], lambda c1, c2, c3, c4: MFIIndicator(c1, c2, c3, c4).money_flow_index())

  def create_signals(self):
    typical_bet_size = self.available_cash * DEFAULT_RISK_PER_TRADE

    for symbol in self.asset_dfs.keys():
      if has_n_days_data(self.asset_dfs[symbol], self.current_day, 201):
        close_prices = self.asset_dfs[symbol]["Close"].to_list()
        sma_10_price = self.asset_dfs[symbol]["SMA_10"].iloc[-1]
        sma_20_price = self.asset_dfs[symbol]["SMA_20"].iloc[-1]
        sma_50_price = self.asset_dfs[symbol]["SMA_50"].iloc[-1]
        sma_200_price = self.asset_dfs[symbol]["SMA_200"].iloc[-1]
        mfi_arr = self.asset_dfs[symbol]["MFI"].to_list()

        # Entry Signals

        # Close price was higher than the day before
        if close_prices[-1] > close_prices[-2]:
          # MFI is not already overbought
          if mfi_arr[-1] < 60:
            # Short term trend is positive
            if sma_10_price > sma_20_price:
              # Medium term trend is positive beyond a trend threshold
              if sma_20_price > sma_50_price * 1.1:
                # Long term trend is positive beyond a trend threshold
                if sma_50_price > sma_200_price * 1.1:
                  amount_to_buy = close_prices[-1] / typical_bet_size
                  if amount_to_buy > 0.1:
                    self.buy(symbol, amount_to_buy)

        # Exit Signals

        # MFI indicates we're leaving overbought territory
        if any([v > 80 for v in mfi_arr[-3:]]) and mfi_arr[-1] < 80:
          if self.get_available_equity()[symbol]:
            self.sell(symbol, self.get_available_equity()[symbol])
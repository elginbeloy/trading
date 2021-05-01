from ta.trend import MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator
from strategy import Strategy
from utils import has_n_days_data

class ManualRulesStrat(Strategy):
  def init(self):
    self.add_column_to_all_assets("ADX", ["High", "Low", "Close"], lambda c1, c2, c3: ADXIndicator(c1, c2, c3).adx())
    self.add_column_to_all_assets("MACD", ["Close"], lambda c: MACD(c).macd())
    self.add_column_to_all_assets("MACD_SIG", ["Close"], lambda c: MACD(c).macd_signal())
    self.add_column_to_all_assets("MACD_DIFF", ["Close"], lambda c: MACD(c).macd_diff())
    self.add_column_to_all_assets("RSI", ["Close"], lambda c: RSIIndicator(c).rsi())
    self.add_column_to_all_assets("MFI", ["High", "Low", "Close", "Volume"], lambda c1, c2, c3, c4: MFIIndicator(c1, c2, c3, c4).money_flow_index())

  def create_signals(self):
    for symbol in self.asset_dfs.keys():
      if has_n_days_data(self.asset_dfs[symbol], self.current_day, 100):
        asset_price = self.asset_dfs[symbol]["Close"].to_list()[-1]
        macd_diff_arr = self.asset_dfs[symbol]["MACD_DIFF"].to_list()
        adx = self.asset_dfs[symbol]["ADX"].to_list()[-1]
        rsi_arr = self.asset_dfs[symbol]["RSI"].to_list()
        mfi_arr = self.asset_dfs[symbol]["MFI"].to_list()

        if adx > 0.3:
          if macd_diff_arr[-1] > 0.2:
            if rsi_arr[-1] > rsi_arr[-3] + 5 and mfi_arr[-1] > mfi_arr[-3] + 5:
              if self.get_available_equity()[symbol] == 0:
                amount_to_purchase = self.available_cash * 0.05 / asset_price
                self.buy(symbol, amount_to_purchase)
          elif macd_diff_arr[-1] < 0 and self.get_available_equity()[symbol] > 0:
            self.sell(symbol, self.get_available_equity()[symbol])
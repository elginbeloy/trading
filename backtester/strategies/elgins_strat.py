'''
First Rules Based Approach

Find a high probability trade, decide exit and stop, risk capital in an amount
proportional to the stop-loss risk. Pyramid invest as more validation points 
are added to corroborate our theory. 

Entry Ideas:

[0] Trade w/ The Major Trend
[0.0] Trend detection 
  [0] Higher highs
  [1] Lower lows

[1] Buy In Retracements
[1.0] Retracement and wave detection
  [0] Average wave length indicator

[2] Avoid Highly Volatile Assets To Reduce Risk
[2.0] Volatility prediction and monitoring
  [0] Volatile events like earnings, etc...
  [1] News and article count monitoring
  [2] Live trade-imbalance monitoring

[3] Confirm Hypothesis with Volume
[3.0] Volume trend confirmation strategies

Exit Ideas:

[4]

Stop / Risk Measurement Ideas:

[5] Using Technical Analysis
[5.0] Support Levels or Ex Resistance Levels
  [0] Amount you risk * probability stop sale occurs 
  [1] Other indicators to exit, such as MA crossover, STOCH, or MACD
whichever is fastest and gives high probability (low estimator variance)
[5.1] Using Trade Development
  [0] How much has the trade lost? Is it beyond our expected loss by this point
  given the Average True Range of the asset?
  [1] How are other correlated assets doing? Is this unusual behavior?

Testing Results:

[0]

Optimization Results:

[0]

Final Rules:

[0]

Final Results:


'''

from ta.trend import MACD, ADXIndicator, SMAIndicator
from ta.volume import MFIIndicator
from ta.volatility import AverageTrueRange
from strategy import Strategy
from utils import has_n_days_data

# Only ever risk 50% of capital to prevent wipe-outs
PERCENT_CAPITAL_AT_RISK = 0.5

# Only risk 10% of at-risk-capital per trade to prevent wipe outs
MAX_AT_RISK_CAPITAL_PER_TRADE = 0.1

class ElginsStrat(Strategy):
  def init(self):
    self.add_column_to_all_assets("SMA_10", ["Close"], lambda c: SMAIndicator(c, window=10).sma_indicator())
    self.add_column_to_all_assets("SMA_30", ["Close"], lambda c: SMAIndicator(c, window=30).sma_indicator())
    self.add_column_to_all_assets("SMA_50", ["Close"], lambda c: SMAIndicator(c, window=50).sma_indicator())
    self.add_column_to_all_assets("SMA_100", ["Close"], lambda c: SMAIndicator(c, window=100).sma_indicator())
    self.add_column_to_all_assets("AVG_T_RNG", ["High", "Low", "Close"], lambda c1, c2, c3: AverageTrueRange(c1, c2, c3).average_true_range())
    self.add_column_to_all_assets("AVG_T_RNG_SMA_50", ["AVG_T_RNG"], lambda c: SMAIndicator(c, window=50).sma_indicator())
    self.add_column_to_all_assets("ADX", ["High", "Low", "Close"], lambda c1, c2, c3: ADXIndicator(c1, c2, c3).adx())
    self.add_column_to_all_assets("MACD_DIFF", ["Close"], lambda c: MACD(c).macd_diff())
    self.add_column_to_all_assets("MFI", ["High", "Low", "Close", "Volume"], lambda c1, c2, c3, c4: MFIIndicator(c1, c2, c3, c4).money_flow_index())

  def create_signals(self):
    for symbol in self.asset_dfs.keys():
      if has_n_days_data(self.asset_dfs[symbol], self.current_day, 200):
        asset_price = self.asset_dfs[symbol]["Close"].iloc[-1]
        macd_diff_arr = self.asset_dfs[symbol]["MACD_DIFF"].to_list()
        adx = self.asset_dfs[symbol]["ADX"].iloc[-1]
        mfi_arr = self.asset_dfs[symbol]["MFI"].to_list()
        sma_10 = self.asset_dfs[symbol]["SMA_10"].iloc[-1]
        sma_30 = self.asset_dfs[symbol]["SMA_30"].iloc[-1]
        sma_50 = self.asset_dfs[symbol]["SMA_50"].iloc[-1]
        sma_100 = self.asset_dfs[symbol]["SMA_100"].iloc[-1]
        atr = self.asset_dfs[symbol]["AVG_T_RNG"].iloc[-1]
        atr_sma_50_arr = self.asset_dfs[symbol]["AVG_T_RNG_SMA_50"].iloc[-1]

        # If the current ATR is twice is large as the 50-day MA of the ATR
        # leave to avoid intense volatility, and thus likely unpredictability
        if atr > atr_sma_50_arr * 2:
          if self.get_available_equity()[symbol] > 0:
            self.sell(symbol, self.get_available_equity()[symbol])

          break 

        if adx > 0.3:
          if sma_10 > sma_30 and sma_30 > sma_50 and sma_50 > sma_100:
            if macd_diff_arr[-1] > macd_diff_arr[-2] and macd_diff_arr[-2] > macd_diff_arr[-3]:
              if self.get_available_equity()[symbol] == 0:
                amount_to_purchase = self.available_cash * PERCENT_CAPITAL_TO_RISK / asset_price
                self.buy(symbol, amount_to_purchase)
            elif macd_diff_arr[-1] < 0 and self.get_available_equity()[symbol] > 0:
              self.sell(symbol, self.get_available_equity()[symbol])
          elif sma_10 < sma_30 and self.get_available_equity()[symbol] > 0:
            self.sell(symbol, self.get_available_equity()[symbol])
        else:
          if mfi_arr[-1] < 20:
            if mfi_arr[-1] < 70 or mfi_arr[-1] > 10:
              if self.get_available_equity()[symbol] == 0:
                amount_to_purchase = self.available_cash * PERCENT_CAPITAL_TO_RISK / asset_price
                self.buy(symbol, amount_to_purchase)
            elif self.get_available_equity()[symbol] > 0:
              self.sell(symbol, self.get_available_equity()[symbol])

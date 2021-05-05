from get_ohlcv_data import load_asset_dfs
from strategies.macd_strat_1 import MACDStratOne

TEST_START_DATE = '2019-01-01'
TEST_END_DATE = '2021-04-18'

INITIAL_CASH=10000
COMMISSION_AND_SLIPPAGE = 0.01

asset_dfs = load_asset_dfs()
strategy = MACDStratOne(asset_dfs)
strategy.backtest(TEST_START_DATE, TEST_END_DATE, INITIAL_CASH, COMMISSION_AND_SLIPPAGE)
strategy.show_trade_plots([["Close"], ["MFI"], ["Close", "SMA_10", "SMA_50", "SMA_200"], ["MACD", "MACD_SIG"]])
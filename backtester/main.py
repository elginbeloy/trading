from get_ohlcv_data import load_asset_dfs
from strategies.gavs_strat import GavsStrat

TEST_START_DATE = '2019-01-01'
TEST_END_DATE = '2020-01-01'

INITIAL_CASH=10000
COMMISSION_AND_SLIPPAGE = 0.01

asset_dfs = load_asset_dfs()
strategy = GavsStrat(asset_dfs)
strategy.backtest(TEST_START_DATE, TEST_END_DATE, INITIAL_CASH, COMMISSION_AND_SLIPPAGE)
strategy.show_trade_plots([["Close"], ["Close", "SMA_10", "SMA_20", "SMA_50"]])
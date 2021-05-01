from get_ohlcv_data import load_asset_dfs
from strategies.n_over_a_strat import NOverAStrategy

TEST_START_DATE = '2016-01-01'
TEST_END_DATE = ' 2021-01-01'

INITIAL_CASH=10000
COMMISSION_AND_SLIPPAGE = 0.01

def test_backtest_strategy():
  asset_dfs = load_asset_dfs()
  strategy = NOverAStrategy(asset_dfs)
  strategy.backtest(TEST_START_DATE, TEST_END_DATE, INITIAL_CASH, COMMISSION_AND_SLIPPAGE)
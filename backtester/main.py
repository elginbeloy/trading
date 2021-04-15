from get_ohlcv_data import get_time_interval_bars
from strategies.trend_strat import TrendStrat

COMMISSION_AND_SLIPPAGE = 0.01
INITIAL_CASH=10000
ASSETS_TO_TEST = ['AAPL', 'GOOG', 'AMC', 'LYFT', 'ZM', 'BABA']
TEST_START_DATE = '2016-01-01'
TEST_END_DATE = '2020-01-01'
PREDICTION_START_DATE = '2020-01-01'
PREDICTION_END_DATE = '2021-04-14'

asset_dfs = dict()
for symbol in ASSETS_TO_TEST:
  asset_dfs[symbol] = get_time_interval_bars(symbol, 'day', '1', TEST_START_DATE, TEST_END_DATE)

strategy = TrendStrat(asset_dfs, INITIAL_CASH, COMMISSION_AND_SLIPPAGE)
strategy.backtest(TEST_START_DATE, TEST_END_DATE)

asset_dfs = dict()
for symbol in ASSETS_TO_TEST:
  asset_dfs[symbol] = get_time_interval_bars(symbol, 'day', '1', PREDICTION_START_DATE, PREDICTION_END_DATE)

strategy.extrapolate_future_predictions(4000, [], PREDICTION_END_DATE, asset_dfs)
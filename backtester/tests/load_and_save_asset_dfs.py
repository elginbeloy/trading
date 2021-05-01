from get_ohlcv_data import get_time_interval_bars, save_asset_dfs, load_asset_dfs
from symbols import test_asset_list

TEST_START_DATE = '2020-01-01'
TEST_END_DATE = ' 2021-01-01'

def test_load_and_save_assets():
  asset_dfs = dict()
  for symbol in test_asset_list:
    asset_dfs[symbol] = get_time_interval_bars(symbol, 'day', '1', TEST_START_DATE, TEST_END_DATE)

  reference_asset_dfs = asset_dfs
  save_asset_dfs(asset_dfs, TEST_START_DATE, TEST_END_DATE)

  asset_dfs = None
  asset_dfs = load_asset_dfs()

  assert(reference_asset_dfs == asset_dfs)
  print("[load_and_save_asset_dfs.py]: Tests pass!")
from ta.trend import MACD
from ta.volume import MFIIndicator
from get_ohlcv_data import load_asset_dfs
from utils import plot_asset_dfs, add_column_to_asset_dfs

asset_dfs = load_asset_dfs()
add_column_to_asset_dfs(asset_dfs, "MFI", ["High", "Low", "Close", "Volume"],
  lambda c1, c2, c3, c4: MFIIndicator(c1, c2, c3, c4).money_flow_index())
add_column_to_asset_dfs(asset_dfs, "MACD", ["Close"], 
  lambda c1: MACD(c1).macd())
add_column_to_asset_dfs(asset_dfs, "MACD_SIG", ["Close"], 
  lambda c1: MACD(c1).macd_signal())
plot_asset_dfs(asset_dfs, to_graph=[["Close", "Open", "High", "Low"], ["MFI"], ["MACD", "MACD_SIG"]])
# https://scikit-learn.org/stable/modules/tree.html

from sklearn import tree
from get_ohlcv_data import get_time_interval_bars
from ta.trend import MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volume import MFIIndicator

ASSETS_TO_TEST = ['AAPL', 'GOOG', 'AMC', 'LYFT', 'ZM', 'BABA', 'AMZN', 'DVAX', 'MSFT', 'PYPL', 'TWTR', 'FB', 'SNAP', 'TRVG', 'BL', 'KLAC', 'TTWO', 'PYPL', 'PSEC', 'SLAB', 'NFLX', 'IMGN', 'CLOU', 'GFF']
TRAIN_START_DATE = '2014-01-01'
TRAIN_END_DATE = '2020-01-1'

X = []
Y = []

for symbol in ASSETS_TO_TEST:
  data_ohlcv = get_time_interval_bars(symbol, 'day', '1', TRAIN_START_DATE, TRAIN_END_DATE)
  data_ohlcv["MFI"] = MFIIndicator(data_ohlcv["High"], data_ohlcv["Low"], 
    data_ohlcv["Close"], data_ohlcv["Volume"]).money_flow_index()
  data_ohlcv["MACD"] = MACD(data_ohlcv["Close"]).macd()
  data_ohlcv["MACD_SIG"] = MACD(data_ohlcv["Close"]).macd_signal()
  data_ohlcv["MACD_DIF"] = MACD(data_ohlcv["Close"]).macd_diff()

  sample = []
  sample_label = []
  for day in data_ohlcv.index:
    data_ohlcv.loc[day]

    X.append(sample)
    Y.append(sample_label)

model = tree.DecisionTreeClassifier()
model = model.fit(X, Y)
tree.plot_tree(model)

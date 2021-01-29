import keras
import yfinance as yf 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.ticker import ScalarFormatter
from util import append_ticker_to_x_y

# Required by pandas: registering matplotlib date converters
pd.plotting.register_matplotlib_converters()

# Define the lookback period (days), target appreciation percentage, and
# growth maximum timeline (days).
lookback_period = 30
p = 5
n = 4
plot = False

training_tickers = ['AAPL','UBER','LYFT','AMD','GOOG','ZM','FB','MSFT','DVAX','TSLA','PLTR','NVDA','ATVI','AMZN','PYPL','TWTR','WMT','BBY','DIS','NKE','XEL','MRNA','ETSY','EXPE','T','GOOGL','EBAY','CHTR','NFLX','QCOM','HLT','ADBE','PTON','FIT','ABNB','SNE','PLUG','AZN','SNAP']
training_tickers = [yf.Ticker(symbol) for symbol in training_tickers]
training_tickers = [ticker for ticker in training_tickers if ticker.info['lastDividendValue'] == None]

evaluation_tickers = ['GPRO','VOO','INO']
evaluation_tickers = [yf.Ticker(symbol) for symbol in evaluation_tickers]
evaluation_tickers = [ticker for ticker in evaluation_tickers if ticker.info['lastDividendValue'] == None]

x = []
y = []

print('NOverP')
print('Grabbing data + calculating indicators for each stock...')
for ticker in training_tickers:
  append_ticker_to_x_y(ticker, x, y, lookback_period=lookback_period, n=n, p=p, plot=plot)

x = np.array(x)
y = np.array(y)

print(x.shape)
print(y.shape)
print(y.sum())

model = keras.Sequential()
model.add(keras.layers.LSTM(128, input_shape=(x.shape[1], x.shape[2])))
model.add(keras.layers.Dropout(0.5))
model.add(keras.layers.Dense(1, activation='sigmoid'))
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])
model.fit(x, y, epochs=100)

# Reset x, y and evaluate the trained model on the evaluation tickers
x = []
y = []

print('Grabbing data + calculating indicators for each stock...')
for ticker in evaluation_tickers:
  append_ticker_to_x_y(ticker, x, y, lookback_period=lookback_period, n=n, p=p, plot=False)

x = np.array(x)
y = np.array(y)

print(x.shape)
print(y.shape)
print(y.sum())

print('Evaluating...')

_, accuracy = model.evaluate(x, y)
print(f'Accuracy: {accuracy * 100}')
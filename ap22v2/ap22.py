import keras
import datetime as dt
import numpy as np
from get_symbols import get_symbols
from get_trade_data import get_trades
from form_bars import get_bars_from_trades
from get_training_data import get_training_data
from sklearn.metrics import classification_report, confusion_matrix

# Data and model behavior params
desired_bars_per_day = 10
lookback_bar_amount = 200
target_appreciation_percentage = 1.0
max_depreciation_percentage = 3.0
max_holding_period_bars = 50
max_class_imbalance_percentage = 0.7

# Model training params
batch_size = 64
epoch_amount = 50

symbols = get_symbols()[0:80]
training_symbols = symbols[:-10]
evaluation_symbols = symbols[-10:]

training_start_date = dt.datetime(2018, 1, 1)
training_end_date = dt.datetime(2020, 1, 1)

evaluation_start_date = dt.datetime(2020, 1, 1)
evaluation_end_date = dt.datetime(2021, 1, 1)


for symbol in symbols:
  trades

symbol_trades, symbol_expected_dollars_per_bar = get_trades(
  training_symbols, 
  training_start_date, 
  training_end_date,
  desired_bars_per_day)

training_symbol_bars = get_bars_from_trades(
  symbol_trades, 
  symbol_expected_dollars_per_bar)

symbol_trades, symbol_expected_dollars_per_bar = get_trades(
  evaluation_symbols, 
  evaluation_start_date, 
  evaluation_end_date,
  desired_bars_per_day)

evaluation_symbol_bars = get_bars_from_trades(
  symbol_trades, 
  symbol_expected_dollars_per_bar)

# Print out the created bars
print('Training Bars:')
for symbol in training_symbol_bars:
  print(symbol)
  print(training_symbol_bars[symbol].head(30))
  print("\n\n")

print('Evaluation Bars:')
for symbol in training_symbol_bars:
  print(symbol)
  print(training_symbol_bars[symbol].head(30))
  print("\n\n")

train_x, train_y = get_training_data(
  training_symbol_bars,
  lookback_bar_amount=lookback_bar_amount,
  target_appreciation_percentage=target_appreciation_percentage, 
  max_depreciation_percentage=max_depreciation_percentage,
  max_holding_period_bars=max_holding_period_bars)

eval_x, eval_y = get_training_data(
  evaluation_symbol_bars,
  lookback_bar_amount=lookback_bar_amount,
  target_appreciation_percentage=target_appreciation_percentage, 
  max_depreciation_percentage=max_depreciation_percentage,
  max_holding_period_bars=max_holding_period_bars)


print(f"T-X shape: {train_x.shape} | T-Y shape: {train_y.shape}")
print(f"E-X shape: {eval_x.shape} | E-Y shape: {eval_y.shape}")


print("Starting training...")
model = keras.Sequential()
model.add(keras.layers.recurrent.LSTM(12, return_sequences=True, input_shape=(train_x.shape[1], train_x.shape[2])))
model.add(keras.layers.recurrent.LSTM(12))
model.add(keras.layers.core.Dense(1, activation='sigmoid'))
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])
model.fit(train_x, train_y, epochs=epoch_amount, batch_size=batch_size, validation_data=(eval_x, eval_y))

results = model.evaluate(eval_x, eval_y, batch_size=batch_size)
print("Eval loss, acc:", results)

eval_y_pred = model.predict(eval_x, batch_size=batch_size)
eval_y_pred = np.argmax(eval_y_pred, axis=1)
target_names = ['Appreciated', 'Did Not Appreciate']

print('Confusion Matrix (tn, fp, fn, tp):')
print(confusion_matrix(eval_y, eval_y_pred).ravel())
print()
print('Classification Report')
print(classification_report(eval_y, eval_y_pred, target_names=target_names))

model.save('model.h5')
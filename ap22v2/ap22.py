import keras
import datetime as dt
import numpy as np
from get_symbols import ROBINHOOD_COLLECTION_SYMBOLS
from get_aggregate_bars import get_time_interval_bars
from get_x_y import get_model_data
from util import log_to_file
from sklearn.metrics import classification_report, confusion_matrix

training_symbols = ROBINHOOD_COLLECTION_SYMBOLS[:800]
training_symbol_bars = get_time_interval_bars(
  training_symbols, 30, "minute", "2018-01-01", "2020-01-01")

eval_symbols = ROBINHOOD_COLLECTION_SYMBOLS[800:]
eval_symbol_bars = get_time_interval_bars(
  eval_symbols, 30, "minute", "2020-01-01", "2021-01-01")

# Data Labeling HyperParams
lookback_bars = 200
max_holding_period_bars = 2
target_appreciation_percentage = 0.3
max_depreciation_percentage = 1.0
max_class_imbalance_percentage = 55 # Used for undersampling

train_x, train_y = get_model_data(
  training_symbol_bars, 
  lookback_bars, 
  max_holding_period_bars, 
  target_appreciation_percentage, 
  max_depreciation_percentage,
  max_class_imbalance_percentage)
eval_x, eval_y = get_model_data(
  eval_symbol_bars, 
  lookback_bars, 
  max_holding_period_bars, 
  target_appreciation_percentage, 
  max_depreciation_percentage,
  max_class_imbalance_percentage)

log_to_file(f"T-X shape: {train_x.shape} | T-Y shape: {train_y.shape}")
log_to_file(f"T-1s {sum(train_y)} | T-0s {len(train_y) - sum(train_y)}")
log_to_file(f"E-X shape: {eval_x.shape} | E-Y shape: {eval_y.shape}")
log_to_file(f"T-1s {sum(eval_y)} | T-0s {len(eval_y) - sum(eval_y)}")


# Model HyperParams
batch_size = 128
epoch_amount = 100

print("Starting training...")
model = keras.Sequential()
model.add(keras.layers.recurrent.LSTM(14, return_sequences=True, input_shape=(train_x.shape[1], train_x.shape[2])))
model.add(keras.layers.recurrent.LSTM(14))
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
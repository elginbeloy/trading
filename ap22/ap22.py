import numpy as np
from get_symbols import ROBINHOOD_COLLECTION_SYMBOLS
from get_aggregate_bars import get_time_interval_bars
from get_model_data import get_model_data
from util import log_to_file
from model import get_model
from sklearn.metrics import classification_report, confusion_matrix

training_symbols = ROBINHOOD_COLLECTION_SYMBOLS[:10]
training_symbol_bars = get_time_interval_bars(
  training_symbols, 30, "minute", "2017-01-01", "2020-01-01")

eval_symbols = ROBINHOOD_COLLECTION_SYMBOLS[10:20]
eval_symbol_bars = get_time_interval_bars(
  eval_symbols, 30, "minute", "2020-01-01", "2021-01-01")

# Hyperparameters for data labeling
lookback_bars = 200
max_holding_period_bars = 2
target_appreciation_percentage = 0.3
max_depreciation_percentage = 1.0
# Used for undersampling the majority class (TODO: Do this w/out losing data?)
max_class_imbalance_percentage = 55

model_training_data = get_model_data(
  training_symbol_bars, 
  lookback_bars, 
  max_holding_period_bars, 
  target_appreciation_percentage, 
  max_depreciation_percentage,
  max_class_imbalance_percentage)
model_eval_data = get_model_data(
  eval_symbol_bars, 
  lookback_bars, 
  max_holding_period_bars, 
  target_appreciation_percentage, 
  max_depreciation_percentage,
  max_class_imbalance_percentage)

log_to_file(f"Model Training Data Shapes:")
log_to_file(model_training_data['bar_values_arr'].shape)
log_to_file(model_training_data['minute_of_day_arr'].shape)
log_to_file(model_training_data['day_of_week_arr'].shape)
log_to_file(model_training_data['day_of_year_arr'].shape)
log_to_file(model_training_data['labels_arr'].shape)

# Model HyperParams
batch_size = 128
epoch_amount = 1000

# Train the model
print("Starting training...")
model = get_model(lookback_bars)
model.fit(
  [
    model_training_data['bar_values_arr'],
    model_training_data['minute_of_day_arr'],
    model_training_data['day_of_week_arr'],
    model_training_data['day_of_year_arr'],
  ], 
  model_training_data['labels_arr'], 
  epochs=epoch_amount, 
  batch_size=batch_size, 
  validation_data=([
    model_eval_data['bar_values_arr'],
    model_eval_data['minute_of_day_arr'],
    model_eval_data['day_of_week_arr'],
    model_eval_data['day_of_year_arr'],
  ], 
  model_eval_data['labels_arr'])
)

# Evaluate the trained model
results = model.evaluate(
  [
    model_eval_data['bar_values_arr'],
    model_eval_data['minute_of_day_arr'],
    model_eval_data['day_of_week_arr'],
    model_eval_data['day_of_year_arr'],
  ], 
  model_eval_data['labels_arr'], 
  batch_size=batch_size
)
print("Eval loss, acc:", results)

# Get evaluation predictions and generate report
eval_predictions = model.predict(
  [
    model_eval_data['bar_values_arr'],
    model_eval_data['minute_of_day_arr'],
    model_eval_data['day_of_week_arr'],
    model_eval_data['day_of_year_arr'],
  ], 
  batch_size=batch_size
)
eval_predictions = np.argmax(eval_predictions, axis=1)
eval_confusion_matrix = confusion_matrix(
  model_eval_data['labels_arr'], eval_predictions)
target_names = ['Appreciated', 'Did Not Appreciate']
classification_report(
  model_eval_data['labels_arr'], 
  eval_predictions, 
  target_names=target_names
)

print('Confusion Matrix (tn, fp, fn, tp):')
print(eval_confusion_matrix.ravel())
print()
print('Classification Report')
print(classification_report)

# Save the final model
model.save('model.h5')

# TODO: Predict asset appreciation likelihood using current date 
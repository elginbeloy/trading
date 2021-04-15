from get_symbols import ROBINHOOD_COLLECTION_SYMBOLS
from get_aggregate_bars import get_tick_interval_bars
from get_model_data import get_model_data
from util import log_to_file
from model import train_and_eval_model
import skopt
from get_trade_data import download_trade_data

# Define list of training and eval symbols
training_symbols = ROBINHOOD_COLLECTION_SYMBOLS[:800]
eval_symbols = ROBINHOOD_COLLECTION_SYMBOLS[800:]

# Define training and eval start and end dates
train_start_date = "2016-01-01"
train_end_date = "2020-01-05"
eval_start_date = train_end_date
eval_end_date = "2021-02-07"

# Download trade data locally for use later
download_trade_data(training_symbols, start_date="2016-01-01",
  end_date="2020-01-01", data_dir="./trade_data")
download_trade_data(eval_symbols, start_date="2020-01-01",
  end_date="2021-02-01", data_dir="./eval_trade_data")

tick_training_bars = get_tick_interval_bars(bar_size_ticks=1000)
tick_eval_bars = get_tick_interval_bars(
  bar_size_ticks=1000, data_dir="./eval_trade_data")

# Define parameter search space used for labeling and training
SEARCH_SPACE = [
    skopt.space.Real(0.0001, 0.001, name='learning_rate'),
    skopt.space.Integer(20, 500, name='lookback_bars'),
    skopt.space.Integer(2, 100, name='max_holding_period_bars'),
    skopt.space.Real(0.1, 5.0, name='target_appreciation_percentage'),
    skopt.space.Real(0.1, 10.0, name='max_depreciation_percentage')]

max_class_imbalance_percentage = 55 # For undersampling the majority class

@skopt.utils.use_named_args(SEARCH_SPACE)
def objective(**params):
  log_to_file(f"Testing Iteration With Params: {params}")

  model_training_data = get_model_data(
    tick_training_bars,
    params["lookback_bars"],
    params["max_holding_period_bars"],
    params["target_appreciation_percentage"],
    params["max_depreciation_percentage"],
    max_class_imbalance_percentage)
  model_eval_data = get_model_data(
    tick_eval_bars, 
    params["lookback_bars"],
    params["max_holding_period_bars"],
    params["target_appreciation_percentage"],
    params["max_depreciation_percentage"],
    max_class_imbalance_percentage)

  log_to_file(f"Model Training Data Shapes:")
  log_to_file(model_training_data['bar_values_arr'].shape)
  log_to_file(model_training_data['minute_of_day_arr'].shape)
  log_to_file(model_training_data['day_of_week_arr'].shape)
  log_to_file(model_training_data['day_of_year_arr'].shape)
  log_to_file(model_training_data['labels_arr'].shape)

  # Train, evaluate, and save this model version
  eval_acc = train_and_eval_model(
    "test_model", 
    model_training_data, 
    model_eval_data, 
    params["lookback_bars"],
    learning_rate=params["learning_rate"])

  log_to_file(f"Iteration Achieved {eval_acc} Accuracy.")

  return eval_acc

results = skopt.forest_minimize(objective, SEARCH_SPACE, n_calls=30, n_random_starts=10)
log_to_file("FINAL RESULTS:")
log_to_file(f"Params: {results.x} | Acc: {results.func}")
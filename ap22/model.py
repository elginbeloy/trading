from util import log_to_file
from numpy import argmax
from keras import Model
from keras.optimizers import Adam
from keras.layers import Input, Embedding, Concatenate, LSTM, Dense, Reshape
from sklearn.metrics import classification_report, confusion_matrix


# Return a multi-layer LSTM model based on a sequence_length
def get_model(sequence_length, learning_rate):
  bar_values_input = Input(shape=(sequence_length, 6), name='bar_values_input')
  minute_of_day_input = Input(shape=(sequence_length, 1), name='minute_of_day_input')
  day_of_week_input = Input(shape=(sequence_length, 7), name='day_of_week_input')
  day_of_year_input = Input(shape=(sequence_length, 1), name='day_of_year_input')

  MINUTE_OF_DAY_EMBEDDING_SIZE = 12
  minute_of_day_embedding = Embedding(
      output_dim=MINUTE_OF_DAY_EMBEDDING_SIZE, 
      input_dim=1440, # 1440 possible minutes in a day
      name='minute_of_day_embedding'
  )(minute_of_day_input)

  minute_of_day_embedding_reshape = Reshape(
    (sequence_length, MINUTE_OF_DAY_EMBEDDING_SIZE), 
    name='minute_of_day_embedding_reshape')(minute_of_day_embedding)
  
  DAY_OF_YEAR_EMBEDDING_SIZE = 6
  day_of_year_embedding = Embedding(
      output_dim=DAY_OF_YEAR_EMBEDDING_SIZE, 
      input_dim=365, # 365 possible days in a year
      name='day_of_year_embedding'
  )(day_of_year_input)

  day_of_year_embedding_reshape = Reshape(
    (sequence_length, DAY_OF_YEAR_EMBEDDING_SIZE), 
    name='day_of_year_embedding_reshape')(day_of_year_embedding)

  lstm_merged_input = Concatenate(axis=-1, name='lstm_merged_input')([
    bar_values_input,
    minute_of_day_embedding_reshape,
    day_of_week_input,
    day_of_year_embedding_reshape,
  ])

  lstm_layer_one = LSTM(32, dropout=0.4, return_sequences=True, name='lstm_layer_one')(lstm_merged_input)
  lstm_layer_two = LSTM(32, dropout=0.4, name='lstm_layer_two')(lstm_layer_one)
  prediction = Dense(1, activation='sigmoid', name='prediction')(lstm_layer_two)
  
  model = Model(
    inputs=[
      bar_values_input, 
      minute_of_day_input, 
      day_of_week_input, 
      day_of_year_input
    ], 
    outputs=prediction
  )
  optimizer = Adam(learning_rate=learning_rate)
  model.compile(optimizer, loss="binary_crossentropy", metrics=['accuracy'])

  model.summary(print_fn=log_to_file)

  return model

def train_and_eval_model(model_name, model_training_data, model_eval_data,
  lookback_bars, save_model=False, learning_rate=0.001, epochs=100, 
  batch_size=128):
  # Get and train the model
  model = get_model(lookback_bars, learning_rate)
  model.fit(
    [
      model_training_data['bar_values_arr'],
      model_training_data['minute_of_day_arr'],
      model_training_data['day_of_week_arr'],
      model_training_data['day_of_year_arr'],
    ], 
    model_training_data['labels_arr'], 
    epochs=epochs, 
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
  log_to_file(f"Eval Loss {results[0]}, Eval Acc: {results[1]}")

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
  eval_predictions = argmax(eval_predictions, axis=1)
  eval_confusion_matrix = confusion_matrix(
    model_eval_data['labels_arr'], eval_predictions)
  target_names = ['Appreciated', 'Did Not Appreciate']

  # Log final evaluation results
  log_to_file('Confusion Matrix (tn, fp, fn, tp):')
  log_to_file(eval_confusion_matrix.ravel())
  log_to_file('Classification Report')
  log_to_file(classification_report(
    model_eval_data['labels_arr'], 
    eval_predictions, 
    target_names=target_names
  ))

  if save_model:
    # Save the final model
    model.save(f"{model_name}.h5")

  return results[0]

from keras import Model
from keras.layers import Input, Embedding, Concatenate, LSTM, Dense, Reshape


# Return a multi-layer LSTM model based on the sequence_length.
def get_model(sequence_length):
  bar_values_input = Input(shape=(sequence_length, 7), name='bar_values_input')
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

  lstm_layer_one = LSTM(32, return_sequences=True, name='lstm_layer_one')(lstm_merged_input)
  lstm_layer_two = LSTM(32, name='lstm_layer_two')(lstm_layer_one)
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
  model.compile(optimizer="adam", loss="binary_crossentropy", metrics=['accuracy'])

  print("Model Compiled:")
  model.summary()

  return model
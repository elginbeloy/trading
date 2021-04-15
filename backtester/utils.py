def has_n_days_data(df, start_date, days):
  return len(df.loc[:start_date].index.to_list()) > days
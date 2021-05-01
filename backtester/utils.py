def has_n_days_data(df, start_date, days):
  return len(df.loc[:start_date].index.to_list()) > days

# Returns the "returned" capital in USD (positive or negative) of a simple
# /n asset investment strategy.
def get_n_over_a_returns(asset_dfs, starting_cash, commission_slippage, start_date, end_date):
  total_return = 0
  amount_to_invest_per_symbol = starting_cash / len(asset_dfs.keys())
  for symbol in asset_dfs:
    close_prices = asset_dfs[symbol].loc[start_date:end_date]["Close"].to_list()    
    asset_start_price = close_prices[0]
    asset_end_price = close_prices[-1]

    amount_to_buy = amount_to_invest_per_symbol / (asset_start_price * (1 + commission_slippage))
    total_return += amount_to_buy * asset_end_price

  return total_return
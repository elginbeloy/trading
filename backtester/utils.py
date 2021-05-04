from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt

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

def add_column_to_asset_dfs(asset_dfs, column_name, input_columns, assign_val_func):
  for symbol in asset_dfs.keys():
    input_series = [asset_dfs[symbol][c] for c in input_columns]
    column_val = assign_val_func(*input_series)
    asset_dfs[symbol][column_name] = column_val

def plot_asset_dfs(asset_dfs, to_graph=[["Close"]]):
  for symbol in asset_dfs.keys():
    plot = input(f"Plot {symbol} y/N? :") == "y"
    if plot:
      days = asset_dfs[symbol].index.to_list()
      plt.figure(figsize=[20,16])
      plt_title = symbol
      plt_title += f" {days[0]} - {days[-1]}"
      plt.suptitle(plt_title)

      for columns_to_graph in to_graph: 
        for column in columns_to_graph:
          if column not in asset_dfs[symbol].columns:
            print(f"Invalid column value: {column}!!")
            exit()

      indicator_plt = None
      for index, columns in enumerate(to_graph[0:4]):
        indicator_plt = plt.subplot(4, 1, index + 1, sharex = indicator_plt)
        for column_name in columns:
          series = asset_dfs[symbol][column_name]
          indicator_plt.plot(series.index, series, label=column_name)
          indicator_plt.grid(True)
          indicator_plt.legend(loc=2)
          indicator_plt.yaxis.set_major_formatter(ScalarFormatter())
          indicator_plt.yaxis.set_minor_formatter(ScalarFormatter())

      plt.tight_layout()
      plt.show()
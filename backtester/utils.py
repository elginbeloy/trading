from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt
import matplotlib as mlp

colors = [
  "#038DB2",
  "#F9637C",
  "#FBB45C",
  "#45AAB4"
]
mlp.rcParams['axes.prop_cycle'] = mlp.cycler(color=colors)

def has_n_days_data(df, start_date, days):
  return len(df.loc[:start_date].index.to_list()) > days

# Returns the "returned" capital in USD (positive or negative) of a simple
# /n asset investment strategy.
def get_n_over_a_returns(asset_dfs, starting_cash, commission_slippage, start_date, end_date):
  total_return = 0
  amount_to_invest_per_symbol = starting_cash / (len(asset_dfs.keys()) * (1 + commission_slippage))
  for symbol in asset_dfs:
    # TODO: the "buy" function will use the next day open for purchase price.
    # But given we only want returns, we can ignore the actual price and use
    # the close price only - like a real strategy would for calculating the
    # purchase amount. 
    asset_first_known_price = asset_dfs[symbol].loc[start_date:]["Close"].iloc[0]
    post_end_open_prices = asset_dfs[symbol].loc[end_date:]["Open"].to_list()
    asset_end_price = 0 
    if len(post_end_open_prices) > 0:
      asset_end_price = post_end_open_prices[0]
    else:
      # If no price is available after end_date, take the final open price
      asset_end_price = asset_dfs[symbol]["Open"].iloc[-1]

    amount_to_buy = amount_to_invest_per_symbol / asset_first_known_price
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
            return

      indicator_plt = None
      for index, columns in enumerate(to_graph[0:4]):
        indicator_plt = plt.subplot(4, 1, index + 1, sharex = indicator_plt)
        for column_name in columns:
          series = asset_dfs[symbol][column_name]
          indicator_plt.plot(series.index, series, lw=2, label=column_name)
          indicator_plt.fill_between(series.index, 0, series, alpha=0.1)
          indicator_plt.grid(True)
          indicator_plt.legend(loc=2)
          indicator_plt.yaxis.set_major_formatter(ScalarFormatter())
          indicator_plt.yaxis.set_minor_formatter(ScalarFormatter())

      plt.tight_layout(pad=4.0)
      plt.show()
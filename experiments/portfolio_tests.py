import numpy as np
from scipy.stats.stats import pearsonr, spearmanr

# Get number of assets, asset history length, and asset data source from input
asset_amount = int(input("# Assets: "))
asset_history_length = int(input("# History Days: "))
asset_source = input("Source (yf, rand, quandl): ")
portfolio_iterations = int(input("# Iterations: "))

for iteration in range(portfolio_iterations):
  # Get list of log asset returns
  returns = np.random.normal(loc=1.0, scale=0.015, size=(asset_amount, asset_history_length))

  # Go through the list of asset returns and show their statstics
  for outer_index, yearly_return in enumerate(returns):
    # Get average covariance w.r.t all other asset returns
    avg_pearson_cor = 0
    avg_spearman_cor = 0
    for inner_index, yearly_return_2 in enumerate(returns):
      if outer_index != inner_index:
        avg_pearson_cor += pearsonr(yearly_return,yearly_return_2)[0]
        avg_spearman_cor += spearmanr(yearly_return, yearly_return_2).correlation

    avg_pearson_cor /= len(returns) - 1
    avg_spearman_cor /= len(returns) - 1
    print("Asset Information:")
    print(f"Value of $10 investemet at EOY: {yearly_return.prod() * 10}")
    print(f"Mean: {yearly_return.mean()} | STD: {yearly_return.std()}")
    print(f"Avg Pearson: {avg_pearson_cor} | AVG Spearman: {avg_spearman_cor}")
    print()
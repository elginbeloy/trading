# Backtest Framework

A simple backtest framework with the following features:
- Backtest on multiple assets 
- Get a wide array of statistics from a backtest 
- Compatible with any technical analysis library
- Simple strategy creation via Strategy class inheritance  

# Todo

- [ ] Finish adding metrics to strategy printout (5 each)
  - [ ] Maximum drawdown %
  - [ ] Maximum drawdown length days
  - [ ] Comparison to N-Over-A Buy-Hold return  
  - [ ] Sharpe ratio
  - [ ] Risk exposure over time (graph asset expenditure (y) and time (x) then take the area under the curve divided by highest possible y * total x - I.E portfolio exposure over time compared to maximum possible exposure. Could also consider what kind of exposure, I.E volatility of asset to which the portfolio is exposed)
- [ ] Re-read all code, clean up, make all functions PURE, check all metrics (?)
- [ ] Add huge list of assets to test over (?)
- [ ] Add ability to store df data locally so each new test has huge list of assets data already ready (?)

- [ ] Implement other strategies (3 each + annualized_return%)
  - [ ] Those possible from https://www.quantconnect.com/tutorials/strategy-library/strategy-library 
  - [ ] Those possible from "High Probability Trading"
  - [ ] At least three others you think of
- [ ] Write tests


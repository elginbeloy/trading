# Backtest Framework

A simple backtest framework.

# BEWARE

- [ ] We use CONSOLIDATED aggregate bar prices - which include transactions
from outside of our primary exchange and which can inflate price
- [ ] We have survivorship bias if we are not using de-listed stocks

# Strategy Approach

Think of strategies as a list of other more simplistic strategies which 
are - at their base - simple rules. Like the if statements in your next 
function, strategies are just set of rules of a buy or sell signal and a
calculation of an amount. We should find a way to define strategies as 
encoroprating more simple strategies and having a way to measure the impact
of each "rule". Maybe its only a logging mechanism to place within the ifs, 
but we need a way to measure how much each "rule" - of if statement - is 
accomplishing its goal and affecting our overall strategy.

I can then define a bunch of simple micro strategies for a ton of points.

Make the following strategies:
- find true trend and only invest in its direction
- find market type and only invest accordingly
- find a way to predict downward volatility and avoid highly volatile periods
- use indicators like MACD and STOCH to avoid overbought periods 
- use indicators like MACD and STOCH to invest in undersold periods
* Note how the last two ^^^ are different strategies. This is so we can measure 
their impact and profitability alone without each other and under other conditions. When generating buy/sells for these "avoid" strategies, simply incorporate a "STANDARD" model of buy/sell strategies that is used elsewhere.
This list can mimic the current "overall strategy" which takes the best
micro strategies based on which has - on its own - shown to be profitable
and statistically significant and effects the overall strategy positively
either through risk or profitability when added. 
- 
as well as those from "High Probability Trading", Ernie Chan's book,
"The Encyclopedia of Chart Patterns", Investopedia and other websites.

# Strategy Creation Process

1. Come up with a bunch of potential ideas, read, watch, listen to try and induct
more theories.
2. See the "impact" - null test and measure the statistical significance of
your theorized rule. 
3. Add them to your backtest to see if it improves.
4. Keep in backtest, optimize parameters.
5. After doing this with a number of theories and rules, test outside time
and asset.

Ex. You think if ATR is some amount greater than some MA of ATR you can 
help increase the "predictability" of an assets price behavior with your 
current list of rules. You go back and test this theory historically with 
a large number of assets and a multi-year time period. It does seem to make
your existing model more predictive, so you add it to your current strategy.
Backtesting it yields improved results that are statistically significant, 
so you optimize the threshold and MA window length.

# Todo

- [ ] Re-read all code, clean up, make all functions PURE, check all metrics (?)
- [ ] Implement other strategies
  - [ ] Those possible from https://www.quantconnect.com/tutorials/strategy-library/strategy-library 
  - [ ] Those possible from "High Probability Trading"
  - [ ] At least three others you think of
- [ ] Make execution Market-On-Open or Market-On-Close for the next day
  - [ ] Trade at the price of the bid/ask + slippage of the first order on the CORRECT exchange to replicate reality. IMB = NYSE, MSFT = NASDAQ 
- [ ] Add intra-day data to strategy class for use
- [ ] Add stop-loss and limit orders
- [ ] Use bid-ask spread to backtest actual execution cost
- [ ] Write tests

- [ ] Finish adding metrics to strategy printout (5 each)
  - [ ] Maximum drawdown %
  - [ ] Maximum drawdown length days
  - [ ] Comparison to N-Over-A Buy-Hold return  
  - [ ] Sharpe ratio
  - [ ] Risk exposure over time (graph asset expenditure (y) and time (x) then take the area under the curve divided by highest possible y * total x - I.E portfolio exposure over time compared to maximum possible exposure. Could also consider what kind of exposure, I.E volatility of asset to which the portfolio is exposed)
- [ ] Add plot metrics
  - [ ] Return distribution as historgram
  - [ ] Simple line plot of portfolio value over time
  - [ ] Get a visual buy sell "trigger" chart to inspect 
- [ ] Find a way to inspect each part of the system individually
  - [ ] Find the right testing "criteria" for each part of the system
  Does your volatility drop-out indicator work out as expected for avoiding
  herd behavior?
  Does your indictor help prediction of the variable in the way you think?
- [ ] Find a way to figure out "why things are happening" so you can see 
  what indicators are actually useful or not.

- [ ] Add ML strats
  - [ ] Decision tree 
  - [ ] Neural network simple LSTM that takes in zero mean centered data - as it preserves series volatility, memory, but mostly accounts for magnitude. Give it technical indicators to represent larger time period trends like ADX, MACD, MFI,
  as well as the actual open, high, low close to find a good daily entry. Label with 10-30 day triple barrier method and LOTS of data. Focus on just getting actual predictions and not always one class. Try lots of y labels. Try lots of technical indicators, different time periods, different data combination methods, different data augmentation methods, etc... Once it finally works, try out its predictions as a strategy and backtest it here. Get some real predictions and your set to start.
# ap22 

Asset Price Appreciation Predictor V2 | Elgin Beloy

ap22 is a simple approach to predicting asset price appreciation over a period
using past price action data. Specifically, ap22 utilizes past trade data from
[polygon](https://polygon.io) to create custom information-imbalance bars that 
are then fed into a multi-layer LSTM for a binary prediction. Said final 
prediction is if an asset will appreciate over an abstract percentage `n` 
within an abstract period of time `p` without first running into a stop-loss 
depreciation percentage `s`. Choices of `n`, `p` and `s` can vary based on the 
trading approach or could be optimized for better predicitibility. 

ap22 is not a trading model insofar as it does not actually execute trades. 
Rather, think of ap22 as an analyst that informs a trader with yet another
reference point for asset appreciation likelihood. See ap22 predictions
as a new probability that can update our prior (Bayesian adjustment). This idea
could be further expanded by imagining that we may one day feed ap22 output
predictions as input to another ML model that weighs ap22, sentiment data, and 
other information to make a more well informed prediction. This way ap22
represents information gleamed from price action, and that can be combined
with other sources such as technical indicators, sentiment data, analyst 
predictions, etc...

## Design 

ap22 is broken up into four distinct parts each with their own nuances
and room for improvement/optimization:
1. downloading trade data
2. bar generation from trade data
3. x, y data creation from bar data (includes labeling and normalization)
4. model construction, training, evaluation, and prediction 

### 1. Downloading Trade Data

All data comes from the 
[polygon trades api](https://polygon.io/docs/get_v2_ticks_stocks_trades__ticker___date__anchor).

Data is downloaded by the day via REST request - 1+ request/day/symbol. 
Given all of the requests needed for hundreds of symbols over hundreds of days,
downloading trades can take a long time. Thus, to save time we save data 
locally after downloading from Polygon. We can then upload to our cloud 
service instead of forcing them to make thousands of requests.

For the list of symbols, we use a hardcoded list of popular stocks from 
Robinhood collections. We also have a function for web-scrapping the 
symbols from Robinhood collections.

### 2. Bar Generation

Using the trades data from polygon, Bars are created based on an imbalance rule
rather than abstract time intervals like 1 minute. The approaches should be 
compared and final accuracy reviewed though. Other imabalance methods should
also be researched and employed. 

If bar generation takes long enough, we should consider also saving generated
bars, not just requested trades.

### 3. Data (X, Y) Creation

X data is the normalized bar data and Y is the tripple barrier method. 
Normilization methods and labeling should be reconsidered and researched. 

### 4. Model Construction

The model is a multi-layer LSTM. Architecture and evaluation should be considered.

## Experiment Results

--
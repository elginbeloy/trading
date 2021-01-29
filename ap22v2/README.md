# ap22 

Asset Price Appreciation Predictor V2 | Elgin Beloy

ap22 is a binary-model approach to predicting asset price appreciation over a
period using ML. ap22 utilizes past trade data from the service 
[polygon](https://polygon.io) to produce a binary prediction with a LSTM. 

ap22 is not a trading model insofar as it does not actually execute trades. 
Rather, think of ap22 as an analyst that informs a trader with yet another
reference point for asset appreciation likelihood. See ap22 predictions
as a new probability that can update our prior (Bayesian adjustment). This idea
could be further expanded by imagining that we may one day feed ap22 output
predictions as input to another ML model. This way ap22 represents information
gleamed from past price action, which can then be combined with other sources
of information such as indicators, sentiment data, analyst predictions, etc...

----

## Design 

ap22 is broken up into five files for each of its functions:
1. `get_symbols.py` - has different symbol lists, including scraping options
2. `get_trade_data.py` - downloades trade data from polygon
3. `get_aggregate_bars.py` - creates (or queries) aggregate bars
4. `get_x_y.py` - creates (x, y) model-ready data from aggregate bars (includes labeling and normalization)
5. `ap22.py` - constructs, trains, evaluates, and predicts the model

### 1. get_symbols.py

Mostly used prior to downloading data, `get_symbols.py` provides a few options
for symbol lists based on sector, size, etc... 

It can also scrape Robinhood collections pages to get new symbols lists.

### 2. get_trade_data.py

> Note: Individual trades data is only needed for custom, non-time-interval 
aggregate bars such as information-imbalance bars

All data comes from the 
[polygon trades api](https://polygon.io/docs/get_v2_ticks_stocks_trades__ticker___date__anchor).

Data is downloaded by the day via REST request with a limit of 50k trades. 
Given the amount of requests nessesary to download years of trade data, it 
should ideally only be done once. Because of this `get_trade_data.py` takes 
a list of symbols and a time interval then saves the trades data locally 
as a `.npy` numpy file. 

For analysis we can then load the data from storage with `np.load`. 
When training in the cloud we can upload from our computer a single time.

Files are saved with the format `{SYMBOL}-{START_DATE}-{END_DATE}`. 
Two intervals of the same symbol can be easily combined by loading 
both as seperate numpy arrays and concatening them. 

### 2. Bar Generation

`get_aggregate_bars.py` supports multiple different aggregate bar types:
1. time-interval bars - 1m, 5m, 1h, 1d, etc...
2. tick/volume/dollar interval bars - 
2. tick/volume/dollar imbalance bars - 

For time-interval bars, OHLCV data is downloaded directly from 
[polygon's OHLCV REST endpoint](https://polygon.io/docs/get_v2_aggs_ticker__stocksTicker__range__multiplier___timespan___from___to__anchor) 
with the desired interval. Split and dividend adjustments are applied for us 
by default.

For all other aggregate bar types we construct the bars ourselves using the 
trades data from polygon as saved in our data download directory. 

Using the trades data from polygon, Bars are created based on an imbalance rule
rather than abstract time intervals like 1 minute. The approaches should be 
compared and final accuracy reviewed though. Other imabalance methods should
also be researched and employed. 

> Note: If bar generation takes long enough, we should consider also saving generated
bars, not just requested trades.

### 3. Data (X, Y) Creation

X data is the normalized bar data and Y is the tripple barrier method. 
Normilization methods and labeling should be reconsidered and researched. 

### 4. Model Construction

The model is a multi-layer LSTM. Architecture and evaluation should be considered.

## Experiment Results

--
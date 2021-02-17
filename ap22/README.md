# ap22 

**Asset Price Appreciation Predictor V2 (ap22)**

ap22 is an LSTM model for predicting the probability an asset price will 
appreciate over a certain threshold within a period without first depreciating
below a stop-loss amount. See the [tripple barrier label](https://mlfinlab.readthedocs.io/en/latest/labeling/tb_meta_labeling.html).

ap22 utilizes past trade data from the service [polygon](https://polygon.io). 

ap22 is not a trading model insofar as it does not actually execute trades. 
Rather, think of ap22 as an analyst that informs a trader with yet another
reference point for asset appreciation likelihood. See ap22 predictions
as a new probability that can update our prior (Bayesian adjustment). This idea
could be further expanded by imagining that we may one day feed ap22 output
predictions as input to another ML model. This way ap22 represents information
gleamed from past price action, which can then be combined with other sources
of information such as indicators, sentiment data, analyst predictions, etc...

That said, ap22 could go through a list of assets and return those 
that are most likely to appreciate within a preferred period without hitting
a stop-loss. This portfolio could then be optimized based on probability 
of predicted returns using the [pyportfolioopt](https://pyportfolioopt.readthedocs.io/en/latest) library.

> NOTE: A black-box modeling approach like this is likely not the way to 
> discover profitable strategies, but nonetheless may help find initial 
> exploitable correlations and combined with other methods could help 
> make trading decisions. See https://medium.com/@beloy.elgin/stop-trading-back-tested-models-start-trading-theories-e306dd3cc933

----

## TODO 

- [x] Add README.md with latest design and other information
- [ ] Add `model.py` with embeddings for categorical features and multiple
input nodes with a concat. 
- [ ] Add bid/ask data.
- [ ] Finish bar aggregation code for tick, volume, dollar, imbalance bars.
- [ ] Run automated experiments for finding optimal hyperparams.
- [ ] Add prediction code. 
- [ ] Add prediction portfolio creation/optimization with pyportfolioopt.
  - [ ] Look into expanding model with meta-labeling for deciding
asset allocation sizes from the probability outputs of the first model.

## Experiment Results

Current Results:

```
1000 Epochs:
loss: 0.6382 - accuracy: 0.6247 - val_loss: 0.7576 - val_accuracy: 0.5155
```

## Design 

ap22 is broken up into six files for each function (excluding utils):
1. `get_symbols.py` - returns different asset symbol lists, including 
web-based scraping options.
2. `get_trade_data.py` - downloads tick-level trade data from 
[polygon](https://polygon.io).
3. `get_aggregate_bars.py` - creates (or queries) various aggregate bar types
including time, tick, volume, dollar, and event/imbalance.
4. `get_x_y.py` - creates (x, y) model-ready data from aggregate bars.
5. `model.py` - WIP constructs the ap22 LSTM model architecture.
6. `ap22.py` - the main entry point responsible for training, evaluation, 
prediction and portfolio creation/optimization. 

### 1. get_symbols.py

Mostly used prior to downloading data, `get_symbols.py` provides a few options
for symbol lists based on sector, size, etc... 

It can also scrape Robinhood collections pages to get new symbols lists.

### 2. get_trade_data.py

> Note: Individual trades data is only needed for custom, non-time-interval 
> aggregate bars such as tick/volume/dollar/information-imbalance bars

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

### 3. get_aggregate_bars.py

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

### 4. get_x_y.py

X data is the normalized bar data and Y is the tripple barrier method. 
Normilization methods and labeling should be reconsidered and researched. 

### 5. model.py / ap22.py

The model is a multi-layer LSTM.

Categorical data is fed into an embedding layer:

> a one-hot encoding followed by a dense layer is the same as a single embedding layer. Try both and you should get the same results with different runtime. Do the linear algebra if you need to convince yourself.

Ref: https://github.com/keras-team/keras/issues/4838

For the embedding layer output dimension consider:

> number_of_categories_for_embedding ** 0.25

Ref: https://developers.googleblog.com/2017/11/introducing-tensorflow-feature-columns.html

Another possible approach is outlined in [the following paper.](https://www.aclweb.org/anthology/I17-2006.pdf)

For combining multiple input layers (I.E the embeddings with other variables) see the following examples:
1. [Blogpost](https://jessicastringham.net/2019/06/02/climate-with-keras)
2. [Notebook](https://github.com/mmortazavi/EntityEmbedding-Working_Example/blob/master/EntityEmbedding.ipynb)
3. [SO post](https://stackoverflow.com/questions/51360827/how-to-combine-numerical-and-categorical-values-in-a-vector-as-input-for-lstm)
4. [Kaggle Kernel](https://www.kaggle.com/kowaalczyk/lstm-with-convolutions)

--
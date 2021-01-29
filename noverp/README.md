# Predictive Ensemble for Price Appreciation 

A strategy for finding n% asset appreciation over a period p and using
n% appreciation as an auto-sell trigger.

## Description

Assets are purchased and set to auto-sell at an n% appreciation. 
The asset selection process utilizes ML model predictions for the probability
an asset will have an appreciation >= n% over the period p (n over p).
Various models can be created for different n and p values allowing the 
practitioner to construct portfolios with various risk adversity levels. 
Multiple models can be combined to create bands of appreciation probabilities.
The bands could then be integrated into a broader quantamental approach to 
asset selection. True-positive to false-positive ratio should be optimized to
minimize the unaccounted risk. Additionally, the auto-sell trigger level should
be considered as it may be lower than the actual predicted n% value.

## Data Selection & Pre-Processing

The data used to train our model is processed from Yahoo Finance.

Data is fed to the model as sequential vectors of the past
p days of [
  high,
  low,
  open,
  close,
  close_change,
  close_percent_change,
  Close 5-day-SMA,
  Close 10-day-SMA,
  Close 15-day-SMA,
  Close 25-day-SMA,
  close 50-day-SMA,
  close 100-day-SMA, 
  close 250-day-SMA,
  W/RSI-5 (+ fluctuation percentage),
  W/RIS-10 (+ fluctuation percentage),
  W/RSI-14 (+ fluctuation percentage),
  MACD,
  MACD-Signal,
]

## The Model

The model used is a LSTM network.

## Training & Evaluation

Results: 

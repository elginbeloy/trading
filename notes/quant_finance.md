# Quant Finance

## CAPM - Capital Asset Pricing Model: 

The capital asset pricing model is a formula for calculating the risk adjusted returns of an asset. The goal of the CAPM formula is to evaluate whether a stock is fairly valued when its risk and the time value of money are compared to its expected return. It states that the risk adjusted return for an asset is equal to the risk free rate (usually the yield of T-Bills) plus the asset beta multiplied by the market risk premium.
Asset Beta is the asset's volatility (as a proxy for risk) relative to the rest of the market. Asset Beta is calculated by dividing the covariance of the asset to the market by the overall market return variance
Market Risk Premium is defined as the difference between the expected return on a market portfolio and the risk-free rate (T-bills)

## SR - Sharpe Ratio: 
A ratio of returns (minus the risk free rate) to volatility.

## Sortino Ratio: 
A version of the Sharpe Ratio that only considers downside volatility as risk. 
I.E a ratio of returns (minus the risk free rate) to downward (under mean) 
volatility.

## Treynor Ratio: 
A ratio of returns (minus the risk free rate) to the combined asset beta of 
the portfolio.

## Stationarity: 

Non-stationary series have no defined mean and an infinite variance, thus any estimations based on a sample from said series will be biased out-of-sample and spurious correlations are more likely. 
Data transformations like detrending, demeaning, differencing, ARMA structure, elimination of pulses/level shifts/seasonal pulses/local time trends, etc...  are used to convert a non-stationary series into a stationary one with parameters of the process (I.E the mean, variance, and covariance) being constant between intervals.

Takeaway for ML: Ultimately the proof is in the pudding. That is, do model validation like you would with any other machine learning project. If your model predicts well for hold-out data, you can feel somewhat confident in using it. But like any other ML project - if your test data is ever significantly different than your training data, your model will not perform well. See a toy example LSTM predictions on stationary and non-stationary series.

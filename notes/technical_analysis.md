# Technical Analysis (TA)

Technical analysis is the process of analyzing an assets past price action
in an attempt to discern information/patterns that could be used to profit
off the assets future price action. Technical analysts utilize technical 
indicators (variables calculated from past price action), visulizations 
(such as price candlestick charts), and other methods all with the common
goal of discerning repeatable price action behaviors that can be exploited.

The key difference between technical analysis and quantatative/ML approaches
is the reliance on math & statistics (quant) vs. pattern intuition (TA).
TA often relieis on hunches drawn from past experiences, I.E "this pattern 
tends to mean a breakout, but watch to make sure". Because of this, TA is much
more approachable, but much less known for involving out-of-sample back-testing
or the rigorous mathmatical hypothesis testing seen in econometrics. 

## Technical Indicators

### RSI - Relative Strength Index:

RSI is an oscillating (0 →100) indicator for measuring the smoothed average 
gain over the smoothed average loss for an N-day period (usually 14 days). 
Though faulty, analysts treat RSI > 70 as overbought and RSI < 30 as oversold. 

Calculation:
`relative_strength = average_gain / average_loss`
`RSI = 100 - 100 / (1 + relative_strength)` 

Where `average_gain`/`average_loss` is the average daily percentage change 
for days where the price of the asset increased/decreased from open to close.

Key takeaways:
- Higher magnitude price gains raise RSI while higher magnitude losses lower it
- An RSI of 50 happens when average gain is equal to average loss
- An RSI of 70 happens when the average gain is 2.33 times the average loss
- An RSI of 30 happens when the average loss is 2.33 times the average gain
- RSI fails to recognize overall volume, hence MFI as an indicator

### MFI - Money Flow Index:

AKA the volume-weighted RSI, MFI is a more complete indicator that looks at 
both volume and the average price change magnitude over a period. 

Calculation:
`typical_price = high * low * close / 3`
`money_flow = typical_price * volume`

Given typical_price at a day `t` is `TP_t`, money flow at day `t` is positive
if `TP_t > TP_(t-1)`, negative if `TP_t < TP_(t-1)` and, in some cases, equal 
to `t-1` if `TP_t == TP_(t-1)`

`money_flow_ratio = positive_money_flow / negative_money_flow`
`MFI = 100 - 100 / (1 + money_flow_ratio)`

Key takeaways:
- Takes not only the prices positive/negative momentum over a period (RSI)
but also the volume of trades during that period of momentum. This shows
investor participation which can be used as validation of a trend. 
For example, an increasing price trend with a decreasing MFI is usually a 
bearish signal as it indicates lower bull participation as the price 
trends upward, meaning less liquidity aggresion to power the trend through.


### Bollinger Band: 

A Bollinger Band is a technical analysis visual pattern used for finding abnormal price action - namely price action two standard deviations from a standard moving average. A Bollinger Band is created by plotting a N-day Standard Moving Average (SMA) line (usually N=20) and two equidistant surrounding lines, the upper and lower, forming a band. The upper and lower lines are usually 2 standard deviations from the middle line, though they can be one SD or another variant. Bollinger Bands are helpful for identifying potentially overbought or oversold positions given normally 90% of price action falls within 2 standard deviations of the 20 day moving average.

### Crossovers (Golden + Death Crosses): 

Crossovers happen when one plotted line “crosses over” the other, I.E intercepts. The lines are typically a longer and shorter SMA (usually 200/100 day and 50/25 day respectively) . Like most indicators and patterns in technical analysis, crossovers like the golden cross and death cross simply find recent growth or loss with a higher magnitude than the longer term trend. This can be said to indicate a new trend or a potential reversal at play when a security is overbought or oversold 
NOTE: with all signals/indicators/patterns, abnormal price movement can continue for days, weeks, or even months and could potentially even signal the start of a new primary trend. So betting against it using only a cross/RSI/MFI/MACD is a NO.
Crossovers are usually confirmed with higher trading volume, things like the current MFI can be considered in conjunction to further confirm/invalidate a crossover 

### Stochastic Oscillator: 

An oscillating (0 →100) indicator for measuring recent positive price momentum. It does so by taking the ratio of the most recent close minus the lowest close over the highest close minus the lowest close. Basically how close is the current close to the highest point. Like RSI/MFI it is meant to produce overbought/oversold signals.

### MACD - Mean Average Convergence Divergence: 

The MACD is a common technical analysis indicator used for finding changes in short term momentum as a potential buy/sell signal. The MACD is a line plotted by subtracting a longer EMA from a shorter EMA, typically 26 and 12 days respectively. Positive MACD values indicate recent positive momentum, negative indicate recent negative momentum. A 9 day EMA of the MACD, known as the signal, often accompanies the MACD plotted alongside it. The MACD going above the signal line indicates recent positive momentum in the price and below indicates a smaller than 9-day-EMA recent positive price momentum.

## Charting / Trade Data Visulizations 

## Support & Resistance

Support and resistance zones/points are price ranges or values that act as a barrier for a security trend to break through. Often support and resistance zones are identified by a repeated inability for a price to break through causing consistent and temporary reversals / retracements. Zones that prop a price up (I.E the price is unable to dip below) are called support whereas zones that prevent a price from continuing its rise are called resistance.
Used to find points where a prevailing trend may pause or reverse or to identify breakouts from pervious support/resistance levels
Support and resistance points can be identified as static numbers (horizontal lines) or as values along a general trend line (often identified from a moving average)
Static round numbers can act as support/resistance (horizontal) lines as they are common triggers for sell offs/purchases and may be psychological 
Moving Average (MA) lines tend to act as support on an upward trend and resistance on a downward trend
Once breakouts occur (defined as the point at which a security price breaks out of the support/resistance zone), the role of a zone can be reversed. Meaning a trendline once providing a point of support can become a point of resistance
The significance of a support/resistance zone can be identified by
The number of “touches” or times a security came close but failed to break the underlying support/resistance line barrier
Includes false breakouts
The momentum that has previously been able to cause a retracement. Higher momentum trends that enter reversal in a zone indicate the zone is stronger than the underlying momentum that tried to break it

## Chart Patterns

### Effectiveness:

Technical Analysis (A Stanford EDU Final Report) found that training kernel regressors to trade based on the extrema of patterns like head and shoulders, inverse head and shoulders, broadening top, and broadening bottom had high sharpe ratios (some > 5) on both in and out of sample data. Below is a list of the most common technical analysis trading patterns. Those that have proved effective in the literature are highlighted as blue and also come with a “why” section detailing what this pattern may tell us about the underlying market microstructure and psychology given it’s predictive capabilities. 

### Lines - Trend, Support, Resistance: 

The most basic of technical analysis patterns are linear lines which can indicate support levels, resistance levels, or using moving averages, trends. An upward trend sees higher local maxima followed by higher local minima over the time series period (I.E positive slope). Conversely, a downward trend sees lower local maxima followed by lower local minima over the time series period (I.E negative slope). Volatility with a moving average that stays static (I.E no slope) indicates consolidation and often forecasts a breakout from the recent support/resistance zone. The breakout is usually correlated in magnitude to the length of the consolidation and inversely correlated in magnitude to the level of volatility and volume of trades during the consolidation period. 

### HS - Head and Shoulders: 

A common bullish-to-bearish reversal price pattern identified by a shoulder (local maxima) followed by a retracement (local minima) followed by a head (local maxima, global over the pattern) followed by another retracement and a second shoulder then the bullish reversal. Inverse head and shoulders identify the same pattern of extrema inverted (replace each maxima with a minima and minima with a maxima or imagine flipping the price pattern over the horizontal bottom line to be upside down). As you’d expect, inverse head and shoulders predict the opposite price action, namely a bearish-to-bullish reversal. 
Why? Intuitively, head and shoulders patterns and their inverse can be seen as another indication of momentum reversal in a current trend. In a positive trend with growing positive momentum the highs should continue to get higher. The head and shoulders indicates the slowing upward momentum with the third shoulder, which is a smaller high than the previous head, and which often comes with smaller trading volume. This smaller high paired with decreased buying power indicates a trend reversal from the previous bull to a new inability to gain higher highs. The breakage of the support line created by the two shoulder retracement minima is further evidence of a change in trend. This intuition explains the importance of validating the pattern with trading volume and other indicators. Specifically, trading volume should be higher in the first shoulder and head than in the positive movement of the third shoulder, this signals the exhaustion of buying power.

### Pennant: 

A price trend continuation pattern identified by a large movement in a security, known as the flagpole, followed by a consolidation period with converging trend lines - the pennant - followed by a breakout movement in the same direction as the initial large movement, which represents the second half of the flagpole. 

### Flag: 

A continuation price pattern showing an area of counter-trend consolidation directly following a sharp movement in price matching the current trend. Flags often forecast a continuation in the original trend, usually in the form of another sharp movement in the trend direction.
Broadening Formation: a reversal pattern characterized by increased volatility after a recent upward (broadening top) or downard (broadening bottom) movement. Broadening top typically indicates a bullish-to-bearish reverse, and conversely broadening bottom indicates a potential bearish-to-bullish reversal. A broadening formation is typically shown visually by graphing two sem-horizontally-semetric, diverging (increased volatility) support and resistance lines. Broadening Bottom is shown by the literature to be one of the most profitable trading pattern strategies when identified with regression kernels trading with a out-of-sample mean sharpe ratio of 5.4.
Commonly, each of the support/resistance lines must be touched at least twice for the pattern to be considered relatively validated. 
Trades usually involve trading the breakout, with purchases coming slightly after a reversal price breakout from the graphed support/resistance lines of the formation. 
Note that broadening formations are more common during times of underlying asset evaluation volatility (earnings coming up, etc…), and otherwise are relatively rare. 
Why? The pattern indicates increased volatility and disagreement about the price. For instance, broadening formations are common prior to elections in FOREX or earnings for securities. This means a reversal may not always be at play, however there is disagreement and that has become the new trend in a sense. Note that a trend is characterized by either increasing tops and bottoms, or decreasing tops and bottoms. However, the broadening formation indicates volatility and disagreement is growing over the period, but the previous trend has already either failed to produce consistently higher lows or consistently lower highs, so the momentum has changed which can indicate a fundamental factor change to come. 

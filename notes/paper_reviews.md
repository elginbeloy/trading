# Paper Reviews & Takeaways

## Technical Analysis (A Stanford EDU Final Report)

The paper focuses on technical analysis price movement patterns and their 
back-tested predictability of future price. The authors utilize Kernel 
Regression to estimate price movement (this avoids noise in price action), 
then from that estimation algorithmically identify different price patterns
using maxima and minima within a window. A list of 8 common chart patterns 
are used including Head and Shoulders, Broadening Formations, Double Bottoms
and others. 

The paper offers formal mathematical definitions of common technical analysis 
chart patterns based on price extrema. For instance double bottom would be
two minima intersected by a local maxima. 

Algorithmically, the authors identify the patterns then take positions in 
accordance with what the pattern tends to predict. Ultimately they find that 
Broadening Bottoms, Broadening Tops, and Inverse Head and Shoulders have the 
highest risk adjusted returns in their simulation with respective out-of-sample
modified Sharpe ratios of 5.5683, 3.99147, and 3.3525 respectively. 

This paper is closely, closely related to (like almost a copy of): 
https://www.cis.upenn.edu/~mkearns/teaching/cis700/lo.pdf, 


## Financial Time Series Forecasting with Deep Learning : A Systematic Literature Review: 2005-2019


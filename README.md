# Elgin's Trading

My notes, strategies, experiments, etc... 

## TODO

1. Data Understanding (20)
- Code a way to download complete time aggregate bars
  - Verify via logs it has everything maybe even write test
- Add a shit load of data based logging so look through and understand the data and model
- Go through logged bars data and understand various statistics about it
  - What value of n, s, and p have best class imbalance values?
  - What value of n, s, and p are most exploitable w/ good class imbalance?
  - How often is data missing? 
  - What outliers are present? What types and how common? 
- Go through x, y generation from bars and understand:
  - What is the general period mean, variance, etc...
    - Potentially also look into autocorrelation and other statistics
  - How does normilization and standardization effect bar values in the period?
    - Is any information lost with the current method? 
      - We only see change w.r.t to the period mean for the column
      - I.E x is a 200-500 long sequence of OHLCV+VW+N values changing around their mean divided by their standard deviation for the period
      - Is scale information lost? Volume scale relative to other stocks/periods.
    - Is there a better method?
  - What else could be added from the price action data to add additional info?
  - Add minute of hour(?), hour of day, day of week, month of year, week of month (7/5 + 12 + 5 = 12/10 bits)
    - Look into using continous values if appropriate (https://stats.stackexchange.com/questions/164542/is-time-of-the-day-predictor-in-regression-a-categorical-or-a-continuous-varia)
- Expand total dataset by getting way more symbols and thinking through a good period logic
  - Don't want to find correlations that no longer exist, but want a longer period for more data with the cyclical patterns 
- Research a good way to measure variable importance and utilize it to select the best input data values (categorical vs. continuous date values)
2. Try out various model architectures (stateless vs. stateful, GRU, other configurations, etc...)
- Select a few of the best and use those to do other hyperparameter tuning
3. Try out various bar aggregation methods and hyperparam test with the best models
- For every hyperparater select the top 3-5 best options and tweak through those while testing other hyperparameters until you find the best combination of each
4. 
    

1. See and understand your data. Make it your best friend.
- Do you have all of your data? How can you expand it? Bigger = Better in most cases so spend a lot of time here until its as big as can be.
- What is a good y-label that is exploitable, predictable, and has a good binary-class balance.
- Go through data labeling and creation process and make sure each part and the final product is super clear to you. Log shit in log files and read through them.
- Try out a few model architectures once you are happy with the data labeling, normilization, lookback, etc... 
- Select a good archictecture while noting other good options.
- Try different bar aggregation methods and see if it increases predictability.
- Try adding a new network that looks at longer trend and other data.

[ ] 1. Write up ap22 README.md
[ ] 2. Break out ap22 into seperate components for 
- the trade data download process
- the bar generation process (for a single symbols trades)
- the x, y creation and data normilization process
[ ] 3. Add the ability for ap22 to save and load 
- polygon downloaded trade data (json)
- generated bars (json)
- x and y data (numpy array) (does this take as long as download or bar generation?)
[ ] 3. Test out different hyperparameters writing results in ap22 README.md
- bar generation methods
- data normilization methods
- data inclusion 
- model architectures
[ ] 4. Add prediction at the end of ap22
- run over all of the possible symbols highest to lowest
- create a diversified portfolio based on outputs
- add to the README
[ ] 5. Do recorded review of the code + results + predictions
- send to Evan & Gavin in email thread and Ryan and 
[ ] 6. Add auto-hyperparameter tuning for the model in the code (?)

=============== RESEARCH PHASE 1 ===============

[ ] 1. Organize the algorithmic trading notes google doc
[ ] 2. Read Investopedia articles, as many as you can, and take notes
- Dividends, splits, glossary, etc...
[ ] 3. Read about market microstructure

[ ] 1. Read up and understand how to account for dividends, splits, auctions, etc...
- Implement the nessesary changes to account for dividends, splits, outliers, etc...
[ ] 2. Study up and do personal analysis on various bar-creation methods to find
- What is the best bar creation method?
- What is the best tick classification method?
- What information should a bar contain?
- How should the data be normalized? 
    - Should we difference?
    - How do we prevent look-ahead bias while creating bars and
    normalizing data
[ ] 3. Look into the most predictive and explotable label (I.E y value).
- What values are more predictive yet also exploitable? 
- Binary vs Categorical vs regressive?
- Specefic price exploits to search for? 

=============== RESEARCH PHASE 2 ===============

[ ] 1. Look into combining the LSTM output with technical indicators 
from time-based bars, put/call ratio, stock sentiment information, 
recent analysis, macroeconomic variables, potential patterns, and any 
other pertinent informtion for a final combined prediction.
[ ] 2. Look into expanding that multi-model with meta-labeling for deciding
asset allocation sizes from the probability outputs of the first model.
This will ultimately select the final portfolio from a list of potential 
assets using the data available. 


https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/understanding-machine-learning-theory-algorithms.pdf
https://d2l.ai/d2l-en.pdf

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2182819

https://towardsdatascience.com/ai-for-algorithmic-trading-rethinking-bars-labeling-and-stationarity-90a7b626f3e1
https://towardsdatascience.com/information-driven-bars-for-financial-machine-learning-imbalance-bars-dda9233058f0

https://poseidon01.ssrn.com/delivery.php?ID=404002065095095009122016077109100031102074091084049053125007107000112098122124019025056004106123018045005080071091102017066097107034037021035113000067020007079095073047083084007092075115000071069093092004073022112004126097029125020118075008099087078&EXT=pdf&INDEX=TRUE


1. Read through https://www.quantconnect.com/tutorials/strategy-library/strategy-library
2. Read through https://arxiv.org/pdf/2003.01859.pdf
3. Read through https://arxiv.org/pdf/1911.13288.pdf
4. Read through http://proceedings.mlr.press/v95/li18c/li18c.pdf
5. Read through https://par.nsf.gov/servlets/purl/10149715


# Foundational Learning

- [ ] Watch all of Essence of Calculus
- [ ] Watch all of Essence of Linear Algebra
- [ ] Watch all of https://ocw.mit.edu/courses/mathematics/18-650-statistics-for-applications-fall-2016/lecture-videos/
    - [ ] Read accompnying lecture notes
- [ ] Do all of https://www.khanacademy.org/math/linear-algebra
- [ ] Do all of https://www.khanacademy.org/math/ap-calculus-bc
- [ ] Do all of https://www.khanacademy.org/math/ap-statistics
- [ ] Do Probability Theory class
- [ ] Watch all CS229n videos
- [ ] Read of CS231n lecture notes
- [ ] Read https://web.stanford.edu/~hastie/ElemStatLearn/printings/ESLII_print12_toc.pdf
- [ ] Read https://www.microsoft.com/en-us/research/uploads/prod/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf
- [ ] Read through https://d2l.ai/index.html
- [ ] Read https://www.deeplearningbook.org/


# ML/ML-Quant Learning

- [ ] Do https://ocw.mit.edu/courses/mathematics/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/lecture-notes/
- [ ] Read https://github.com/PlamenStilyianov/FinMathematics/blob/master/Financial%20Calculus%20An%20Introduction%20to%20Derivative%20Pricing-Baxter.pdf

- [ ] Read Financial ML Textbook
- [ ] Read Machine Learning for Algorithmic Trading
    - [ ] Use https://github.com/PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition
- [ ] Read Advances in Financial Machine Learning

- [ ] Read https://ruder.io/optimizing-gradient-descent/index.html
- [ ] Read https://arxiv.org/pdf/1712.09913.pdf
- [ ] Read file:///Users/elgin2/Downloads/FAQ2.html#A_std
- [ ] Review https://arxiv.org/pdf/1902.07892.pdf
- [ ] Review https://www.researchgate.net/profile/Gisele_Pappa/publication/221532708_Adaptive_Normalization_A_novel_data_normalization_approach_for_non-stationary_time_series/links/0c96051cc596087da6000000/Adaptive-Normalization-A-novel-data-normalization-approach-for-non-stationary-time-series.pdf

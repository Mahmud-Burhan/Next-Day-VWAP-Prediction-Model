# Next-Day-VWAP-Prediction-Model
Modelling any stocks' future VWAP. It predicts the next day VWAP of a stock by applying Inverse CDF Function and Monte Carlo algorithm.
The example product (VWAP model graph) can be seen in the example.png, it only took approximately 10 second to produce 1 VWAP graph with 20,000 simulations.

## Libraries required
- Jupyter Notebook
- Scipy
- Numpy
- Matplotlib
- Pandas
- yFinance

## How to use the project
1. This project is made as simple as possible as it is intended for personal usage.
2. The source code is made to be ran basically inside a Jupyter Notebook, which will then produce Next Day VWAP graphs.
3. The VWAP graph will display ranges of where VWAP might land tomorrow with its probabilities.
4. Any valid stocks' ticker from yfinance API could be used.
5. Due to trying on obtaining precise VWAP calculations, 5 minutes interval historical data is being used and yFinance API only allows maximum of 60 days historical data.
6. These VWAP model graphs can then be consumed to help with investment decisions (this is not a financial advice).

## Credits and links
- What is VWAP and its formula: [Investopedia VWAP](https://www.investopedia.com/terms/v/vwap.asp)
- Inverse of CDF formula: [CFI Excel NORMINV](https://corporatefinanceinstitute.com/resources/excel/norminv-function/) and [StackOverFlow NORMSINV](https://stackoverflow.com/questions/20626994/how-to-calculate-the-inverse-of-the-normal-cumulative-distribution-function-in-p)
- Modelling with Monte Carlo: [BI Excel](https://www.youtube.com/watch?v=wKdmEXCvo9s&list=LL&index=1)

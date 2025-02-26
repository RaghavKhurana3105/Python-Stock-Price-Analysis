# Stock price analysis CLI using Python
All stock prices have been downloaded from [Nasdaq](https://www.nasdaq.com/market-activity/quotes/historical). 
- **main.py** Contains all the logic for the command line interface calls.
- **stocks.py** Contains all the logic for reading the data/symbols.csv files, process them and plot them.
- **data folder** Contains csv files for each symbol available. Each file has up to 10 years of historical data.

Major libraries used for data analysis: **MatplotLib, Pandas, Numpy**

## Features
### ✅ Stock Data Processing

Reads stock data from CSV files
Cleans and preprocesses price and volume data
Computes percentage price changes over different time intervals (5yr, 1yr, 6m, 3m, etc.)

### ✅ Data Visualization

Candlestick Charts: Displays daily stock price movements (Open, Close, High, Low) with volume bars
Time-Series Plots: Plots stock performance over time for multiple stocks
Performance Table: Summarizes price change percentages for selected stocks

### ✅ Flexible Querying

Select specific stocks and time intervals
Filter stock data by date range
Sort and limit table output for better readability

## Usage Examples

```sh
python main.py --table symbol --limit 5
python main.py --table 3m --limit 5
python main.py --start 2023-01-01 --plot aapl goog meta
python main.py --start 2023-07-07 --plot all
python main.py --start 2024-03-01 --candle aapl
```

## Helpful Resources Links
- https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html
- https://matplotlib.org/stable/gallery/subplots_axes_and_figures/two_scales.html#sphx-glr-gallery-subplots-axes-and-figures-two-scales-py
- https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
- https://www.geeksforgeeks.org/how-to-create-a-candlestick-chart-in-matplotlib/
- https://pythonprogramming-nhl.github.io/PythonExerciseJupyterBook/pandas/pandas_exercises.html
- https://pythonprogramming-nhl.github.io/PythonExerciseJupyterBook/matplotlib/matplotlib_exercises.html




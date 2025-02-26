# Stock price analysis
All stock prices have been downloaded from [Nasdaq](https://www.nasdaq.com/market-activity/quotes/historical).
See the [assignment documentation on canvas](https://canvas.kth.se/courses/50052/files/8427785?module_item_id=931315)

## main.py
Contains all the logic for the command line interface calls

Some examples to run the file, (see the assignment documentation for examples on expected output).

```sh
python main.py --table symbol --limit 5
python main.py --table 3m --limit 5
python main.py --start 2023-01-01 --plot aapl goog meta
python main.py --start 2024-03-01 --candle aapl
```

## stocks.py
Contains all the logic for reading the data/symbols.csv files, process them and plot them.

## data 
Contains csv files for each symbol available. Each file has up to 10 years of historical data.


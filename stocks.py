import os
import glob
import copy
import pandas as pd
import numpy as np
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import csv

plt.rcParams["font.size"] = 14
plt.rcParams["axes.labelsize"] = 17
plt.rcParams["axes.titlesize"] = 17

# Headers for prices
PRICE_HEADERS = ["Close/Last", "Open", "High", "Low"]
DATE = "Date"
CLOSE = "Close/Last"
OPEN = "Open"
VOLUMES = "Volume"
SMA50 = "SM50"  # Simple Moving Average 50 days
SMA200 = "SMA200"  # Simple Moving Average 200 days

# Date constants
# Dataset ends at 06/06/2024, and referred to as 'today'
TODAY = pd.to_datetime("2024-06-06", format="%Y-%m-%d")

# Dictionary for the time intervals
TIMES = {
    "max": TODAY - pd.DateOffset(years=10),
    "5yr": TODAY - pd.DateOffset(years=5),
    "1yr": TODAY - pd.DateOffset(years=1),
    "6m": TODAY - pd.DateOffset(months=6),
    "3m": TODAY - pd.DateOffset(months=3),
    "2m": TODAY - pd.DateOffset(months=2),
    "1m": TODAY - pd.DateOffset(months=1),
    "2w": TODAY - pd.DateOffset(days=14),
    "1w": TODAY - pd.DateOffset(days=7),
}

class Stock:
    def __init__(self, filepath: str, symbol: str):
        """Constructor : sets the symbol name
        and reads+parses the given data filepath

        Args:
            filepath (str): File path to read stock data from
            symbol (str): Symbol signifying the stock name
        """
        self.__symbol = symbol
        self.__read_stock(filepath)
        self.__add_sma()

    def get_dataframe(self):
        return self.__df


    def __read_stock(self, filepath: str):
        """Reads the stock data from the given filepath (relative/absolute)
        and converts it into the proper data types.

        Args:
            filepath (str): path to read
        """
        # Read CSV into a Pandas DataFrame
        self.__df = pd.read_csv(filepath, parse_dates=[DATE])
        print(self.__df)

        # Remove "$" sign and convert price columns to float
        for price_header in PRICE_HEADERS:
            self.__df[price_header] = self.__df[price_header].replace({'\$': ''}, regex=True).astype(float)

        # Sort data in descending order by date (most recent first)
        self.__df = self.__df.sort_values(by=DATE, ascending=False)


    def __add_sma(self):
        # Not implemented yet
        pass

    def change_since(self, since: datetime) -> float:
        # Not implemented yet
        pass

    def get_date_range(self, start: datetime = None, end: datetime = None):
        """Extracts a bounded dataframe from the Stock object itself with data that is limited to the provided 
        start & end dates from CLI

        If start or end dates are not given, then no filtering is applied on the Stock Object

        Args:
            start (datetime, optional): Start date of the data to return. If None, no limit
            end (datetime, optional): End date of the data to return. If None, no limit.

        Returns:
            Dataframe: Returns a pandas dataframe object with the data bounded with the provided start & end dates.

        Raises:
            ValueError: Raised when provided end date is same as start date OR provided end date is before the start date 
        """
        if end == None:
            end = TODAY
        else:
            end = datetime.strptime(end, "%Y-%m-%d")

        if start == None:
            start = TIMES["max"]
        else:
            start = datetime.strptime(start, "%Y-%m-%d")
        
        if ((end < start) or (end == start)):
            raise ValueError

        limited_dates_df = self.get_dataframe()[self.get_dataframe().Date.between(start, end)]
        
        return limited_dates_df
        
    @property
    def symbol(self) -> str:
        return self.__symbol


class StocksDB:
    def __init__(self, path: str):
        """Reads in all csv files in a path"""
        self.__stocks = {}
        self.read_files(path)

    def read_files(self, path: str):
        """Reads all the csv files in the given path.
        Each will be stored as a {symbol : Stock} in the __stocks attribute.

        Args:
            path (str): relative or absolute path to the stocks directory.
        """
        # Loop over all csv files in the provided path
        for filename in glob.glob(os.path.join(path, "*.csv")):
            symbol = os.path.basename(filename).replace(".csv", "")  # Example: extracts "aapl" from "data/aapl.csv"
            self.__stocks[symbol] = Stock(filepath=filename, symbol=symbol)  # Stores unique Stock object           

    def __getitem__(self, name: str) -> Stock:
        """Getter method for accessing stocks in the
        stocks database created

        Args:
            name (str): symbol name of stock

        Returns:
            Stock: the required Stock object
        """
        try:
            return self.__stocks[name]
        except KeyError:
            logging.error(f"key [{name}] not found")
            return None

    def __iter__(self):
        """Implements the iterator to loop over all the stocks"""
        for stock in self.__stocks.values():
            yield stock


class Plot:
    def __init__(self, db: StocksDB, start: datetime = None, end: datetime = None):

        # Set internal attributes
        self.__db = db
        self.__start = start
        self.__end = end
        

    def candlestick(self, symbol: str):
        """Generate a Candlestick plot of the given symbol name, for
        the time period specified by thr optional start and end date provided through a CLI

        Args:
            symbol (str): Stock symbol name to plot
        """
        fig, ax1 = plt.subplots(figsize=(14, 6))

        # for candlestick
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Daily Price Range [$]',color='orange')

        plt.grid()
        limited_dates_df = self.__db[symbol].get_date_range(self.__start,self.__end)

        plt.ylim(0, max(limited_dates_df['Close/Last']) * 2.5)

        # store increasing and decreasing stock(s) in seperate dataframes
        up_df = limited_dates_df[limited_dates_df["Close/Last"] >= limited_dates_df["Open"]] 
        down_df = limited_dates_df[limited_dates_df["Close/Last"] <= limited_dates_df["Open"]]

        x_up = up_df['Date']
        x_down = down_df['Date']

        #candlestick bar body appearance parameters
        decrease_colour = 'red'  
        increase_colour = 'green' 
        body_width = .5   
        wick_width = .03 

        #candlestick bar specifications
        ax1.bar(x_up, up_df['Close/Last'], body_width, bottom=up_df['Open'], color=increase_colour)
        ax1.bar(x_up, up_df['High'], wick_width, bottom=up_df['Close/Last'], color=increase_colour)
        ax1.bar(x_up, up_df['Open'], wick_width, bottom=up_df['Low'], color=increase_colour)

        ax1.bar(x_down, down_df['Close/Last'], body_width, bottom=down_df['Open'], color=decrease_colour)  
        ax1.bar(x_down, down_df['High'], wick_width, bottom=down_df['Close/Last'], color=decrease_colour)
        ax1.bar(x_down, down_df['Open'], wick_width, bottom=down_df['Low'], color=decrease_colour)

        #volume bar graph(s) specifications
        ax2 = ax1.twinx()  # ax2 is the second axes that shares x-axis from ax1
        ax2.set_ylabel('Volume', color='blue') 
        ax2.bar(limited_dates_df['Date'],limited_dates_df['Volume'],body_width, color='blue') 
        ax2.set_ylim(0, max(limited_dates_df['Volume']) * 5)

        # Overall graph specifications
        plt.title(symbol)
        plt.legend()
        plt.show()  


    def plot(self, symbols: list[str]):
        """Plots closing price for all chosen stocks in StockDB through the CLI, for
        the time period specified by thr optional start and end date provided through a CLI

        Args:
            symbols (list[str]): List of symbol names
        """
        plt.figure(figsize=(14, 6))
        plt.xlabel(DATE)
        plt.ylabel('Closing Price [$]')
        plt.grid()

        for symbol in symbols:
            x = self.__db[symbol].get_date_range(self.__start,self.__end)['Date']
            plt.plot(x, self.__db[symbol].get_date_range(self.__start,self.__end)['Close/Last'],label=symbol)
        
        # Grid and legend
        plt.grid(True)
        plt.title("Time Series Plot for Stocks")
        plt.legend()

        # Show the plot
        plt.show()

    def plot_all(self):
        """Plots closing price for all existing stocks in StockDB,
        for the time period specified by thr optional start and end date provided through a CLI
        """
        plt.figure(figsize=(14, 6))
        plt.xlabel(DATE)
        plt.ylabel('Closing Price [$]')
        plt.grid()

        for stock in self.__db:
            x = stock.get_date_range(self.__start,self.__end)['Date']
            plt.plot(x, stock.get_date_range(self.__start,self.__end)['Close/Last'],label=stock.symbol)

        # Grid and legend
        plt.grid(True)
        plt.title("Time Series Plot for Stocks")
        plt.legend()

        # Show the plot
        plt.show()


class Table:
    def __init__(self, db: StocksDB):
        self.__db = db
        pass

class Table:
    def __init__(self, db: StocksDB):
        self.__db = db

    def print(self, sort_by: str = "symbol", limit: int = None):
        """Prints table of different companies showing their price development stats for 5yr, 1yr, 6m(months), 3m, 2m, 1m, 2w and 1w

        Args:
            sort_by (str): sorting key for data, default = symbol
            limit (int): Number of stocks to print, default = None, then all stocks are printed
        """
        table = []

        for key, stock in self.__db._StocksDB__stocks.items():  # Loop over all stocks
            stock_data = {} 
            stock_data["name"] = key  # Stock symbol

            # Get ending price (most recent)
            ending_price = stock.get_dataframe().iloc[0][CLOSE]

            # Compute price changes for each time period
            for time_key, time_value in TIMES.items():
                start_date = time_value
                filtered_df = stock.get_dataframe().loc[stock.get_dataframe()[DATE] <= start_date]

                if not filtered_df.empty:
                    closest_date_index = filtered_df[DATE].idxmax()  # Get the closest valid date
                    start_price = stock.get_dataframe().loc[closest_date_index, OPEN]

                    print(f"Stock: {stock.symbol}, {time_key} Start Price: {start_price}, End Price: {ending_price}")
                    stock_data[time_key] = ((ending_price - start_price) / start_price) * 100
                else:
                    stock_data[time_key] = None

            # Ensure missing values are set to 0.00
            for time_key in TIMES.keys():
                if time_key not in stock_data or stock_data[time_key] is None:
                    stock_data[time_key] = 0.00  # Or use "N/A"

            # Append the stock's data to the table
            table.append(stock_data)  

        # Sort data in table
        descending = True
        if sort_by == "symbol": 
            descending = False

        table.sort(key=lambda stock: stock["name"] if sort_by == "symbol" else stock[sort_by], reverse=descending)

        # Limit number of rows in table
        if limit is not None:
            table = table[:limit]

        # Print the results
        print(f'{"name":<6} {"Max":>8} {"5yr":>8} {"1yr":>7} {"6m":>7} {"3m":>7} {"2m":>7} {"1m":>7} {"2w":>7} {"1w":>7}')
        
        for stock in table:
            print(f'{stock["name"]:<6s} {stock["max"]:>8.2f} {stock["5yr"]:>8.2f} {stock["1yr"]:>7.2f} {stock["6m"]:>7.2f} {stock["3m"]:>7.2f} {stock["2m"]:>7.2f} {stock["1m"]:>7.2f} {stock["2w"]:>7.2f} {stock["1w"]:>7.2f}')

        

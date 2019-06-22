'''

pricecollection_alphavantage.py

A wrapper function to collect (and save) daily adjusted pricing data for a watchlist
of public stock.

Developer: Michael Browne
Email: mikelcbrowne@gmail.com

'''

import os
import pandas as pd
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
from tqdm import tqdm
import io


class UpdatePriceData:
    def __init__(self, ticker_list, api_key, fpath=None):
        self.ticker_list = ticker_list
        self.ts = TimeSeries(key=api_key, output_format='pandas', indexing_type='date')
        self.df = pd.DataFrame()

        self.get_new_data_multiple_stock()

        if fpath is not None:
            try:
                self.df.to_csv(fpath)
            except Exception as e:
                print(str(e))

    def get_new_data_single_stock(self, ticker):
        data, _ = self.ts.get_daily_adjusted(ticker.upper(), outputsize="full")

        return data["5. adjusted close"]

    def get_new_data_multiple_stock(self):
        # for ticker in tqdm(self.ticker_list):
        for ticker in self.ticker_list:
            try:
                self.df[ticker] = self.get_new_data_single_stock(ticker)
            except Exception as e:
                pass


if __name__ == "__main__":
    with open("../AlphaVantageAPI.txt", "r") as doc:
        api_key = doc.read()

    nasdaq_watchlist = pd.read_csv("../Data/watchlist_nasdaq_feb262019.csv")
    nasdaq_watchlist.columns = ["CompanyName", "Ticker", "MarketCap", "Sector", "Exchange"]

    # Choose a subset of the companies
    watchlist_in_scope = nasdaq_watchlist.loc[nasdaq_watchlist.MarketCap.between(500, 5000, inclusive=True)]

    tickers = list(watchlist_in_scope.Ticker.values)

    updater = UpdatePriceData(tickers, api_key, "../Data/stock_prices_asof_2019-06-21.csv")
import yfinance as yf
import pandas as pd

def get_corr_matrix(stocks, time_period):
    for stock in stocks:
        temp_ticker = yf.Ticker(stock)
        df[stock] = temp_ticker.history(period = time_period).loc[:, "Close"]

    return(df.corr())

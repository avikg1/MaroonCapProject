import yfinance as yf
import pandas as pd

def get_basic_matrix(stocks, time_period):
    df = pd.DataFrame()
    df.index = yf.Ticker(stocks[0]).history(period = time_period).index
    for stock in stocks:
        temp_ticker = yf.Ticker(stock)
        df[stock] = temp_ticker.history(period = time_period).loc[:, "Close"]
    return(df)

def get_corr_matrix(stocks, time_period):
    df = get_basic_matrix(stocks, time_period)
    return(df.corr())

def get_long_df(stocks, total_time, period_time):
    df = get_basic_matrix(stocks, total_time)
    resampled_df = df.resample(period_time).mean()
    df_long = resampled_df.reset_index().melt(id_vars = ["Date"], var_name = "Ticker", value_name = "Price")
    df_long.set_index("Date", inplace = True)
    return(df_long)

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
    print(df)
    start_price = df.resample(period_time).first().rename(lambda x: x + ' start', axis = 'columns')
    end_price = df.resample(period_time).last().rename(lambda x: x + ' end', axis = 'columns')

    resampled_df = pd.concat([start_price, end_price], axis=1).reset_index()
    

    melted = resampled_df.melt(id_vars='Date', var_name='Metric and Period', value_name='Value')
    
    melted[['Metric', 'Period']] = melted['Metric and Period'].str.rsplit(' ', n=1, expand=True)
    
    melted = melted.drop(columns=['Metric and Period'])
    final = melted.pivot_table(index=['Date', 'Metric'], columns='Period', values='Value').reset_index()
    return final

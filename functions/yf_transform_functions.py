import yfinance as yf
import pandas as pd

def get_basic_matrix(stocks, start_date, end_date):
    series_list = []
    index_set = False
    valid_stocks = []  # Keep track of valid stocks

    for stock in stocks:
        temp_ticker = yf.Ticker(stock)
        try:
            temp_history = temp_ticker.history(start=start_date, end=end_date)
            if not temp_history.empty and 'Close' in temp_history.columns:
                close_series = temp_history["Close"].rename(stock)
                series_list.append(close_series)
                valid_stocks.append(stock)  # Add to valid stocks list
                if not index_set:
                    index = temp_history.index
                    index_set = True
            else:
                raise ValueError(f"No valid data for {stock}, symbol may be delisted.")
        except Exception as e:
            print(f"Skipping {stock} due to error: {e}")

    if series_list:
        df = pd.concat(series_list, axis=1)
        if index_set:
            df.index = index
    else:
        df = pd.DataFrame(index=index if index_set else [])
    
    print(f"Valid stocks processed: {valid_stocks}")
    return df
    
    # Concatenate all series along the columns
    if series_list:
        df = pd.concat(series_list, axis=1, keys=[s.name for s in series_list])
        # Set the index if it was determined
        if index_set:
            df.index = index
    else:
        # Return an empty DataFrame with the appropriate index if no data was fetched
        df = pd.DataFrame(index=index if index_set else [])

    return df

def get_corr_matrix(stocks, start_date, end_date):
    df = get_basic_matrix(stocks, start_date, end_date)
    return(df.corr())

def get_long_df(stocks, start_date, end_date, period_time):
    df = get_basic_matrix(stocks, start_date, end_date)
    start_price = df.resample(period_time).first().rename(lambda x: x + ' start', axis = 'columns')
    end_price = df.resample(period_time).last().rename(lambda x: x + ' end', axis = 'columns')

    resampled_df = pd.concat([start_price, end_price], axis=1).reset_index()
    

    melted = resampled_df.melt(id_vars='Date', var_name='Stock and Period', value_name='Value')
    
    melted[['Stock', 'Period']] = melted['Stock and Period'].str.rsplit(' ', n=1, expand=True)
    
    melted = melted.drop(columns=['Stock and Period'])
    final = melted.pivot_table(index=['Date', 'Stock'], columns='Period', values='Value').reset_index()
    final.set_index('Date', inplace = True)
    final.index = final.index.tz_localize(None)

    return final

def fetch_stock_attributes(tickers, attributes):
    data = []
    for ticker in tickers:
        row = [ticker] + [None] * len(attributes)  # Pre-fill row with None
        try:
            temp_ticker = yf.Ticker(ticker)
            info = temp_ticker.info
            # Replace None with actual data if available
            for i, attribute in enumerate(attributes):
                row[i+1] = info.get(attribute, None)
        except Exception as e:
            print(f"An error occurred for {ticker}: {e}.")
        data.append(row)

    columns = ['Stock'] + attributes
    df = pd.DataFrame(data, columns=columns)
    return df

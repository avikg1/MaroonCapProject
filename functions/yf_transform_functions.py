import yfinance as yf
import pandas as pd

def get_basic_matrix(stocks, start_date, end_date):
    # Initialize an empty DataFrame
    df = pd.DataFrame()
    
    # Variable to track if the index has been set
    index_set = False
    
    for stock in stocks:
        temp_ticker = yf.Ticker(stock)
        try:
            # Attempt to fetch historical data for the given date range
            temp_history = temp_ticker.history(start=start_date, end=end_date)
            
            # If data is successfully fetched and the DataFrame is not empty
            if not temp_history.empty:
                # If the index hasn't been set yet, set it using the first successfully fetched stock
                if not index_set:
                    df.index = temp_history.index
                    index_set = True
                
                # Add the closing prices to the DataFrame
                df[stock] = temp_history["Close"]
        except Exception as e:
            # If an error occurs (e.g., ticker doesn't exist), skip this ticker
            print(f"Skipping {stock} due to error: {e}")
    
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
    # Initialize an empty list to store the data
    data = []
    
    # Iterate over each ticker
    for ticker in tickers:
        temp_ticker = yf.Ticker(ticker)
        info = temp_ticker.info
        
        # Fetch each attribute for the ticker, use None if the attribute is not found
        row = [info.get(attribute, None) for attribute in attributes]
        
        # Insert the ticker at the beginning of the row
        row.insert(0, ticker)
        
        # Append the row to the data list
        data.append(row)
    
    # Create a DataFrame from the data
    # The columns are the stock tickers plus the attributes
    columns = ['Stock'] + attributes
    df = pd.DataFrame(data, columns=columns)
    
    return df

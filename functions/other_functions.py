import pandas as pd
import numpy as np

def read_stock_tickers(filepath):
    tickers = []
    i = 0
    with open(filepath, 'r') as file:
        for line in file:
            i += 1
            if i > 10:
                break
            stripped = line.strip()
            if stripped not in tickers:
                tickers.append(line.strip())  # Remove any leading/trailing whitespace or newline chars
    return tickers


def transform_fed_data(filepath, start_date, end_date, period_time):
    df = pd.read_csv(filepath, parse_dates=['DATE'], index_col='DATE')
    
    # Filter the dataset for the specified date range
    mask = (df.index >= start_date) & (df.index <= end_date)
    filtered_df = df.loc[mask]
    
    # Resample and calculate means for the specified period
    resampled_df = filtered_df.resample(period_time).mean()

    resampled_df.index = resampled_df.index.tz_localize(None)

    return resampled_df

def calculate_fama_french_factors(df):
    results = []

    # Group the DataFrame by 'Date'
    grouped_by_date = df.groupby('Date')
    
    for date, group in grouped_by_date:
        # Calculate returns and market cap for the group
        total_market_cap = group['MarketCap'].sum()
        group['Weight'] = group['MarketCap'] / total_market_cap
        market_return = (group['Return'] * group['Weight']).sum()
        
        # Assign market cap and PE ratio ranks
        group['MarketCapRank'] = pd.qcut(group['MarketCap'], 2, labels=False)  # 0 is low, 1 is high
        group['PERank'] = pd.qcut(group['trailingPE'], [0, 0.3, 0.7, 1.0], labels=False)  # 0, 1, 2 for low, middle, high
        
        # Group by ranks within the date group and calculate weighted returns for each subgroup
        grouped_by_rank = group.groupby(['MarketCapRank', 'PERank'])
        portfolio_returns = grouped_by_rank.apply(lambda x: (x['Return'] * x['Weight']).sum())
        
        # Calculate SMB and HML for the group
        smb = (portfolio_returns.loc[0].mean() - portfolio_returns.loc[1].mean())
        hml = (portfolio_returns.loc[(slice(None), 0)].mean() - portfolio_returns.loc[(slice(None), 2)].mean())

        # Construct a dictionary for the results of the current date
        result = {
            'Date': date,
            'Market': market_return,
            'SMB': smb,
            'HML': hml
        }
        
        # Append the result to the results list
        results.append(result)
    
    return pd.DataFrame(results)


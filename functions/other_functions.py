import pandas as pd
import numpy as np

def read_stock_tickers(filepath):
    tickers = []
    with open(filepath, 'r') as file:
        for line in file:
            stripped = line.strip()
            if stripped not in tickers:
                tickers.append(stripped)
    return tickers

def annual_to_monthly_rate(annual_rate):
    return (1 + annual_rate) ** (1/12) - 1

def transform_fed_data(filepath, start_date, end_date, period_time, annualization_factor):
    df = pd.read_csv(filepath, parse_dates=['DATE'], index_col='DATE')
    
    # Filter the dataset for the specified date range
    mask = (df.index >= start_date) & (df.index <= end_date)
    filtered_df = df.loc[mask]
    
    # Resample and calculate means for the specified period
    resampled_df = filtered_df.resample(period_time).mean()

    resampled_df.index = resampled_df.index.tz_localize(None)
    resampled_df.iloc[:, 0] = resampled_df.iloc[:, 0].apply(annual_to_monthly_rate)

    return resampled_df

def calculate_fama_french_factors(df):
    results = []

    # Group the DataFrame by 'Date'
    grouped_by_date = df.groupby('Date')
    
    for date, group in grouped_by_date:
        valid_group = group.replace([np.inf, -np.inf], np.nan).dropna(subset=['Return', 'MarketCap', 'trailingPE'])
        # Calculate returns and market cap for the group
        total_market_cap = valid_group['MarketCap'].sum()
        valid_group['Weight'] = valid_group['MarketCap'] / total_market_cap
        market_return = (valid_group['Return'] * valid_group['Weight']).sum()
        
        # Assign market cap and PE ratio ranks
        valid_group['MarketCapRank'] = pd.qcut(valid_group['MarketCap'], 2, labels=False)  # 0 is low, 1 is high
        valid_group['PERank'] = pd.qcut(valid_group['trailingPE'], [0, 0.3, 0.7, 1.0], labels=False)  # 0, 1, 2 for low, middle, high
        
        # Group by ranks within the date group and calculate weighted returns for each subgroup
        grouped_by_rank = valid_group.groupby(['MarketCapRank', 'PERank'])
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


import pandas as pd
import numpy as np

def read_stock_tickers(filepath):
    tickers = []
    with open(filepath, 'r') as file:
        for line in file:
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
    # Calculate returns and market cap
    df['Return'] = (df['end'] - df['start']) / df['start']
    df['MarketCap'] = df['start'] * df['impliedSharesOutstanding']
    
    # Calculate Market Return as weighted average of returns by market cap
    total_market_cap = df['MarketCap'].sum()
    df['Weight'] = df['MarketCap'] / total_market_cap
    market_return = (df['Return'] * df['Weight']).sum()
    
    # Assign market cap and PE ratio ranks
    df['MarketCapRank'] = pd.qcut(df['MarketCap'], 2, labels=False)  # 0 is low, 1 is high
    df['PERank'] = pd.qcut(df['trailingPE'], [0, 0.3, 0.7, 1.0], labels=False)  # 0, 1, 2 for low, middle, high
    
    # Group by ranks and calculate weighted returns for each group
    grouped = df.groupby(['MarketCapRank', 'PERank'])
    portfolio_returns = grouped.apply(lambda x: (x['Return'] * x['Weight']).sum())
    
    # Calculate SMB and HML
    smb = (portfolio_returns.loc[0].mean() - portfolio_returns.loc[1].mean())
    hml = (portfolio_returns.loc[(slice(None), 0)].mean() - portfolio_returns.loc[(slice(None), 2)].mean())
    
    # Prepare the output DataFrame
    output_df = pd.DataFrame({
        'Date': df['Date'].unique(),
        'Market': [market_return],
        'SMB': [smb],
        'HML': [hml],
        'Risk_Free': [df['TB3MS'].iloc[0]],
        'Long_Interest': [df['FEDFUNDS'].iloc[0]]
    })
    
    # Add a column for each distinct stock with its return
    for stock in df['Stock'].unique():
        output_df[stock] = df[df['Stock'] == stock]['Return'].iloc[0]
    
    return output_df


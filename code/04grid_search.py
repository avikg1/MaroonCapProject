import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Set the working directory
# In Python, this can be done with os.chdir, but it's often unnecessary. Just specify the full or relative path when loading files.

# Gathering data
long_interest = pd.read_csv("clean/cleaned_ten_year_rate.csv")
train_dates = pd.read_csv("clean/train_data.csv")
price_data = pd.read_csv("raw/raw_data.csv")
market_return = pd.read_csv("clean/cleaned_data.csv")[["Date", "Market", "Risk_Free"]]

# Functions
def calculate_period_profits(data_frame, buy_list, sell_list):
    data_frame = data_frame[data_frame['Stock'].isin(buy_list + sell_list)]
    data_frame['profit'] = np.where(data_frame['Stock'].isin(buy_list) & data_frame['is_high_int'], 1000 / data_frame['start'] * (data_frame['end'] - data_frame['start']),
                                    np.where(data_frame['Stock'].isin(sell_list) & ~data_frame['is_high_int'], 1000 / data_frame['start'] * (data_frame['end'] - data_frame['start']), 0))
    profit_df = data_frame.groupby('Date').agg({'profit': 'sum'})
    profit_df['return'] = profit_df['profit'] / (1000 * len(buy_list))
    return profit_df

def calculate_sharpe_ratio(df, market):
    merged_df = pd.merge(df, market, on="Date")
    merged_df['Excess_Return'] = merged_df['return'] - merged_df['Risk_Free']
    sharpe_ratio = merged_df['Excess_Return'].mean() / merged_df['Excess_Return'].std()
    return sharpe_ratio

def calculate_alpha(df, market):
    merged_df = pd.merge(df, market, on="Date")
    merged_df['Portfolio_Excess_Return'] = merged_df['return'] - merged_df['Risk_Free']
    merged_df['Market_Excess_Return'] = merged_df['Market'] - merged_df['Risk_Free']
    model = ols("Portfolio_Excess_Return ~ Market_Excess_Return", data=merged_df).fit()
    print(model.summary())
    return {'alpha': model.params[0], 'beta': model.params[1]}

# Define the parameter ranges
n_range = np.arange(0, 0.5, 0.05)
HML_weight_range = np.arange(0, 1, 0.1)
buy_threshold_range = np.arange(0.5, 2, 0.1)

# Initialize variables to store the best Sharpe Ratio and corresponding parameters
best_sharpe_ratio = float('-inf')
best_params = {'n': None, 'HML_weight': None, 'buy_threshold': None}

for n in n_range:
    for HML_weight in HML_weight_range:
        for buy_threshold in buy_threshold_range:
            # Code
            regression_results = pd.read_csv("clean/BIGGESTWIN.csv")
            regression_results['sum'] = regression_results['SMB_interaction'] * (1 - HML_weight) + regression_results['HML_interaction'] * HML_weight
            regression_results = regression_results.sort_values(by='sum')

            # Calculate the number of rows to extract
            num_rows = len(regression_results)
            rows_to_extract = int(np.ceil(num_rows * n))  # Use np.ceil to round up to ensure at least one row is included

            # Extract the first 10% for the sell list and the last 10% for the buy list
            sell_list = regression_results['Stock'].iloc[:rows_to_extract].tolist()
            buy_list = regression_results['Stock'].iloc[-rows_to_extract:].tolist()

            above_av_months_df = long_interest[long_interest['FEDFUNDS'] > buy_threshold * long_interest['FEDFUNDS'].mean()]
            above_av_dates = above_av_months_df['DATE'].tolist()

            train_data = price_data[price_data['Date'].isin(train_dates['Date'])]
            train_data.loc[:, 'is_high_int'] = train_data['Date'].isin(above_av_dates)

            train_profits = calculate_period_profits(train_data, buy_list, sell_list)
            current_sharpe_ratio = calculate_sharpe_ratio(train_profits, market_return)
            
            # Check if the current Sharpe Ratio is the best one
            if current_sharpe_ratio > best_sharpe_ratio:
                best_sharpe_ratio = current_sharpe_ratio
                best_params['n'] = n
                best_params['HML_weight'] = HML_weight
                best_params['buy_threshold'] = buy_threshold

print(f"Best Sharpe Ratio: {best_sharpe_ratio}")
print(f"Best Parameters: n = {best_params['n']}, HML_weight = {best_params['HML_weight']}, buy_threshold = {best_params['buy_threshold']}")

import sys
import pandas as pd
import numpy as np
from check_user import DIR_PATH

sys.path.append(f"{DIR_PATH}/MaroonCapProject/functions") # Add functions module to the path

from yf_transform_functions import get_long_df
from yf_transform_functions import fetch_stock_attributes
from other_functions import transform_fed_data
from other_functions import calculate_fama_french_factors
from other_functions import read_stock_tickers

price_data = pd.read_csv(f"{DIR_PATH}/MaroonCapProject/raw/raw_data.csv", parse_dates=['Date'])


mcap_pe = pd.read_csv(f"{DIR_PATH}/MaroonCapProject/raw/raw_attributes.csv")

three_month_df = pd.read_csv(f"{DIR_PATH}/MaroonCapProject/clean/cleaned_three_month_rate.csv", parse_dates=['DATE'])
ten_year_df = pd.read_csv(f"{DIR_PATH}/MaroonCapProject/clean/cleaned_ten_year_rate.csv", parse_dates=['DATE'])

#do merges
merged_df = pd.merge(price_data, mcap_pe, left_on = "Stock", right_on = "Stock", how = "left")
# Replace 'None' with NaN for consistency in checks
merged_df.replace(to_replace=[None], value=np.nan, inplace=True)

# Drop rows where any of the specified attributes is NaN
attributes = ["trailingPE", "sharesOutstanding"]
merged_df = merged_df.dropna(subset= attributes)

merged_df.rename(columns = {"index": "Date"}, inplace = True)
print(merged_df)

#calculate return and market cap
merged_df['Return'] = (merged_df['end'] - merged_df['start']) / merged_df['start']
merged_df['MarketCap'] = merged_df['start'] * merged_df['sharesOutstanding']

#calculate fama-french factors
three_factors = calculate_fama_french_factors(merged_df)

#drop, merge, and pivot
pivoted_df = merged_df.pivot(index='Date', columns='Stock', values='Return').reset_index()
final = pd.merge(pivoted_df, three_factors, left_on = "Date", right_on = "Date", how = "left")
final = pd.merge(final, three_month_df, left_on= "Date", right_on= "DATE", how='left')
final = pd.merge(final, ten_year_df, left_on = "Date", right_on = "DATE", how='left').reset_index()
final.rename(columns = {"TB3MS": "Risk_Free", "FEDFUNDS": "Long_Rate"}, inplace = True)

final.to_csv(f"{DIR_PATH}/MaroonCapProject/clean/cleaned_data.csv")
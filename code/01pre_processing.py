import sys
import pandas as pd
import numpy as np

sys.path.append("/Users/avikgarg/repo/MaroonCapProject/functions") #have to change

from yf_transform_functions import get_long_df
from yf_transform_functions import fetch_stock_attributes
from other_functions import transform_fed_data
from other_functions import calculate_fama_french_factors
from other_functions import read_stock_tickers

START_DATE = "2009-01-01"
END_DATE = "2023-12-01"
GROUP_TIME_PERIOD = "M"

ticker_file = "/Users/avikgarg/repo/MaroonCapProject/raw/stockslist.txt" #have to change
STOCKS = read_stock_tickers(ticker_file)

"""
#pull price data
price_data = get_long_df(STOCKS, START_DATE, END_DATE, GROUP_TIME_PERIOD).reset_index()

price_data.to_csv("~/repo/MaroonCapProject/raw/raw_data.csv")
"""

price_data = pd.read_csv("~/repo/MaroonCapProject/raw/raw_data.csv", parse_dates=['Date'])

#Market Cap and P/E ratio

attributes = ["trailingPE", "sharesOutstanding"]

"""
mcap_pe = fetch_stock_attributes(STOCKS, attributes)
mcap_pe.to_csv("~/repo/MaroonCapProject/raw/raw_attributes.csv")
"""

mcap_pe = pd.read_csv("~/repo/MaroonCapProject/raw/raw_attributes.csv")

#FRED Data
three_month_path = "~/repo/MaroonCapProject/raw/three_month_rate.csv"
ten_year_path = "~/repo/MaroonCapProject/raw/ten_year_rate.csv"

three_month_df = transform_fed_data(three_month_path, START_DATE, END_DATE,
    GROUP_TIME_PERIOD)
ten_year_df = transform_fed_data(ten_year_path, START_DATE, END_DATE,
    GROUP_TIME_PERIOD)

#do merges
merged_df = pd.merge(price_data, mcap_pe, left_on = "Stock", right_on = "Stock", how = "left")
# Replace 'None' with NaN for consistency in checks
merged_df.replace(to_replace=[None], value=np.nan, inplace=True)

# Drop rows where any of the specified attributes is NaN
merged_df = merged_df.dropna(subset= attributes)

merged_df.rename(columns = {"index": "Date"}, inplace = True)
print(merged_df)

#calculate return and market cap
merged_df['Return'] = (merged_df['end'] - merged_df['start']) / merged_df['start']
merged_df['MarketCap'] = merged_df['start'] * merged_df['sharesOutstanding']

#calculate fama-french factors
three_factors = calculate_fama_french_factors(merged_df)

#drop, merge, and pivot
#merged_df.drop(["end", "start", "impliedSharesOutstanding"], axis = 1)
pivoted_df = merged_df.pivot(index='Date', columns='Stock', values='Return').reset_index()
final = pd.merge(pivoted_df, three_factors, left_on = "Date", right_on = "Date", how = "left")
final = pd.merge(final, three_month_df, left_on= "Date", right_index=True, how='left')
final = pd.merge(final, ten_year_df, left_on = "Date", right_index=True, how='left').reset_index()
final.rename(columns = {"TB3MS": "Risk_Free", "FEDFUNDS": "Long_Rate"}, inplace = True)

final.to_csv("~/repo/MaroonCapProject/clean/cleaned_data.csv")
import sys
import pandas as pd
import numpy as np

sys.path.append("/Users/avikgarg/repo/MaroonCapProject/functions")

from yf_transform_functions import get_long_df
from yf_transform_functions import fetch_stock_attributes
from other_functions import transform_fed_data
from other_functions import calculate_fama_french_factors

START_DATE = "2022-11-01"
END_DATE = "2024-01-01"
GROUP_TIME_PERIOD = "M"
STOCKS = ["MSFT", "AAPL", "GOOG", "META"]

#pull price data
price_data = get_long_df(STOCKS, START_DATE, END_DATE, GROUP_TIME_PERIOD)
print("price data:", price_data)

#Market Cap and P/E ratio
mcap_pe = fetch_stock_attributes(STOCKS, ["trailingPE", "impliedSharesOutstanding"])
print("mcap pe:", mcap_pe)

#FRED Data
three_month_path = "~/repo/MaroonCapProject/raw/three_month_rate.csv"
ten_year_path = "~/repo/MaroonCapProject/raw/ten_year_rate.csv"

three_month_df = transform_fed_data(three_month_path, START_DATE, END_DATE,
    GROUP_TIME_PERIOD)
ten_year_df = transform_fed_data(ten_year_path, START_DATE, END_DATE,
    GROUP_TIME_PERIOD)

print("10 year:", ten_year_df)
print("3 month:", three_month_df)


#do merges
merged_df = pd.merge(price_data, three_month_df, left_index=True, right_index=True, how='left')
merged_df = pd.merge(merged_df, ten_year_df, left_index=True, right_index=True, how='left').reset_index()
merged_df = pd.merge(merged_df, mcap_pe, left_on = "Stock", right_on = "Stock", how = "left")
merged_df.rename(columns = {"index": "Date"}, inplace = True)

print("merged df:", merged_df)

#calculate fama-french factors

cleaned_df = calculate_fama_french_factors(merged_df)
print("final:", cleaned_df)
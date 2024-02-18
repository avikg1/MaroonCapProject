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

START_DATE = "2009-01-01"
END_DATE = "2023-12-01"
GROUP_TIME_PERIOD = "M"
PERIOD_OVER_YEAR = 1/12

#FRED Data
three_month_path = f"{DIR_PATH}/MaroonCapProject/raw/three_month_rate.csv"
ten_year_path = f"{DIR_PATH}/MaroonCapProject/raw/ten_year_rate.csv"

three_month_df = transform_fed_data(three_month_path, START_DATE, END_DATE,
    GROUP_TIME_PERIOD, PERIOD_OVER_YEAR)
ten_year_df = transform_fed_data(ten_year_path, START_DATE, END_DATE,
    GROUP_TIME_PERIOD, PERIOD_OVER_YEAR)

three_month_df.to_csv(f"{DIR_PATH}/MaroonCapProject/clean/cleaned_three_month_rate.csv")
ten_year_df.to_csv(f"{DIR_PATH}/MaroonCapProject/clean/cleaned_ten_year_rate.csv")


ticker_file = f"{DIR_PATH}/MaroonCapProject/raw/stockslist.txt"
STOCKS = read_stock_tickers(ticker_file)
#pull price data
price_data = get_long_df(STOCKS, START_DATE, END_DATE, GROUP_TIME_PERIOD).reset_index()

price_data.to_csv(f"{DIR_PATH}/MaroonCapProject/raw/raw_data.csv")


#Market Cap and P/E ratio

attributes = ["trailingPE", "sharesOutstanding"]


mcap_pe = fetch_stock_attributes(STOCKS, attributes)
mcap_pe.to_csv(f"{DIR_PATH}/MaroonCapProject/raw/raw_attributes.csv")
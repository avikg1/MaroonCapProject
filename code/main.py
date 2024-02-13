import sys
sys.path.append("/Users/avikgarg/repo/MaroonCapProject/functions")

from yf_transform_functions import get_long_df

TOTAL_TIME_PERIOD = "1mo"
GROUP_TIME_PERIOD = "7D"
STOCKS = ["MSFT", "AAPL"]

df = get_long_df(STOCKS, TOTAL_TIME_PERIOD, GROUP_TIME_PERIOD)
print(df)
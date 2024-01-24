import yfinance as yf
import pandas as pd

#collect returns and PE ratio
PE_ratio = {}
returns_df = pd.DataFrame()

for stock in stocks:
    temp = yf.Ticker(stock)
    PE_ratio[stock] = temp.getinfo["trailingPE"]
    returns_df[stock] = transform_returns(temp.history(period = time_period))

#collect interest rate data

#collect forward-looking interest rate data

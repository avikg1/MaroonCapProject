import numpy as np
import pandas as pd

time_period = "3M"

df = pd.read_csv("~/repo/MaroonCapProject/raw/ten_year_rate.csv",
    index_col=0,       # Tell Pandas that the first column should be used as an index
    parse_dates=[0]    # Tell Pandas to parse the column at index 0 as dates
                )
df = df.resample(time_period).mean()

df.to_csv("~/repo/MaroonCapProject/clean/cleaned_10_year.csv")

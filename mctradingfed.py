import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

time_period = "3M"

df = pd.read_csv('FEDFUNDS.csv',
    index_col=0,       # Tell Pandas that the first column should be used as an index
    parse_dates=[0]    # Tell Pandas to parse the column at index 0 as dates
                )
df = df.resample(time_period).mean()
print(df.to_string()) 
#change tickers as you please--I suggest using chat gpt to generate tickers if you want a bunch
#valid time periods are 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd


import sys
sys.path.insert(1, '~/repo/MaroonCapProject/Avik')

from get_corr_matrix import get_corr_matrix

time_period = "1y"
tickers = [
    "AAPL",  # Apple Inc.
    "MSFT",  # Microsoft Corporation
    "AMZN",  # Amazon.com, Inc.
    "GOOGL", # Alphabet Inc. (Class A)
    "GOOG",  # Alphabet Inc. (Class C)
    "FB",    # Meta Platforms, Inc. (formerly Facebook)
    "TSLA",  # Tesla, Inc.
    "BRK.B", # Berkshire Hathaway Inc. (Class B)
    "JPM",   # JPMorgan Chase & Co.
    "JNJ",   # Johnson & Johnson
    "V",     # Visa Inc.
    "PG",    # Procter & Gamble Company
    "UNH",   # UnitedHealth Group Incorporated
    "MA",    # Mastercard Incorporated
    "NVDA",  # NVIDIA Corporation
    "HD",    # Home Depot, Inc.
    "PYPL",  # PayPal Holdings, Inc.
    "BAC",   # Bank of America Corporation
    "DIS",   # Walt Disney Company
    "VZ",    # Verizon Communications Inc.
    "ADBE",  # Adobe Inc.
    "CMCSA", # Comcast Corporation
    "NFLX",  # Netflix, Inc.
    "KO",    # Coca-Cola Company
    "NKE",   # NIKE, Inc.
    "MRK",   # Merck & Co., Inc.
    "PEP",   # PepsiCo, Inc.
    "PFE",   # Pfizer Inc.
    "INTC",  # Intel Corporation
    "CSCO",  # Cisco Systems, Inc.
    "T",     # AT&T Inc.
    "XOM",   # Exxon Mobil Corporation
    "WMT",   # Walmart Inc.
    "ABBV",  # AbbVie Inc.
    "CVX",   # Chevron Corporation
    "MCD",   # McDonald's Corporation
    "MDT",   # Medtronic plc
    "ABT",   # Abbott Laboratories
    "BMY",   # Bristol-Myers Squibb Company
    "LLY",   # Eli Lilly and Company
    "UNP",   # Union Pacific Corporation
    "ORCL",  # Oracle Corporation
    "ACN",   # Accenture plc
    "MMM",   # 3M Company
    "IBM",   # International Business Machines Corporation
    "TXN",   # Texas Instruments Incorporated
    "HON",   # Honeywell International Inc.
    "QCOM",  # Qualcomm Incorporated
    "UPS",   # United Parcel Service, Inc.
    "SCHW",  # Charles Schwab Corporation
    "BLK",   # BlackRock, Inc.
]

print(get_corr_matrix(tickers, time_period))

import yfinance as yf
import pandas as pd

# arguments for API call
ticker = 'AAPL'
period = "1d"
interval = "1h"

# fetch
data = yf.download(ticker, period=period, interval=interval)

# export as csv
data.to_csv("stockdata.csv")
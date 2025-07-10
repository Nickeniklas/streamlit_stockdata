import yfinance as yf
import pandas as pd
import os

# arguments for API call
ticker = 'AAPL'
period = "1d"
interval = "1h"

# fetch
data = yf.download(ticker, period=period, interval=interval)

# output folder and pathfile name
folder = "stockdata"
os.makedirs(folder, exist_ok=True)  # Create the folder if it doesn't exist
filepath = os.path.join(folder, f"stockdata_{ticker}.csv")

# export as csv
data.to_csv(filepath)

print(f"Saved CSV as '{filepath}'")
from dotenv import load_dotenv
import requests 
import os
from twelvedata import TDClient
import pandas as pd

# get api key from .env file
load_dotenv()
api_key = os.getenv('TWELVE_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set TWELVE_API_KEY in .env")

# Create the folder if it doesn't exist
os.makedirs('stockdata', exist_ok=True)

# Initialize the Twelve Data client
td = TDClient(apikey=api_key)

symbols = ["AAPL", "MSFT", "GOOGL", "ORCL", "AMZN", "META", "NVDA"]  # list of symbols to fetch

# Fetching stock data for Apple Inc. (AAPL) as an example
for symbol in symbols:
    # Fetch the time series data for the specified symbol        
    ts = td.time_series(
        symbol=symbol,
        interval="1day",
        outputsize=90
    )
    
    # Convert to pandas DataFrame
    df = ts.as_pandas()

    # Save to CSV file
    df.to_csv(f'stockdata/stockdata_{symbol}.csv', index=True)

    print(f"Data saved to stockdata/stockdata_{symbol}.csv")


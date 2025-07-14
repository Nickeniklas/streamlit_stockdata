# Finnhub API
import finnhub
from dotenv import load_dotenv
import time
import requests
import os

# get api key from .env file
load_dotenv()
api_key = os.getenv('TWELVE_API_KEY')
if not api_key:
    raise ValueError("No API key found. Please set TWELVE_API_KEY in .env")
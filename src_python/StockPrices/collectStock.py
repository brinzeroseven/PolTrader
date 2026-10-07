import json
from pathlib import Path
import pandas as pd
import yfinance as yf
import os

RAW_DATA_DIR = Path("data/raw/stock_prices")

ticker_list = ['AMZN',
 'AAPL',
 'BRK-B', # yahoo finance uses BRK-B as apposed ot BRK.b
 'JNJ',
 'GOOGL',
 'MSFT',
 'META',
 'DELL',
 'SMCI',
 'NVDA',
 'UNH']

RAW_DATA_DIR.mkdir(parents=True,exist_ok=True)

for ticker in ticker_list:

    print(f"Downloading {ticker} stock data")

    df = yf.download(
        ticker,
        start="2016-01-01",
        end=None,
        interval="1d"
    )

    print(f"{ticker} downloaded with {len(df)} data") # realistcally len(df) should be about the same for all i think

    df.to_parquet(f"{RAW_DATA_DIR}/{ticker}.parquet")

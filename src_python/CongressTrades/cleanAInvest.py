import json
from pathlib import Path

import pandas as pd

RAW_DATA_DIR=Path("data/raw/AInvest/")
OUTPUT_FILE = Path("data/processed/tradesAInvestALL.parquet")

def load_ticker_trades(ticker_dir):
    tradesTicker = []

    for file in ticker_dir.glob("trades_page*.json"):
        with open(file) as f:
            tickerData = json.load(f)

        if tickerData["data"] is None:
            print(f"Skipping invalid file: {file}")
            continue

        tradesTicker.extend(tickerData["data"]["data"])

    return tradesTicker

def clean_trades(ticker_trades, ticker):
    ticker_df = pd.DataFrame(ticker_trades)

    # Convert dates
    ticker_df["filing_date"] = pd.to_datetime(ticker_df["filing_date"])
    ticker_df["trade_date"] = pd.to_datetime(ticker_df["trade_date"])

    ticker_df["ticker"] = ticker

    return ticker_df

def load_all_trades():
    tradesFull = []

    for ticker_dir in RAW_DATA_DIR.iterdir():
        if ticker_dir.is_dir():
            ticker = ticker_dir.name

            tradesTicker = load_ticker_trades(ticker_dir)
            tradesTickerClean = clean_trades(tradesTicker,ticker)
            
            tradesFull.append(tradesTickerClean)

    df = pd.concat(tradesFull, ignore_index=True)
    return df

def save_trades(df):
    df.to_parquet(OUTPUT_FILE,index=False)

    print(f"saved {len(df)} trades to {OUTPUT_FILE}")

if __name__ == "__main__":
    df = load_all_trades()
    save_trades(df)


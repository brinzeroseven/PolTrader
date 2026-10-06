import json
from pathlib import Path

import pandas as pd

RAW_DATA_DIR=Path("data/raw/AInvest/")
OUTPUT_FILE = Path("data/processed/tradesAInvest.parquet")

def load_raw_trades():
    trades = []

    for file in RAW_DATA_DIR.glob("trades_page*.json"):

        with open(file) as f:
            data = json.load(f)

        trades.extend(data["data"]["data"])

    return trades

def clean_trades(trades):
    df = pd.DataFrame(trades)

    # Convert dates
    df["filing_date"] = pd.to_datetime(df["filing_date"])
    df["trade_date"] = pd.to_datetime(df["trade_date"])

    return df

def save_trades(df):

    df.to_parquet(OUTPUT_FILE, index=False)

    print(f"Saved {len(df)} trades to {OUTPUT_FILE}")

if __name__ == "__main__":
    trades = load_raw_trades()
    df = clean_trades(trades)
    save_trades(df)
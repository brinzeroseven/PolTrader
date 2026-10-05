import json
from pathlib import Path

import pandas as pd

RAW_FILE = Path("data/trades_page_0.json")
OUTPUT_FILE = Path("data/trades.parquet")

def load_raw_trades():
    with open(RAW_FILE) as file:
        data = json.load(file)

    return data["trades"]

def clean_trades(trades):
    df = pd.DataFrame(trades)

    # Convert dates
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["disclosure_date"] = pd.to_datetime(df["disclosure_date"])
    df["recent_price_date"] = pd.to_datetime(df["recent_price_date"])

    # Calc disclosure delay
    df["disclosure_delay_days"] = (
        df["disclosure_date"] - df["transaction_date"]
    ).dt.days

    return df

def save_trades(df):
    df.to_parquet(OUTPUT_FILE, index=False)

    print(f"Saved {len(df)} trades to {OUTPUT_FILE}")

if __name__ == "__main__":
    trades = load_raw_trades()
    df = clean_trades(trades)
    save_trades(df)
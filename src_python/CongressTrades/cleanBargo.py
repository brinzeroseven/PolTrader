import json
from pathlib import Path
import pandas as pd

RAW_DATA_DIR = Path("data/raw/Bargo/")
OUTPUT_FILE = Path("data/processed/tradesBargo.parquet")

def load_raw_trades():
    trades = []

    for file in RAW_DATA_DIR.glob("trades_page*.json"):

        with open(file) as f:
            data = json.load(f)

        trades.extend(data["trades"])

    return trades

def clean_trades(trades):
    df = pd.DataFrame(trades)

    # Convert Dates (useless for now as likely are not to use bargo)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["disclosure_date"] = pd.to_datetime(df["disclosure_date"])
    df["recent_price_date"] = pd.to_datetime(df["recent_price_date"])

    return df

def save_trades(df):

    df.to_parquet(OUTPUT_FILE, index=False)

    print(f"Saved {len(df)} trades to {OUTPUT_FILE}")

if __name__ == "__main__":
    trades = load_raw_trades()
    df = clean_trades(trades)
    save_trades(df)


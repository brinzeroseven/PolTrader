import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv() # reads .env file

BASE_URL = "https://openapi.ainvest.com/open/ownership/congress"
API_KEY = os.getenv("AINVEST_API_KEY")

RAW_DATA_DIR = Path("data/raw/AInvest")

def fetch_trades(ticker="AAPL", size=100, page=1):
    # Fetch page of congress trades from bargo

    if not API_KEY:
        raise RuntimeError("AINVEST_API_KEY not found in .env")

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    params = {
        "ticker": ticker,
        "page": page,
        "size": size,
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status() # checks if https error

    return response.json()


def save_raw_data(data, page):

    # Save as json
    output_path = RAW_DATA_DIR / f"trades_page{page}.json"

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {output_path}")


if __name__ == "__main__":

    for page in range(6,10):

        data = fetch_trades(
            ticker="AAPL",
            size=100,
            page=page,
        )

        save_raw_data(data, page)
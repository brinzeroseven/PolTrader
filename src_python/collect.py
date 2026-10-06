import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv() # reads .env file

BASE_URL = "https://www.bargo.ai/free-apis/congress/v1"
API_KEY = os.getenv("BARGO_API_KEY")

RAW_DATA_DIR = Path("data/raw")

def fetch_trades(limit=250, page=0):
    # Fetch page of congress trades from bargo

    if not API_KEY:
        raise RuntimeError("BARGO_API_KEY not found in .env")

    response = requests.get(
        f"{BASE_URL}/trades",
        params={
            "limit": limit,
            "page": page,
        },
        headers={
            "Authorization": f"Bearer {API_KEY}",
        },
        timeout=30,
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

    for page in range(4):

        data = fetch_trades(
            limit=250,
            page=page
        )

        save_raw_data(data, page)

        if len(data["trades"]) < 250:
            break
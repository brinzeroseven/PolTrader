import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

BASE_URL = "https://www.bargo.ai/free-apis/congress/v1"
API_KEY = os.getenv("BARGO_API_KEY")

RAW_DATA_DIR = Path("data")

def fetch_trades(limit=100, page=0):
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

    response.raise_for_status()

    return response.json()


def save_raw_data(data, filename="trades_page_0.json"):
    # Save as json

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    output_path = RAW_DATA_DIR / filename

    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {output_path}")


if __name__ == "__main__":
    data = fetch_trades(limit=100)
    save_raw_data(data)
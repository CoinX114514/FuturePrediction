#!/usr/bin/env python3
"""从本地行情 JSON 打印铁矿石等合约现价（检查 MARKET_DATA_JSON）。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
except ImportError:
    pass


def main() -> None:
    from app.services.market_data_service import MarketDataService

    svc = MarketDataService()
    print("MARKET_DATA_JSON=", os.getenv("MARKET_DATA_JSON", "(默认 backend/data/market_data.json)"))
    for code in ("I2605", "I2603.DCE"):
        p = svc.get_futures_price(code)
        print(f"{code}: {p}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""强制更新库中所有帖子的现价。

从 Tushare 拉取各合约最新收盘价并写入 posts.current_price，
使详情页「现价」与 K 线图最后一根、主页列表保持一致。

用法（在 backend 目录下）:
  python force_update_prices.py

环境要求:
  - TUSHARE_TOKEN 已配置（.env 或环境变量）
  - DATABASE_URL 可连接
"""

import os
import sys

# 将项目根目录加入路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载 .env（TUSHARE_TOKEN、DATABASE_URL）
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass


def main():
    from app.database.connection import SessionLocal
    from app.services.price_update_service import PriceUpdateService

    print("正在强制更新库中所有帖子的现价（从 Tushare 拉取并写入 DB）...")
    db = SessionLocal()
    try:
        service = PriceUpdateService(db)
        result = service.update_all_posts_price()
        print(
            f"完成: 总数={result['total']}, "
            f"成功={result['success']}, 失败={result['failed']}"
        )
        if result.get("error"):
            print(f"错误: {result['error']}")
        return 0 if result.get("failed", 0) == 0 else 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())

"""数据库初始化脚本。

用于创建数据库表结构并初始化种子数据。
"""

from app.database.connection import init_db, engine, SessionLocal
from app.database import models
from app.database.seed_data import seed_database

if __name__ == "__main__":
    print("正在创建数据库表...")
    init_db()
    print("数据库表创建完成！")
    print(f"数据库连接: {engine.url}")
    
    # 初始化种子数据
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


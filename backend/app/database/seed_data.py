"""数据库种子数据。

用于初始化一些基础数据，如板块信息。
"""

from sqlalchemy.orm import Session
from app.database.models import Sector, FuturesContract

# 基础板块数据
INITIAL_SECTORS = [
    {"sector_code": "METAL", "sector_name": "金属", "sector_level": 1, "display_order": 1, "is_vip_only": False},
    {"sector_code": "ENERGY", "sector_name": "能源", "sector_level": 1, "display_order": 2, "is_vip_only": False},
    {"sector_code": "AGRICULTURE", "sector_name": "农产品", "sector_level": 1, "display_order": 3, "is_vip_only": False},
    {"sector_code": "CHEMICAL", "sector_name": "化工", "sector_level": 1, "display_order": 4, "is_vip_only": False},
    {"sector_code": "FINANCIAL", "sector_name": "金融", "sector_level": 1, "display_order": 5, "is_vip_only": False},
    {"sector_code": "STOCK_INDEX", "sector_name": "股指", "sector_level": 1, "display_order": 6, "is_vip_only": True},
]


def init_sectors(db: Session):
    """初始化板块数据。

    Args:
        db: 数据库会话。
    """
    for sector_data in INITIAL_SECTORS:
        # 检查是否已存在
        existing = db.query(Sector).filter(Sector.sector_code == sector_data["sector_code"]).first()
        if not existing:
            sector = Sector(**sector_data)
            db.add(sector)
    
    db.commit()
    print(f"已初始化 {len(INITIAL_SECTORS)} 个板块")


def seed_database(db: Session):
    """初始化所有种子数据。

    Args:
        db: 数据库会话。
    """
    print("开始初始化种子数据...")
    init_sectors(db)
    print("种子数据初始化完成！")


if __name__ == "__main__":
    from app.database.connection import SessionLocal
    
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


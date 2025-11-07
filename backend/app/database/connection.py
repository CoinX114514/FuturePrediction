"""数据库连接配置。

负责创建和管理数据库连接。
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# 数据库连接配置
# 从环境变量读取，如果没有则使用默认值
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/futures_trading"
)

# 创建数据库引擎
# 使用连接池提高性能
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 连接前检查连接是否有效
    echo=False,  # 设置为 True 可以打印 SQL 语句（用于调试）
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()


def get_db():
    """获取数据库会话。

    这是一个依赖注入函数，用于 FastAPI 路由中。

    Yields:
        Session: SQLAlchemy 数据库会话。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库。

    创建所有表结构。仅在首次部署时调用。
    """
    Base.metadata.create_all(bind=engine)


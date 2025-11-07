"""Pytest 配置和共享 fixtures。

提供测试数据库、测试客户端等共享资源。
"""

import os
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects import registry
from fastapi.testclient import TestClient

from app.database.connection import Base, get_db
from app.database.models import User
from app.main import app

# 测试数据库 URL（使用 SQLite 文件数据库，测试后删除）
TEST_DATABASE_URL = "sqlite:///./test.db"


# 为 SQLite 创建类型映射函数
def setup_sqlite_types():
    """设置 SQLite 类型映射，将 PostgreSQL 特定类型转换为 SQLite 兼容类型。"""
    from sqlalchemy import String, Integer, BigInteger
    from sqlalchemy.dialects.postgresql import INET, UUID as PG_UUID
    
    # 遍历所有表并修改列类型
    for table_name, table in Base.metadata.tables.items():
        for column in table.columns:
            # 将 INET 类型映射为 String
            if isinstance(column.type, INET):
                column.type = String(50)
            # 将 UUID 类型映射为 String
            elif isinstance(column.type, PG_UUID):
                column.type = String(36)
            # SQLite 不支持 BigInteger 的 autoincrement，改为 Integer
            elif isinstance(column.type, BigInteger) and column.primary_key and column.autoincrement:
                column.type = Integer()


@pytest.fixture(scope="function")
def test_db():
    """创建测试数据库会话。

    Yields:
        Session: 测试数据库会话。
    """
    # 设置 SQLite 类型映射
    setup_sqlite_types()
    
    # 删除旧的测试数据库文件（如果存在）
    if os.path.exists("test.db"):
        os.remove("test.db")
    
    # 创建测试数据库引擎
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False}  # SQLite 需要
    )
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 创建会话工厂
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建会话
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # 删除所有表
        Base.metadata.drop_all(bind=engine)
        # 删除测试数据库文件
        if os.path.exists("test.db"):
            os.remove("test.db")


@pytest.fixture(scope="function")
def client(test_db):
    """创建测试客户端。

    Args:
        test_db: 测试数据库会话。

    Yields:
        TestClient: FastAPI 测试客户端。
    """
    # 覆盖 get_db 依赖
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 清理依赖覆盖
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_normal(test_db):
    """创建测试普通用户。

    Args:
        test_db: 测试数据库会话。

    Returns:
        User: 普通用户对象。
    """
    from app.utils.password import hash_password
    
    user = User(
        phone_number="13800138000",
        email="test@example.com",
        password_hash=hash_password("test123456"),
        nickname="测试用户",
        user_role=1,  # 普通用户
        daily_prediction_limit=5,
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_user_member(test_db):
    """创建测试会员用户。

    Args:
        test_db: 测试数据库会话。

    Returns:
        User: 会员用户对象。
    """
    from app.utils.password import hash_password
    
    user = User(
        phone_number="13900139000",
        email="member@example.com",
        password_hash=hash_password("test123456"),
        nickname="会员用户",
        user_role=2,  # 会员
        daily_prediction_limit=999999,
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def test_user_admin(test_db):
    """创建测试管理员用户。

    Args:
        test_db: 测试数据库会话。

    Returns:
        User: 管理员用户对象。
    """
    from app.utils.password import hash_password
    
    user = User(
        phone_number="13700137000",
        email="admin@example.com",
        password_hash=hash_password("test123456"),
        nickname="管理员",
        user_role=3,  # 超级管理员
        daily_prediction_limit=999999,
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture
def auth_token_normal(client, test_user_normal):
    """获取普通用户的认证 Token。

    Args:
        client: 测试客户端。
        test_user_normal: 普通用户对象。

    Returns:
        str: JWT Token。
    """
    response = client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": test_user_normal.phone_number,
            "password": "test123456",
        }
    )
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def auth_token_member(client, test_user_member):
    """获取会员用户的认证 Token。

    Args:
        client: 测试客户端。
        test_user_member: 会员用户对象。

    Returns:
        str: JWT Token。
    """
    response = client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": test_user_member.phone_number,
            "password": "test123456",
        }
    )
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def auth_token_admin(client, test_user_admin):
    """获取管理员的认证 Token。

    Args:
        client: 测试客户端。
        test_user_admin: 管理员用户对象。

    Returns:
        str: JWT Token。
    """
    response = client.post(
        "/api/v1/auth/login",
        json={
            "phone_number": test_user_admin.phone_number,
            "password": "test123456",
        }
    )
    assert response.status_code == 200
    return response.json()["token"]


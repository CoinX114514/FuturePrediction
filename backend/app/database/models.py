"""数据库模型定义。

根据 README_DEV.md 的数据库设计定义所有表模型。
"""

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Boolean,
    Date,
    DateTime,
    Numeric,
    Text,
    ForeignKey,
    SmallInteger,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class User(Base):
    """用户表模型。

    对应数据库表：users
    """

    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True)
    phone_number = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    user_role = Column(SmallInteger, default=1)  # 1:普通用户 2:会员 3:超级管理员
    avatar_url = Column(String(500))
    nickname = Column(String(50))
    real_name = Column(String(50))
    prediction_count = Column(Integer, default=0)  # 已使用预测次数
    daily_prediction_limit = Column(Integer, default=5)  # 每日预测限制
    member_expire_time = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # 关系
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    prediction_tasks = relationship("PredictionTask", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, phone_number={self.phone_number}, role={self.user_role})>"


class UserSession(Base):
    """用户会话表模型。

    对应数据库表：user_sessions
    """

    __tablename__ = "user_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False, index=True)
    user_agent = Column(String(500))
    browser_name = Column(String(50))
    ip_address = Column(INET)
    expire_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return f"<UserSession(session_id={self.session_id}, user_id={self.user_id})>"


class Sector(Base):
    """板块表模型。

    对应数据库表：sectors
    """

    __tablename__ = "sectors"

    sector_id = Column(Integer, primary_key=True, autoincrement=True)
    sector_code = Column(String(20), unique=True, nullable=False, index=True)
    sector_name = Column(String(100), nullable=False)
    parent_sector_id = Column(Integer, ForeignKey("sectors.sector_id"), index=True)
    sector_level = Column(SmallInteger, default=1)
    display_order = Column(Integer, default=0)
    is_vip_only = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    parent = relationship("Sector", remote_side=[sector_id], backref="children")
    contracts = relationship("FuturesContract", back_populates="sector")

    def __repr__(self):
        return f"<Sector(sector_id={self.sector_id}, sector_code={self.sector_code}, sector_name={self.sector_name})>"


class FuturesContract(Base):
    """期货合约表模型。

    对应数据库表：futures_contracts
    """

    __tablename__ = "futures_contracts"

    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    contract_code = Column(String(20), unique=True, nullable=False, index=True)  # 如：IF2312
    contract_name = Column(String(100), nullable=False)
    exchange_code = Column(String(10), nullable=False, index=True)  # SHFE/DCE/CZCE/CFFEX
    underlying_asset = Column(String(50))
    contract_multiplier = Column(Numeric(10, 2))
    price_tick = Column(Numeric(10, 4))
    sector_id = Column(Integer, ForeignKey("sectors.sector_id"), index=True)
    is_active = Column(Boolean, default=True)
    listed_date = Column(Date)
    expiry_date = Column(Date)
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    sector = relationship("Sector", back_populates="contracts")
    market_data = relationship("MarketData", back_populates="contract", cascade="all, delete-orphan")
    prediction_tasks = relationship("PredictionTask", back_populates="contract")
    alerts = relationship("OpportunityAlert", back_populates="contract")

    def __repr__(self):
        return f"<FuturesContract(contract_id={self.contract_id}, contract_code={self.contract_code})>"


class MarketData(Base):
    """行情数据表模型。

    对应数据库表：market_data
    """

    __tablename__ = "market_data"

    data_id = Column(BigInteger, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("futures_contracts.contract_id", ondelete="CASCADE"), nullable=False, index=True)
    trade_date = Column(Date, nullable=False, index=True)
    open_price = Column(Numeric(12, 2))
    high_price = Column(Numeric(12, 2))
    low_price = Column(Numeric(12, 2))
    close_price = Column(Numeric(12, 2))
    settlement_price = Column(Numeric(12, 2))
    volume = Column(BigInteger)
    open_interest = Column(BigInteger)
    turnover = Column(Numeric(15, 2))
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    contract = relationship("FuturesContract", back_populates="market_data")

    # 唯一约束
    __table_args__ = (
        Index("unq_market_data_contract_date", "contract_id", "trade_date", unique=True),
    )

    def __repr__(self):
        return f"<MarketData(data_id={self.data_id}, contract_id={self.contract_id}, trade_date={self.trade_date})>"


class PredictionTask(Base):
    """预测任务表模型。

    对应数据库表：prediction_tasks
    """

    __tablename__ = "prediction_tasks"

    task_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    user_id = Column(BigInteger, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    contract_id = Column(Integer, ForeignKey("futures_contracts.contract_id"), index=True)
    prediction_type = Column(String(20), default="kronos_daily")
    prediction_horizon = Column(Integer, default=1)  # 预测步长(天)
    prediction_paths = Column(Integer, default=10)  # 路径数量
    status = Column(String(20), default="pending", index=True)  # pending/processing/completed/failed
    created_at = Column(DateTime, server_default=func.now())
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    # 关系
    user = relationship("User", back_populates="prediction_tasks")
    contract = relationship("FuturesContract", back_populates="prediction_tasks")
    results = relationship("PredictionResult", back_populates="task", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<PredictionTask(task_id={self.task_id}, user_id={self.user_id}, status={self.status})>"


class PredictionResult(Base):
    """预测结果表模型。

    对应数据库表：prediction_results
    """

    __tablename__ = "prediction_results"

    result_id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(UUID(as_uuid=True), ForeignKey("prediction_tasks.task_id", ondelete="CASCADE"), nullable=False, index=True)
    prediction_date = Column(Date, nullable=False, index=True)
    path_number = Column(Integer, default=1)
    predicted_price = Column(Numeric(12, 2))
    upper_bound = Column(Numeric(12, 2))  # 置信区间上界
    lower_bound = Column(Numeric(12, 2))  # 置信区间下界
    confidence_level = Column(Numeric(5, 2))  # 置信度百分比
    created_at = Column(DateTime, server_default=func.now())

    # 关系
    task = relationship("PredictionTask", back_populates="results")

    def __repr__(self):
        return f"<PredictionResult(result_id={self.result_id}, task_id={self.task_id}, prediction_date={self.prediction_date})>"


class OpportunityAlert(Base):
    """机会提醒表模型。

    对应数据库表：opportunity_alerts
    """

    __tablename__ = "opportunity_alerts"

    alert_id = Column(BigInteger, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("futures_contracts.contract_id", ondelete="CASCADE"), index=True)
    alert_type = Column(String(30))  # breakout/volume_surge/pattern_match
    alert_level = Column(SmallInteger)  # 1:低 2:中 3:高
    alert_message = Column(Text)
    trigger_price = Column(Numeric(12, 2))
    trigger_volume = Column(BigInteger)
    sector_id = Column(Integer, ForeignKey("sectors.sector_id"), index=True)
    is_pushed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    pushed_at = Column(DateTime)

    # 关系
    contract = relationship("FuturesContract", back_populates="alerts", foreign_keys=[contract_id])
    sector = relationship("Sector", foreign_keys=[sector_id])

    def __repr__(self):
        return f"<OpportunityAlert(alert_id={self.alert_id}, contract_id={self.contract_id}, alert_type={self.alert_type})>"


class DataSource(Base):
    """数据源配置表模型。

    对应数据库表：data_sources
    """

    __tablename__ = "data_sources"

    source_id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String(100), nullable=False)
    source_type = Column(String(20))  # api/database/file
    api_url = Column(String(500))
    api_key = Column(String(255))
    is_active = Column(Boolean, default=True, index=True)
    priority_level = Column(Integer, default=1)
    updated_by = Column(BigInteger, ForeignKey("users.user_id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<DataSource(source_id={self.source_id}, source_name={self.source_name}, source_type={self.source_type})>"


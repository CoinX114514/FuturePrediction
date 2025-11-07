-- 期货交易系统数据库表结构
-- 基于 README_DEV.md 的数据库设计

-- 启用 UUID 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- 5.1 用户体系表设计
-- ============================================

-- 用户表
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    user_role SMALLINT DEFAULT 1, -- 1:普通用户 2:会员 3:超级管理员
    avatar_url VARCHAR(500),
    nickname VARCHAR(50),
    real_name VARCHAR(50),
    prediction_count INTEGER DEFAULT 0, -- 已使用预测次数
    daily_prediction_limit INTEGER DEFAULT 5, -- 每日预测限制
    member_expire_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_users_role ON users(user_role);
CREATE INDEX idx_users_email ON users(email);

-- 用户会话表
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    user_agent VARCHAR(500),
    browser_name VARCHAR(50),
    ip_address INET,
    expire_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_sessions_user ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(token_hash);
CREATE INDEX idx_user_sessions_expire ON user_sessions(expire_at);

-- ============================================
-- 5.2 期货数据表设计
-- ============================================

-- 板块表（需要先创建，因为期货合约表引用它）
CREATE TABLE sectors (
    sector_id SERIAL PRIMARY KEY,
    sector_code VARCHAR(20) UNIQUE NOT NULL,
    sector_name VARCHAR(100) NOT NULL,
    parent_sector_id INTEGER REFERENCES sectors(sector_id),
    sector_level SMALLINT DEFAULT 1,
    display_order INTEGER DEFAULT 0,
    is_vip_only BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sectors_parent ON sectors(parent_sector_id);
CREATE INDEX idx_sectors_code ON sectors(sector_code);

-- 期货合约表
CREATE TABLE futures_contracts (
    contract_id SERIAL PRIMARY KEY,
    contract_code VARCHAR(20) UNIQUE NOT NULL, -- 如：IF2312
    contract_name VARCHAR(100) NOT NULL,
    exchange_code VARCHAR(10) NOT NULL, -- SHFE/DCE/CZCE/CFFEX
    underlying_asset VARCHAR(50),
    contract_multiplier DECIMAL(10,2),
    price_tick DECIMAL(10,4),
    sector_id INTEGER REFERENCES sectors(sector_id),
    is_active BOOLEAN DEFAULT TRUE,
    listed_date DATE,
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contracts_code ON futures_contracts(contract_code);
CREATE INDEX idx_contracts_sector ON futures_contracts(sector_id);
CREATE INDEX idx_contracts_exchange ON futures_contracts(exchange_code);

-- 行情数据表
CREATE TABLE market_data (
    data_id BIGSERIAL PRIMARY KEY,
    contract_id INTEGER REFERENCES futures_contracts(contract_id) ON DELETE CASCADE,
    trade_date DATE NOT NULL,
    open_price DECIMAL(12,2),
    high_price DECIMAL(12,2),
    low_price DECIMAL(12,2),
    close_price DECIMAL(12,2),
    settlement_price DECIMAL(12,2),
    volume BIGINT,
    open_interest BIGINT,
    turnover DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(contract_id, trade_date)
);

CREATE INDEX idx_market_data_contract_date ON market_data(contract_id, trade_date);
CREATE INDEX idx_market_data_date ON market_data(trade_date);

-- ============================================
-- 5.3 预测相关表设计
-- ============================================

-- 预测任务表
CREATE TABLE prediction_tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    contract_id INTEGER REFERENCES futures_contracts(contract_id),
    prediction_type VARCHAR(20) DEFAULT 'kronos_daily', 
    prediction_horizon INTEGER DEFAULT 1, -- 预测步长(天)
    prediction_paths INTEGER DEFAULT 10, -- 路径数量
    input_data_source VARCHAR(20), -- api/csv/manual
    csv_file_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending', -- pending/processing/completed/failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX idx_prediction_tasks_user ON prediction_tasks(user_id);
CREATE INDEX idx_prediction_tasks_status ON prediction_tasks(status);
CREATE INDEX idx_prediction_tasks_contract ON prediction_tasks(contract_id);

-- 预测结果表
CREATE TABLE prediction_results (
    result_id BIGSERIAL PRIMARY KEY,
    task_id UUID REFERENCES prediction_tasks(task_id) ON DELETE CASCADE,
    prediction_date DATE NOT NULL,
    path_number INTEGER DEFAULT 1,
    predicted_price DECIMAL(12,2),
    upper_bound DECIMAL(12,2), -- 置信区间上界
    lower_bound DECIMAL(12,2), -- 置信区间下界
    confidence_level DECIMAL(5,2), -- 置信度百分比
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prediction_results_task ON prediction_results(task_id);
CREATE INDEX idx_prediction_results_date ON prediction_results(prediction_date);

-- ============================================
-- 5.4 板块与推荐表设计
-- ============================================

-- 机会提醒表
CREATE TABLE opportunity_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    contract_id INTEGER REFERENCES futures_contracts(contract_id) ON DELETE CASCADE,
    alert_type VARCHAR(30), -- breakout/volume_surge/pattern_match
    alert_level SMALLINT, -- 1:低 2:中 3:高
    alert_message TEXT,
    trigger_price DECIMAL(12,2),
    trigger_volume BIGINT,
    sector_id INTEGER REFERENCES sectors(sector_id),
    is_pushed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pushed_at TIMESTAMP
);

CREATE INDEX idx_alerts_contract ON opportunity_alerts(contract_id);
CREATE INDEX idx_alerts_created ON opportunity_alerts(created_at);
CREATE INDEX idx_alerts_sector ON opportunity_alerts(sector_id);

-- ============================================
-- 5.5 系统配置表设计
-- ============================================

-- 数据源配置表
CREATE TABLE data_sources (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    source_type VARCHAR(20), -- api/database/file
    api_url VARCHAR(500),
    api_key VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    priority_level INTEGER DEFAULT 1,
    updated_by BIGINT REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_data_sources_active ON data_sources(is_active);

-- ============================================
-- 触发器：自动更新 updated_at
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_data_sources_updated_at BEFORE UPDATE ON data_sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();


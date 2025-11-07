## 一、项目概述

### 1.1 产品定位

面向中国职业期货交易员的智能辅助决策工具，通过AI技术赋能交易决策，提升交易效率和成功率。

## 二、用户画像与需求分析

### 2.1 目标用户

- **主要用户**：职业期货交易员
- **用户痛点**： 
   - 信息过载，难以快速发现交易机会
   - 缺乏科学的价格预测工具
   - 传统技术分析效率低下

### 2.2 使用场景

- 开盘前快速扫描市场机会
- 交易决策时的价格走势参考
- 收盘后的复盘分析

## 三、功能需求详细说明

### 3.1 核心功能模块

#### 3.1.1 板块榜单系统

- **功能描述**：按板块分类展示期货合约排名
- **技术实现**：基于实时行情数据计算涨跌幅、成交量排序
- **展示维度**： 
   - 涨幅榜（按日涨跌幅排序）
   - 成交量榜（按成交金额排序）
   - 波动率榜（按日内振幅排序）
- **数据更新**：每5秒刷新一次排名
- **优先级**：P0

#### 3.1.2 Kronos框架价格预测引擎

- **功能描述**：使用预训练的Kronos模型对输入的OHLCV数据进行日线级别价格预测
- **模型说明**： 
   - 使用历史20年数据预训练完成的固定权重模型
   - 模型权重不随用户输入动态更新
   - 仅做推理预测，不进行在线训练
- **输入数据**： 
   - Open（开盘价）
   - High（最高价）
   - Low（最低价）
   - Close（收盘价）
   - Volume（成交量）
- **技术架构**：Kronos时序预测框架（推理模式）
- **预测维度**： 
   - 日线级别预测（T+1至T+30）
   - 支持自定义预测步长
   - 基于固定模型的多路径概率推演
- **输出结果**： 
   - 预测价格序列
   - 置信区间（上下界）
   - 多条可能路径及概率分布
- **一期目标**： 
   - 部署预训练模型进行推理服务
   - 确保推理性能和响应速度
   - 模型文件版本管理
- **优先级**：P0

This content is only supported in a Feishu Docs

功能层级详细图标

This content is only supported in a Feishu Docs

数据流示意图

### 3.2 界面设计需求

#### 3.2.1 登录界面

- 手机号/邮箱登录
- 微信扫码登录
- 找回密码功能

#### 3.2.2 主界面

- **实时行情模块**
   - K线图（支持多周期切换）
   - 深度图
   - 成交明细
- **板块热力图**
   - 涨跌幅排行
   - 成交额排行
   - 异动提醒
- **AI****预测面板**
   - 预测K线叠加显示
   - 准确率历史回测
   - 信号强度指示器
- **基础信息栏**
   - 合约详情
   - 持仓分析
   - 资金流向

#### 3.2.3 数据管理

- CSV数据上传接口
- 自定义指标配置
- 历史数据回测

### 3.3 账户权限体系

#### 权限矩阵

| 功能模块     | 普通用户  | 会员用户 | 超级管理员 |
| ------------ | --------- | -------- | ---------- |
| 基础行情查看 | ✓         | ✓        | ✓          |
| 板块榜单查看 | 部分(3个) | 全部     | 全部       |
| AI预测次数   | 5次/天    | 无限     | 无限       |
| CSV上传      | ✗         | ✓        | ✓          |
| 自定义头像   | ✗         | ✓        | ✓          |
| 数据源管理   | ✗         | ✗        | ✓          |
| 用户权限管理 | ✗         | ✗        | ✓          |

## 四、技术架构设计

### 4.1 系统架构

```Plain
前端层：React + TypeScript (Web响应式)
服务层：Node.js + GraphQL
算法层：Python + Kronos Framework
数据层：PostgreSQL + Redis + InfluxDB
```

### 4.2 数据流设计

- 实时行情：WebSocket长连接
- 预测服务：异步队列处理
- 推送服务：消息队列 + Push Gateway

### 4.3 性能指标

- 行情延迟：<100ms
- 预测响应：<3s
- 并发支持：10000 QPS

## 五、数据库设计

### 5.1 用户体系表设计

#### users（用户表）

```SQL
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
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_phone (phone_number),
    INDEX idx_role (user_role)
);
```

#### user_sessions（会话表）

```SQL
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(user_id),
    token_hash VARCHAR(255) NOT NULL,
    user_agent VARCHAR(500),
    browser_name VARCHAR(50),
    ip_address INET,
    expire_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_session (user_id),
    INDEX idx_token (token_hash)
);
```

### 5.2 期货数据表设计

#### futures_contracts（期货合约表）

```SQL
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_code (contract_code),
    INDEX idx_sector (sector_id)
);
```

#### market_data（行情数据表）

```SQL
CREATE TABLE market_data (
    data_id BIGSERIAL PRIMARY KEY,
    contract_id INTEGER REFERENCES futures_contracts(contract_id),
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
    UNIQUE(contract_id, trade_date),
    INDEX idx_contract_date (contract_id, trade_date)
);
```

### 5.3 预测相关表设计

#### prediction_tasks（预测任务表）

```SQL
CREATE TABLE prediction_tasks (
    task_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id BIGINT REFERENCES users(user_id),
    contract_id INTEGER REFERENCES futures_contracts(contract_id),
    prediction_type VARCHAR(20) DEFAULT 'kronos_daily', 
    prediction_horizon INTEGER DEFAULT 1, -- 预测步长(天)
    prediction_paths INTEGER DEFAULT 10, -- 路径数量
    input_data_source VARCHAR(20), -- api/csv/manual
    csv_file_url VARCHAR(500),
    status VARCHAR(20) DEFAULT 'pending', -- pending/processing/completed/failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    INDEX idx_user_task (user_id),
    INDEX idx_status (status)
);
```

#### prediction_results（预测结果表）

```SQL
CREATE TABLE prediction_results (
    result_id BIGSERIAL PRIMARY KEY,
    task_id UUID REFERENCES prediction_tasks(task_id),
    prediction_date DATE NOT NULL,
    path_number INTEGER DEFAULT 1,
    predicted_price DECIMAL(12,2),
    upper_bound DECIMAL(12,2), -- 置信区间上界
    lower_bound DECIMAL(12,2), -- 置信区间下界
    confidence_level DECIMAL(5,2), -- 置信度百分比
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_task_result (task_id)
);
```

### 5.4 板块与推荐表设计

#### sectors（板块表）

```SQL
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
```

#### opportunity_alerts（机会提醒表）

```SQL
CREATE TABLE opportunity_alerts (
    alert_id BIGSERIAL PRIMARY KEY,
    contract_id INTEGER REFERENCES futures_contracts(contract_id),
    alert_type VARCHAR(30), -- breakout/volume_surge/pattern_match
    alert_level SMALLINT, -- 1:低 2:中 3:高
    alert_message TEXT,
    trigger_price DECIMAL(12,2),
    trigger_volume BIGINT,
    sector_id INTEGER REFERENCES sectors(sector_id),
    is_pushed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pushed_at TIMESTAMP,
    INDEX idx_contract_alert (contract_id),
    INDEX idx_created (created_at)
);
```

### 5.5 系统配置表设计

#### data_sources（数据源配置表）

```SQL
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
```

## 六、变量命名规范框架

### 6.1 通用命名原则

#### 基础规则

- **小写下划线**：数据库字段、Python变量 → `user_name`, `trade_date`
- **驼峰命名**：JavaScript/Java变量 → `userName`, `tradeDate`
- **帕斯卡命名**：类名、组件名 → `UserProfile`, `PredictionEngine`
- **全大写下划线**：常量 → `MAX_RETRY_COUNT`, `API_TIMEOUT`

### 6.2 前端命名规范

#### React组件与变量

```JavaScript
// 组件命名
const TradingDashboard = () => {};
const PriceChart = () => {};

// 状态变量
const [selectedContract, setSelectedContract] = useState();
const [isLoading, setIsLoading] = useState(false);
const [predictionData, setPredictionData] = useState([]);

// 函数命名
const handleSubmitPrediction = () => {};
const fetchMarketData = async () => {};
const calculateConfidenceInterval = () => {};

// 常量定义
const PREDICTION_LIMIT_FREE = 5;
const REFRESH_INTERVAL_MS = 1000;
```

#### CSS模块化命名

```CSS
/* CSS Modules */
.tradingDashboard {}
.tradingDashboard__header {}
.tradingDashboard__chart--active {}
.btn--primary {}
.btn--disabled {}
```

### 6.3 后端命名规范

#### Python/Django规范

```Python
# 类命名
class PredictionTask:
class UserAuthenticationService:

# 函数和方法
def get_user_by_id(user_id: int):
def calculate_moving_average(prices: list):
def validate_contract_code(code: str):

# 变量命名
user_role = 1
prediction_count = 0
is_member_expired = False

# 常量定义
MAX_PREDICTION_HORIZON = 30
DEFAULT_PATH_COUNT = 10
KRONOS_MODEL_VERSION = "1.0.0"
```

#### API接口命名

```Plain
# RESTful资源命名
GET    /api/v1/users/{user_id}
POST   /api/v1/predictions
GET    /api/v1/contracts/{contract_code}/market-data
PUT    /api/v1/users/{user_id}/membership
DELETE /api/v1/sessions/{session_id}

# GraphQL查询命名
query getUserProfile
mutation createPredictionTask
subscription marketDataUpdates
```

### 6.4 数据库命名规范

#### 表和字段命名

```SQL
-- 表名：复数名词，小写下划线
users, futures_contracts, prediction_tasks

-- 字段名：小写下划线
user_id, created_at, is_active

-- 索引命名
idx_{table}_{column}  -- idx_users_email
unq_{table}_{columns} -- unq_market_data_contract_date
fk_{table}_{reference} -- fk_predictions_user

-- 外键命名
{table}_id -- user_id, contract_id
```

### 6.5 文件和目录命名

#### 项目结构

```Plain
/frontend
  /src
    /components
      /TradingDashboard
        TradingDashboard.tsx
        TradingDashboard.test.ts
        TradingDashboard.module.css
    /pages
      /login
        Login.tsx
        Login.module.css
      /dashboard
        Dashboard.tsx
        Dashboard.module.css
    /services
      authService.ts
      predictionService.ts
    /utils
      dateFormatter.ts
      priceCalculator.ts
    /constants
      apiEndpoints.ts
      tradingConstants.ts
    /hooks
      useWebSocket.ts
      useAuth.ts
    /store
      userStore.ts
      marketStore.ts
```

### 6.6 Git分支命名

```Plain
master/main          -- 主分支
develop             -- 开发分支
feature/user-auth   -- 功能分支
bugfix/chart-render -- 修复分支
hotfix/api-timeout  -- 热修复分支
release/v1.0.0     -- 发布分支
```

### 6.7 环境变量命名

```Bash
# .env 文件
DB_HOST=localhost
DB_PORT=5432
DB_NAME=futures_trading
REDIS_URL=redis://localhost:6379
KRONOS_API_KEY=xxx
MAX_WORKERS=4
LOG_LEVEL=INFO
```

## 七、项目实施计划

### 7.1 开发周期（3个月）

- **第1个月**：核心功能开发（行情+板块榜单）
- **第2个月**：Kronos日线预测集成+权限系统
- **第3个月**：测试优化+上线准备

## 七、项目实施计划

### 7.1 开发周期（3个月）

- **第1个月**：核心功能开发（行情+板块榜单）
- **第2个月**：Kronos日线预测集成+权限系统
- **第3个月**：测试优化+上线准备

### 7.2 技术架构实施顺序

1. **Week 1-2**: 数据库搭建，API框架初始化
2. **Week 3-4**: 用户认证系统，权限管理
3. **Week 5-6**: 行情数据接入，WebSocket实时推送
4. **Week 7-8**: 板块榜单功能，机会发现算法
5. **Week 9-10**: Kronos模型集成，预测任务队列
6. **Week 11-12**: 前端界面完善，系统联调测试

## 八、技术实现要点

### 8.1 关键技术难点

- **WebSocket****长连接****管理**：使用Socket.io处理断线重连，心跳检测
- **Kronos模型部署**：Docker容器化，使用Celery异步任务队列
- **高并发处理**：Redis缓存热点数据，PostgreSQL读写分离
- **CSV****文件处理**：限制文件大小<10MB，使用pandas预处理验证

### 8.2 接口设计示例

#### 登录接口

```Plain
POST /api/v1/auth/login
Request:
{
  "phone_number": "13800138000",
  "password": "hashed_password"
}
Response:
{
  "token": "jwt_token",
  "user_id": 12345,
  "user_role": 1
}
```

#### 预测任务接口

```Plain
POST /api/v1/predictions/create
Headers: Authorization: Bearer {token}
Request:
{
  "contract_code": "IF2312",
  "prediction_horizon": 5,
  "prediction_paths": 10,
  "data_source": "api"
}
Response:
{
  "task_id": "uuid",
  "status": "processing",
  "estimated_time": 30
}
```

#### WebSocket推送格式

```JavaScript
// 订阅
socket.emit('subscribe', {
  contract_codes: ['IF2312', 'IC2312'],
  data_types: ['price', 'alert']
});

// 接收推送
socket.on('market_data', (data) => {
  // data: {contract_code, price, volume, timestamp}
});
```

### 8.3 部署配置

#### Docker Compose配置

```YAML
version: '3.8'
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_DB: futures_trading
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    
  backend:
    build: ./backend
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres/futures_trading
      REDIS_URL: redis://redis:6379
    
  kronos:
    build: ./kronos
    depends_on:
      - redis
    environment:
      REDIS_URL: redis://redis:6379
      MODEL_PATH: /models/kronos_v1.pkl
```

#### Nginx配置

```Nginx
upstream backend {
    server backend:8000;
}

upstream websocket {
    server backend:3000;
}

server {
    listen 80;
    
    location /api/ {
        proxy_pass http://backend;
    }
    
    location /ws/ {
        proxy_pass http://websocket;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }
}
```

## 九、待解决问题

1. **数据源****选择**：需确定期货行情数据API供应商（新浪财经/东方财富/付费数据源）
2. **Kronos模型训练**：需要历史数据进行模型训练，建议使用过去3年日线数据
3. **浏览器****兼容性**：建议支持Chrome 90+、Firefox 88+、Safari 14+、Edge 90+
4. **支付接入**：会员支付需接入支付宝/微信支付SDK
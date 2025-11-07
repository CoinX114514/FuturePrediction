# 数据库设置指南

## 前置要求

1. **安装 PostgreSQL**
   ```bash
   # macOS (使用 Homebrew)
   brew install postgresql@14
   brew services start postgresql@14
   
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Windows
   # 从 https://www.postgresql.org/download/windows/ 下载安装
   ```

2. **安装 Redis**（可选，用于缓存和任务队列）
   ```bash
   # macOS
   brew install redis
   brew services start redis
   
   # Ubuntu/Debian
   sudo apt-get install redis-server
   sudo systemctl start redis
   ```

## 数据库初始化步骤

### 1. 创建数据库

**重要提示（macOS/Homebrew 用户）**：
使用 Homebrew 安装的 PostgreSQL 默认使用当前系统用户名（而不是 `postgres`）作为数据库超级用户。如果遇到 `role "postgres" does not exist` 错误，请使用以下方法：

#### 方法 A：使用系统用户名（推荐，简单）

```bash
# 使用当前系统用户名连接（替换 your_username 为你的系统用户名）
psql -U $(whoami) -d postgres

# 或者直接使用
psql -d postgres

# 创建数据库
CREATE DATABASE futures_trading;

# 创建 postgres 用户（可选，用于与文档保持一致）
CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';

# 退出
\q
```

#### 方法 B：使用 postgres 用户（标准方式）

```bash
# 登录 PostgreSQL（使用系统用户名）
psql -U $(whoami) -d postgres

# 创建 postgres 用户
CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';

# 创建数据库
CREATE DATABASE futures_trading;

# 创建用户（可选）
CREATE USER futures_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE futures_trading TO futures_user;

# 退出
\q
```

#### Linux/Windows 用户（标准方式）

```bash
# 登录 PostgreSQL
psql -U postgres

# 创建数据库
CREATE DATABASE futures_trading;

# 创建用户（可选）
CREATE USER futures_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE futures_trading TO futures_user;

# 退出
\q
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cd backend
cp .env.example .env
```

编辑 `.env` 文件，设置数据库连接：

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/futures_trading
```

### 3. 安装 Python 依赖

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 4. 创建数据库表

有两种方式：

#### 方式 1：使用 SQL 脚本（推荐）

```bash
# 直接执行 SQL 脚本
psql -U postgres -d futures_trading -f database/schema.sql
```

#### 方式 2：使用 Python 脚本

```bash
# 使用 SQLAlchemy 创建表
python -m app.database.init_db
```

### 5. 验证数据库

```bash
# 连接数据库查看表
psql -U postgres -d futures_trading

# 查看所有表
\dt

# 应该看到以下表：
# - users
# - user_sessions
# - sectors
# - futures_contracts
# - market_data
# - prediction_tasks
# - prediction_results
# - opportunity_alerts
# - data_sources
```

## 数据库迁移（使用 Alembic）

### 初始化 Alembic

```bash
cd backend
alembic init alembic
```

### 创建迁移

```bash
# 自动生成迁移脚本
alembic revision --autogenerate -m "Initial migration"

# 应用迁移
alembic upgrade head
```

## 常见问题

### 问题 1：role "postgres" does not exist（macOS/Homebrew）

**错误**：`psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL: role "postgres" does not exist`

**原因**：Homebrew 安装的 PostgreSQL 默认使用系统用户名，而不是 `postgres` 用户。

**解决**：
```bash
# 方法 1：使用系统用户名连接
psql -U $(whoami) -d postgres

# 方法 2：创建 postgres 用户
psql -U $(whoami) -d postgres -c "CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';"

# 然后就可以使用 postgres 用户了
psql -U postgres -d postgres
```

### 问题 2：连接被拒绝

**错误**：`psycopg2.OperationalError: could not connect to server`

**解决**：
1. 检查 PostgreSQL 是否运行：
   - macOS: `brew services list`
   - Linux: `sudo systemctl status postgresql`
2. 启动 PostgreSQL：
   - macOS: `brew services start postgresql@14`
   - Linux: `sudo systemctl start postgresql`
3. 检查端口是否正确（默认 5432）
4. 检查防火墙设置

### 问题 3：权限不足

**错误**：`permission denied for database`

**解决**：
```sql
-- 授予权限
GRANT ALL PRIVILEGES ON DATABASE futures_trading TO your_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
```

### 问题 4：UUID 扩展不存在

**错误**：`extension "uuid-ossp" does not exist`

**解决**：
```sql
-- 在数据库中执行
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

## 下一步

数据库设置完成后，继续：
1. 阶段 2：用户认证系统
2. 阶段 3：Kronos 模型集成


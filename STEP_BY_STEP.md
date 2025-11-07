# 分步骤开发指南

## 📋 当前进度

### ✅ 已完成（阶段 1：数据库搭建）

1. **数据库设计**
   - ✅ 创建了完整的 SQL 表结构脚本（`backend/database/schema.sql`）
   - ✅ 定义了所有 SQLAlchemy 模型（`backend/app/database/models.py`）
   - ✅ 配置了数据库连接（`backend/app/database/connection.py`）

2. **依赖更新**
   - ✅ 更新了 `requirements.txt`，添加了所有必需的依赖

3. **初始化脚本**
   - ✅ 创建了数据库初始化脚本
   - ✅ 创建了种子数据脚本

### 🔄 下一步操作

#### 立即执行：安装依赖并初始化数据库

```bash
# 1. 安装新的 Python 依赖
cd backend
source venv/bin/activate
pip install -r requirements.txt

# 2. 安装 PostgreSQL（如果还没有）
# macOS:
brew install postgresql@14
brew services start postgresql@14

# 3. 创建数据库
createdb futures_trading
# 或使用 psql:
# psql -U postgres
# CREATE DATABASE futures_trading;

# 4. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置 DATABASE_URL

# 5. 初始化数据库表
python -m app.database.init_db
```

## 📝 开发路线图

### 阶段 1：数据库搭建 ✅ 已完成代码

**文件清单：**
- `backend/database/schema.sql` - SQL 表结构
- `backend/app/database/connection.py` - 数据库连接
- `backend/app/database/models.py` - ORM 模型
- `backend/app/database/seed_data.py` - 种子数据
- `backend/app/database/init_db.py` - 初始化脚本

**下一步：** 用户需要安装 PostgreSQL 并执行初始化

---

### 阶段 2：用户认证与权限（下一步）

#### 2.1 用户认证系统

**需要创建的文件：**
- `backend/app/services/auth_service.py` - 认证服务
- `backend/app/routers/auth.py` - 认证路由
- `backend/app/middleware/auth.py` - 认证中间件
- `backend/app/utils/jwt.py` - JWT 工具

**功能：**
- 用户注册（手机号/邮箱）
- 用户登录
- JWT Token 生成和验证
- 密码加密（bcrypt）
- 会话管理

#### 2.2 权限管理系统

**需要创建的文件：**
- `backend/app/middleware/permission.py` - 权限中间件
- `backend/app/utils/permissions.py` - 权限工具

**功能：**
- 角色验证（普通用户/会员/超级管理员）
- 权限装饰器
- 预测次数限制逻辑

---

### 阶段 3：Kronos 模型集成

#### 3.1 模型服务完善

**需要修改的文件：**
- `backend/app/services/model_inference.py` - 集成实际模型

**功能：**
- 加载预训练 Kronos 模型
- 多路径预测
- 置信区间计算

#### 3.2 预测任务系统

**需要创建的文件：**
- `backend/app/services/task_queue.py` - Celery 任务队列
- `backend/app/routers/prediction_v2.py` - 新版预测接口

**功能：**
- 异步任务处理
- 任务状态管理
- 结果存储到数据库

---

### 阶段 4：板块榜单与实时行情

#### 4.1 板块榜单系统

**需要创建的文件：**
- `backend/app/services/ranking_service.py` - 榜单计算服务
- `backend/app/routers/rankings.py` - 榜单 API

**功能：**
- 涨幅榜计算
- 成交量榜计算
- 波动率榜计算

#### 4.2 实时行情系统

**需要创建的文件：**
- `backend/app/routers/websocket.py` - WebSocket 路由
- `backend/app/services/market_data_service.py` - 行情数据服务

**功能：**
- WebSocket 服务器
- 实时数据推送
- 订阅管理

---

### 阶段 5：前端界面完善

#### 5.1 登录界面

**需要创建的文件：**
- `frontend/src/pages/Login.tsx`
- `frontend/src/pages/Register.tsx`
- `frontend/src/services/authService.ts`

#### 5.2 主界面

**需要创建的文件：**
- `frontend/src/pages/Dashboard.tsx`
- `frontend/src/components/TradingDashboard/`
- `frontend/src/components/KLineChart/`
- `frontend/src/components/Rankings/`

---

## 🎯 立即开始

**当前任务：阶段 1 完成后的数据库初始化**

请按照 `backend/DATABASE_SETUP.md` 的说明：
1. 安装 PostgreSQL
2. 创建数据库
3. 配置环境变量
4. 运行初始化脚本

完成后，我们将继续阶段 2：用户认证系统。


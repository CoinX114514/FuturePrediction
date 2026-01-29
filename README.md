# 期货信号发布与权限管理系统

这是一个前后端分离的期货信号分发平台。系统为普通用户提供信号浏览、账户信息、收藏/历史记录等体验，为管理员和超级管理员提供信号发布、草稿管理以及帖子编辑/删除等能力。

## ✨ 主要特性

- **仪表盘信号流**：从后端实时拉取官方信号，展示策略摘要、止损/止盈等信息。
- **帖子详情页**：管理员可在详情页直接删除或跳转到编辑页面；普通用户可收藏/浏览。
- **草稿 & 发布中心**：
  - 草稿箱与已发布帖子均从数据库实时拉取。
  - 支持草稿创建、更新、删除以及一键发布。
  - 管理员可再次选中自己的帖子进行编辑并更新内容。
- **权限管理**：使用 JWT 鉴权与角色（普通用户 / VIP 会员 / 管理员 / 超管）控制访问。
- **健壮的后端 API**：FastAPI + SQLAlchemy + PostgreSQL，含草稿、帖子、收藏、浏览历史等模块。
- **工程化体验**：提供 `restart_project.sh` 一键重启脚本，启动前自动建表并清理端口。

## 🗂️ 项目结构

```
Quant_webui/
├── backend/                 # FastAPI 服务
│   ├── app/
│   │   ├── main.py          # 入口，挂载路由 & CORS
│   │   ├── database/        # SQLAlchemy 连接 & 模型
│   │   ├── routers/         # auth、posts、drafts、collections、browse_history
│   │   ├── services/        # 业务逻辑（post_service、draft_service 等）
│   │   └── utils/           # JWT、密码哈希、权限工具
│   ├── requirements.txt
│   └── run_server.py
├── frontend/                # React + TypeScript + Vite
│   ├── src/
│   │   ├── pages/           # Dashboard、SignalDetail、AdminPublish、Account 等
│   │   ├── components/      # Header、Sidebar、SignalCard...
│   │   └── services/        # authService、postService、draftService...
│   ├── package.json
│   └── vite.config.ts
├── restart_project.sh       # 一键清端口、建表、启动脚本
├── DOCKER_SETUP.md / docker-compose.yml
└── README.md                # 当前文档
```

## 🛠️ 技术栈

| 层        | 技术                                                   |
|-----------|--------------------------------------------------------|
| 前端      | React 18、TypeScript、Vite、Tailwind CSS、React Router |
| 后端      | FastAPI、SQLAlchemy、PostgreSQL、JWT、bcrypt           |
| 通信      | Axios + REST API                                       |
| 开发辅助  | Node 20、Python 3.11+、restart_project.sh              |

## 🚀 快速开始

### 1. 准备环境

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### 2. 后端依赖

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. 前端依赖

```bash
cd frontend
npm install
```

### 4. 启动（推荐脚本）

```bash
cd /Users/colin/Documents/Quant_webui
./restart_project.sh
```

脚本会自动：

1. 杀掉 8000 / 5173 端口占用进程
2. 调用 `Base.metadata.create_all()` 确保数据库表齐全
3. 启动 FastAPI (`http://localhost:8000`)
4. 启动 Vite (`http://localhost:5173`)

若需手动运行：

```bash
# 后端
cd backend && source venv/bin/activate && python run_server.py

# 前端
cd frontend && npm run dev
```

## 📦 关键 API

- `POST /api/v1/auth/login`：登录获取 JWT
- `GET /api/v1/posts`：支持分页、按作者过滤（`author_id=current`）
- `POST /api/v1/posts`：管理员发布帖子
- `PUT /api/v1/posts/{id}`：管理员/超管编辑自己的帖子
- `DELETE /api/v1/posts/{id}`：软删除帖子
- `GET /api/v1/drafts` / `POST /api/v1/drafts`...：草稿 CRUD
- `GET /api/v1/browse-history` / `GET /api/v1/collections`：个人数据拉取

## 🧹 根目录清理

历史遗留的 `Kronos-master/` 与 `LULU_daily.csv` 已移除，避免混淆；如需再次导入模型或样例数据，请放置在 `backend/app/models/` 或 `backend/database/` 中并更新文档。

## 📄 其他文档

- `README_DEV.md`：开发阶段记录
- `DOCKER_SETUP.md` / `docker-compose.yml`：容器化部署指引
- `PHASE2_COMPLETE.md`、`PRD_GAP_ANALYSIS.md` 等：需求/验收文档

---

如需了解更多细节（如角色权限、API 示例、UI 交互），请参考 `README_DEV.md` 或直接阅读前后端源码。欢迎继续完善！💪


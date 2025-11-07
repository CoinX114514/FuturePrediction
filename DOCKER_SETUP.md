# Docker 快速部署指南

本文檔說明如何使用 Docker 一鍵啟動整個專案（PostgreSQL + FastAPI 後端 + Vite 前端）。

## 1. 先決條件

- 已安裝 [Docker](https://docs.docker.com/get-docker/)
- 已安裝 [Docker Compose](https://docs.docker.com/compose/install/)（Mac 與 Windows 的 Docker Desktop 內建）

## 2. 一鍵啟動

```bash
# 於專案根目錄執行
docker compose up --build
```

首次執行會自動：
- 下載 PostgreSQL、Node.js、Python 的基礎映像檔
- 安裝前後端依賴
- 初始化資料庫結構（由 `backend/app/database/init_db.py` 完成）

完成後服務對應的埠為：
- 前端（Vite Dev Server）：http://localhost:5173
- 後端（FastAPI）：http://localhost:8000
- PostgreSQL：localhost:5432 （帳號密碼皆為 `postgres`）

## 3. 常用指令

```bash
# 重新建置並啟動（遇到依賴更新時使用）
docker compose up --build

# 背景執行
docker compose up -d

# 查看容器日誌
docker compose logs -f backend

# 停止容器
docker compose down

# 停止並刪除資料卷（重置資料庫）
docker compose down -v
```

## 4. 前端環境變數

Docker Compose 已自動將 `VITE_API_BASE_URL` 設定為 `http://backend:8000`，前端在容器內會直接呼叫後端服務。

若要於本機非 Docker 模式下啟動前端，可在 `frontend/.env` 中自訂：

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 5. 推送至 GitHub 提示

1. 在本機檢查狀態：
   ```bash
   git status
   ```
2. 新增與提交：
   ```bash
   git add .
   git commit -m "chore: add docker setup"
   ```
3. 登入 GitHub 建立遠端 repo 後，設定 remote 並推送：
   ```bash
   git remote add origin <你的 GitHub 倉庫 URL>
   git push -u origin main
   ```

完成後，任何人只需 `git clone` 此專案，並運行 `docker compose up --build` 即可開箱使用。

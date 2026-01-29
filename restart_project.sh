#!/bin/bash

# 使用绝对路径，确保在任何位置执行都能定位到项目
PROJECT_ROOT="/Users/colin/Documents/Quant_webui"
cd "$PROJECT_ROOT" || exit 1

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  项目重启脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 清理端口函数
cleanup_ports() {
    echo -e "${YELLOW}正在检查并清理端口...${NC}"
    
    # 清理后端端口 8000
    PIDS_8000=$(lsof -ti:8000 2>/dev/null)
    if [ -n "$PIDS_8000" ]; then
        echo -e "${RED}停止占用端口 8000 的进程...${NC}"
        echo "$PIDS_8000" | xargs kill -9 2>/dev/null
        sleep 1
    fi

    # 清理前端端口 5175
    PIDS_5175=$(lsof -ti:5175 2>/dev/null)
    if [ -n "$PIDS_5175" ]; then
        echo -e "${RED}停止占用端口 5175 的进程...${NC}"
        echo "$PIDS_5175" | xargs kill -9 2>/dev/null
        sleep 1
    fi
    
    # 额外清理：查找所有相关的uvicorn和vite进程
    echo -e "${YELLOW}清理残留进程...${NC}"
    pkill -f "uvicorn app.main:app" 2>/dev/null
    pkill -f "vite" 2>/dev/null
    
    sleep 2
    echo -e "${GREEN}端口清理完成${NC}"
}

# 初始化数据库表，避免缺表导致后端 500
init_database() {
    echo -e "${GREEN}正在检查/创建数据库表...${NC}"
    cd "$PROJECT_ROOT/backend" || exit 1
    if [ -d "venv" ]; then
        source venv/bin/activate
    else
        echo "警告: 未找到虚拟环境 venv，尝试直接运行 python"
    fi

    python - <<'PY'
from app.database.connection import Base, engine
from app.database import models  # noqa: F401  确保所有模型被导入
print("→ 开始执行 Base.metadata.create_all ...")
Base.metadata.create_all(bind=engine)
print("✓ 数据库表检查完成")
PY

    # 退出虚拟环境，避免影响后续 npm 命令
    if command -v deactivate >/dev/null 2>&1; then
        deactivate
    fi
    cd "$PROJECT_ROOT" || exit 1
}

# 执行清理与数据库初始化
cleanup_ports
init_database

# 捕获退出信号以清理子进程
trap 'kill $(jobs -p) 2>/dev/null' SIGINT SIGTERM EXIT

# 启动后端
echo -e "${GREEN}正在启动后端服务...${NC}"
cd "$PROJECT_ROOT/backend" || exit 1
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "警告: 未找到虚拟环境 venv，尝试直接运行 python"
fi

# 后台运行后端
python run_server.py &
BACKEND_PID=$!
cd "$PROJECT_ROOT" || exit 1

# 等待几秒确保后端开始初始化
sleep 3

# 启动前端
echo -e "${GREEN}正在启动前端服务...${NC}"
cd "$PROJECT_ROOT/frontend" || exit 1

# 检查node_modules是否存在
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}未找到 node_modules，正在安装依赖...${NC}"
    npm install
fi

# 后台运行前端
npm run dev &
FRONTEND_PID=$!
cd "$PROJECT_ROOT" || exit 1

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 5

# 检查服务状态
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  服务启动完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "后端服务: ${GREEN}http://localhost:8000${NC} (PID: $BACKEND_PID)"
echo -e "前端服务: ${GREEN}http://localhost:5175${NC} (PID: $FRONTEND_PID)"
echo -e "API文档: ${GREEN}http://localhost:8000/api/docs${NC}"
echo ""
echo -e "${YELLOW}按 Ctrl+C 停止所有服务${NC}"

# 等待所有子进程
wait
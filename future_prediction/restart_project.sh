#!/bin/bash

# 使用绝对路径，确保在任何位置执行都能定位到项目
PROJECT_ROOT="/Users/colin/Documents/Quant_webui"
cd "$PROJECT_ROOT" || exit 1

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}正在准备重启项目...${NC}"

# 清理端口函数
cleanup_ports() {
    echo "正在检查并清理端口 8000 (后端) 和 5173 (前端)..."
    
    # 尝试杀掉占用 8000 端口的进程
    PID_8000=$(lsof -ti:8000)
    if [ -n "$PID_8000" ]; then
        echo -e "${RED}杀死占用端口 8000 的进程 (PID: $PID_8000)${NC}"
        kill -9 $PID_8000 2>/dev/null || echo "无法自动杀死进程，请手动检查。"
    fi

    # 尝试杀掉占用 5173 端口的进程
    PID_5173=$(lsof -ti:5173)
    if [ -n "$PID_5173" ]; then
        echo -e "${RED}杀死占用端口 5173 的进程 (PID: $PID_5173)${NC}"
        kill -9 $PID_5173 2>/dev/null || echo "无法自动杀死进程，请手动检查。"
    fi
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
# 后台运行前端
npm run dev &
FRONTEND_PID=$!
cd "$PROJECT_ROOT" || exit 1

echo -e "${GREEN}项目已启动!${NC}"
echo "后端运行在: http://localhost:8000 (PID: $BACKEND_PID)"
echo "前端运行在: http://localhost:5173 (PID: $FRONTEND_PID)"
echo "按 Ctrl+C 停止所有服务。"

# 等待所有子进程
wait
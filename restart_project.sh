#!/bin/bash

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
    if [ ! -z "$PID_8000" ]; then
        echo -e "${RED}杀死占用端口 8000 的进程 (PID: $PID_8000)${NC}"
        kill -9 $PID_8000 2>/dev/null || echo "无法自动杀死进程，请手动检查。"
    fi

    # 尝试杀掉占用 5173 端口的进程
    PID_5173=$(lsof -ti:5173)
    if [ ! -z "$PID_5173" ]; then
        echo -e "${RED}杀死占用端口 5173 的进程 (PID: $PID_5173)${NC}"
        kill -9 $PID_5173 2>/dev/null || echo "无法自动杀死进程，请手动检查。"
    fi
}

# 执行清理
cleanup_ports

# 捕获退出信号以清理子进程
trap 'kill $(jobs -p); exit' SIGINT SIGTERM

# 启动后端
echo -e "${GREEN}正在启动后端服务...${NC}"
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "警告: 未找到虚拟环境 venv，尝试直接运行 python"
fi

# 后台运行后端
python run_server.py &
BACKEND_PID=$!
cd ..

# 等待几秒确保后端开始初始化
sleep 3

# 启动前端
echo -e "${GREEN}正在启动前端服务...${NC}"
cd frontend
# 后台运行前端
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}项目已启动!${NC}"
echo "后端运行在: http://localhost:8000"
echo "前端运行在: http://localhost:5173"
echo "按 Ctrl+C 停止所有服务。"

# 等待所有子进程
wait



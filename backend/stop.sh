#!/bin/bash
# 停止后端服务器脚本

echo "正在查找并停止后端服务进程..."

# 查找占用8000端口的uvicorn进程
PIDS=$(lsof -ti :8000 2>/dev/null | xargs ps -p 2>/dev/null | grep uvicorn | awk '{print $1}' || lsof -ti :8000 2>/dev/null)

if [ -z "$PIDS" ]; then
    echo "未找到运行中的后端服务"
    exit 0
fi

# 停止所有相关进程
for PID in $PIDS; do
    if ps -p $PID > /dev/null 2>&1; then
        echo "正在停止进程 $PID..."
        kill $PID 2>/dev/null
        sleep 1
        # 如果还在运行，强制停止
        if ps -p $PID > /dev/null 2>&1; then
            echo "强制停止进程 $PID..."
            kill -9 $PID 2>/dev/null
        fi
    fi
done

sleep 1

# 验证端口是否已释放
if lsof -ti :8000 > /dev/null 2>&1; then
    echo "警告: 8000端口仍被占用"
    lsof -i :8000
else
    echo "后端服务已停止，8000端口已释放"
fi

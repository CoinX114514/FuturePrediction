#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}正在检查并清理本地服务...${NC}\n"

# 检查端口占用
echo "=== 端口占用情况 ==="
echo "5173 (前端):"
lsof -i :5173 | grep LISTEN || echo "  未占用"
echo "5174:"
lsof -i :5174 | grep LISTEN || echo "  未占用"
echo "5175:"
lsof -i :5175 | grep LISTEN || echo "  未占用"
echo "8000 (后端):"
lsof -i :8000 | grep LISTEN || echo "  未占用"

echo -e "\n=== 相关进程 ==="
echo "Vite 进程:"
ps aux | grep -E "vite|node.*dev" | grep -v grep || echo "  无"
echo "后端进程:"
ps aux | grep -E "python.*run_server|uvicorn" | grep -v grep || echo "  无"

echo -e "\n${YELLOW}是否要清理所有服务？(y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "\n${RED}正在清理...${NC}"
    
    # 清理前端
    pkill -f "vite" && echo "✓ 已停止 Vite 服务" || echo "  Vite 服务未运行"
    
    # 清理后端
    pkill -f "python.*run_server" && echo "✓ 已停止后端服务" || echo "  后端服务未运行"
    pkill -f "uvicorn" && echo "✓ 已停止 Uvicorn 进程" || echo "  Uvicorn 未运行"
    
    echo -e "\n${GREEN}清理完成！${NC}"
else
    echo "取消清理。"
fi


#!/bin/bash

# 快速同步脚本 - 将更改同步到 EC2 服务器
# 使用方法: ./sync_to_ec2.sh [EC2-IP] [用户名]

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 获取项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 默认配置
KEY_FILE="$PROJECT_DIR/future.pem"
USER_NAME=${2:-ec2-user}  # 默认为 ec2-user

# 检查密钥文件
if [ ! -f "$KEY_FILE" ]; then
    echo -e "${RED}错误: 密钥文件不存在: $KEY_FILE${NC}"
    exit 1
fi

# 设置密钥文件权限
chmod 400 "$KEY_FILE"

# 获取 EC2 IP
if [ -z "$1" ]; then
    echo -e "${YELLOW}请输入 EC2 服务器 IP 地址:${NC}"
    read -r EC2_IP
else
    EC2_IP=$1
fi

if [ -z "$EC2_IP" ]; then
    echo -e "${RED}错误: EC2 IP 地址不能为空${NC}"
    exit 1
fi

echo -e "${GREEN}开始同步到 EC2 服务器: $EC2_IP${NC}"

# 使用 rsync 同步文件（排除不必要的文件）
echo -e "${YELLOW}同步项目文件...${NC}"
rsync -avz \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='.venv' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='.env.local' \
    --exclude='dist' \
    --exclude='build' \
    --exclude='.vite' \
    --exclude='uploads' \
    --exclude='temp' \
    --exclude='*.log' \
    --exclude='*.pem' \
    --exclude='*.tar' \
    --exclude='*.tar.gz' \
    --exclude='*.zip' \
    --exclude='future_prediction' \
    --exclude='tushare_*.csv' \
    --exclude='tushare_*.md' \
    -e "ssh -i $KEY_FILE" \
    "$PROJECT_DIR/" "$USER_NAME@$EC2_IP:~/app/"

echo -e "${GREEN}文件同步完成！${NC}"

# 询问是否在服务器上执行部署
echo -e "${YELLOW}是否在服务器上执行部署？(y/n)${NC}"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}在服务器上执行部署...${NC}"
    ssh -i "$KEY_FILE" "$USER_NAME@$EC2_IP" << 'EOF'
        cd ~/app
        
        # 检查 Docker 是否运行
        if ! sudo systemctl is-active --quiet docker; then
            echo "启动 Docker 服务..."
            sudo service docker start
        fi
        
        # 停止现有服务
        if [ -f "docker-compose.yml" ]; then
            echo "停止现有服务..."
            docker compose down || true
        fi
        
        # 构建并启动服务
        echo "构建并启动 Docker 服务..."
        docker compose up -d --build
        
        # 等待服务启动
        sleep 10
        
        # 显示服务状态
        echo "服务状态:"
        docker compose ps
        
        echo "部署完成！"
EOF
    echo -e "${GREEN}部署完成！${NC}"
else
    echo -e "${YELLOW}文件已同步，但未执行部署。${NC}"
    echo -e "${YELLOW}您可以手动 SSH 到服务器执行部署:${NC}"
    echo "  ssh -i $KEY_FILE $USER_NAME@$EC2_IP"
    echo "  cd ~/app && docker compose up -d --build"
fi

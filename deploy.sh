#!/bin/bash

# 部署脚本 - 用于将项目打包并上传到 AWS EC2
# 使用方法: ./deploy.sh <EC2-IP> <密钥文件路径> [用户名]

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -lt 2 ]; then
    echo -e "${RED}错误: 缺少必要参数${NC}"
    echo "使用方法: $0 <EC2-IP> <密钥文件路径> [用户名]"
    echo "示例: $0 1.2.3.4 ~/Downloads/my-key.pem ec2-user"
    exit 1
fi

EC2_IP=$1
KEY_FILE=$2
USER_NAME=${3:-ec2-user}  # 默认为 ec2-user，Ubuntu 系统使用 ubuntu

echo -e "${GREEN}开始部署流程...${NC}"

# 检查密钥文件是否存在
if [ ! -f "$KEY_FILE" ]; then
    echo -e "${RED}错误: 密钥文件不存在: $KEY_FILE${NC}"
    exit 1
fi

# 设置密钥文件权限
echo -e "${YELLOW}设置密钥文件权限...${NC}"
chmod 400 "$KEY_FILE"

# 获取项目根目录
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# 创建临时目录用于打包
TEMP_DIR=$(mktemp -d)
echo -e "${YELLOW}创建临时目录: $TEMP_DIR${NC}"

# 复制项目文件（排除不必要的文件）
echo -e "${YELLOW}打包项目文件...${NC}"
rsync -av \
    --exclude='node_modules' \
    --exclude='venv' \
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
    "$PROJECT_DIR/" "$TEMP_DIR/"

# 压缩项目（排除自身归档，避免 tar 递归包含）
ARCHIVE_NAME="project-$(date +%Y%m%d-%H%M%S).tar.gz"
ARCHIVE_PATH="$TEMP_DIR/$ARCHIVE_NAME"
echo -e "${YELLOW}压缩项目文件...${NC}"
cd "$TEMP_DIR"
tar --exclude="$ARCHIVE_NAME" --exclude='project-*.tar.gz' -czf "$ARCHIVE_NAME" .

# 上传到 EC2
echo -e "${YELLOW}上传到 EC2 服务器 ($EC2_IP)...${NC}"
scp -i "$KEY_FILE" "$ARCHIVE_NAME" "$USER_NAME@$EC2_IP:~/"

# 清理临时目录
rm -rf "$TEMP_DIR"

echo -e "${GREEN}上传完成！${NC}"
echo -e "${YELLOW}现在请 SSH 连接到服务器并运行部署脚本:${NC}"
echo "  ssh -i $KEY_FILE $USER_NAME@$EC2_IP"
echo "  ./deploy-on-server.sh $ARCHIVE_NAME"

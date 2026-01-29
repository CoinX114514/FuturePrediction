#!/bin/bash

# 服务器端部署脚本 - 在 EC2 实例上执行
# 使用方法: ./deploy-on-server.sh [压缩包名称]

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否提供了压缩包名称
if [ $# -eq 0 ]; then
    # 如果没有提供，查找最新的压缩包
    ARCHIVE_NAME=$(ls -t project-*.tar.gz 2>/dev/null | head -n 1)
    if [ -z "$ARCHIVE_NAME" ]; then
        echo -e "${RED}错误: 找不到项目压缩包${NC}"
        echo "请先上传项目压缩包，或指定压缩包名称"
        exit 1
    fi
    echo -e "${YELLOW}使用最新的压缩包: $ARCHIVE_NAME${NC}"
else
    ARCHIVE_NAME=$1
fi

# 检查压缩包是否存在
if [ ! -f "$ARCHIVE_NAME" ]; then
    echo -e "${RED}错误: 压缩包不存在: $ARCHIVE_NAME${NC}"
    exit 1
fi

echo -e "${GREEN}开始服务器端部署...${NC}"

# 创建应用目录（如果不存在）
APP_DIR="$HOME/app"
if [ -d "$APP_DIR" ]; then
    echo -e "${YELLOW}备份现有应用目录...${NC}"
    BACKUP_DIR="$HOME/app-backup-$(date +%Y%m%d-%H%M%S)"
    mv "$APP_DIR" "$BACKUP_DIR"
    echo -e "${GREEN}备份完成: $BACKUP_DIR${NC}"
fi

mkdir -p "$APP_DIR"
cd "$APP_DIR"

# 解压项目文件
echo -e "${YELLOW}解压项目文件...${NC}"
tar -xzf "$HOME/$ARCHIVE_NAME"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装${NC}"
    echo "请先安装 Docker:"
    echo "  sudo yum update -y"
    echo "  sudo yum install -y docker"
    echo "  sudo service docker start"
    echo "  sudo usermod -a -G docker $USER"
    exit 1
fi

# 检查 Docker Compose 是否可用
if ! docker compose version &> /dev/null; then
    echo -e "${YELLOW}安装 Docker Compose 插件...${NC}"
    sudo yum install docker-compose-plugin -y
fi

# 确保当前用户在 docker 组中
if ! groups | grep -q docker; then
    echo -e "${YELLOW}将当前用户添加到 docker 组...${NC}"
    sudo usermod -a -G docker $USER
    echo -e "${YELLOW}请重新登录以使组更改生效，然后重新运行此脚本${NC}"
    exit 1
fi

# 启动 Docker 服务（如果未运行）
if ! sudo systemctl is-active --quiet docker; then
    echo -e "${YELLOW}启动 Docker 服务...${NC}"
    sudo service docker start
fi

# 停止现有服务（如果存在）
if [ -f "docker-compose.yml" ]; then
    echo -e "${YELLOW}停止现有服务...${NC}"
    docker compose down || true
fi

# 提醒：K 线、现价依赖 Tushare，需在应用目录创建 .env 并设置 TUSHARE_TOKEN
if [ ! -f ".env" ] || ! grep -q "TUSHARE_TOKEN=.\+" .env 2>/dev/null; then
    echo -e "${YELLOW}提示: 若需帖子内 K 线图与现价，请在 $APP_DIR 创建 .env 并设置 TUSHARE_TOKEN=你的Token${NC}"
    echo -e "${YELLOW}  例如: echo 'TUSHARE_TOKEN=xxx' > .env${NC}"
fi

# 构建并启动服务
echo -e "${YELLOW}构建并启动 Docker 服务...${NC}"
echo -e "${YELLOW}这可能需要几分钟时间，请耐心等待...${NC}"
docker compose up -d --build

# 等待服务启动
echo -e "${YELLOW}等待服务启动...${NC}"
sleep 10

# 检查服务状态
echo -e "${GREEN}检查服务状态...${NC}"
docker compose ps

# 显示日志（最后 50 行）
echo -e "${GREEN}服务日志（最后 50 行）:${NC}"
docker compose logs --tail=50

echo -e "${GREEN}部署完成！${NC}"
echo -e "${YELLOW}服务应该可以通过以下地址访问:${NC}"
echo "  http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'YOUR-EC2-IP')"
echo ""
echo -e "${YELLOW}常用命令:${NC}"
echo "  查看日志: docker compose logs -f"
echo "  停止服务: docker compose down"
echo "  重启服务: docker compose restart"
echo "  查看状态: docker compose ps"

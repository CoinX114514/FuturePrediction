#!/usr/bin/env bash
#
# 将本地 Quant_webui 同步到阿里云 ECS，并在远端用 Docker Compose 构建并启动前后端+Nginx+数据库。
# 使用 SSH ControlMaster：第一次连接时只需输入一次密码，后续 rsync 与同套接字的 ssh 复用该连接。
#
set -euo pipefail

# 远端主机（可通过环境变量覆盖）
REMOTE_HOST="${REMOTE_HOST:-47.238.72.203}"
# 远端 SSH 用户
REMOTE_USER="${REMOTE_USER:-root}"
# 远端项目目录
REMOTE_DIR="${REMOTE_DIR:-/root/Quant_webui}"
# 本地仓库根目录（脚本在 scripts/ 下）
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# SSH 控制套接字路径（用于连接复用）
SSH_CONTROL_DIR="${HOME}/.ssh"
SSH_CONTROL_SOCKET="${SSH_CONTROL_DIR}/cm-quant-%r@%h:%p"

mkdir -p "${SSH_CONTROL_DIR}"
chmod 700 "${SSH_CONTROL_DIR}" 2>/dev/null || true

cleanup() {
  ssh -S "${SSH_CONTROL_SOCKET}" -O exit "${REMOTE_USER}@${REMOTE_HOST}" 2>/dev/null || true
}
trap cleanup EXIT

echo "==> 建立 SSH 控制连接（请输入一次 root 密码）..."
ssh -MNf \
  -o ControlMaster=yes \
  -o ControlPath="${SSH_CONTROL_SOCKET}" \
  -o ControlPersist=300 \
  -o StrictHostKeyChecking=accept-new \
  "${REMOTE_USER}@${REMOTE_HOST}"

echo "==> rsync 同步到 ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}（排除 node_modules 等，加快上传）..."
rsync -avz \
  --exclude 'node_modules' \
  --exclude '__pycache__' \
  --exclude '.git' \
  --exclude 'frontend/dist' \
  --exclude '.vite' \
  --exclude 'FuturePrediction-main' \
  --exclude '.cursor' \
  --exclude '*.pyc' \
  -e "ssh -S ${SSH_CONTROL_SOCKET}" \
  "${LOCAL_DIR}/" "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"

echo "==> 远端：检查 Docker / Compose，构建并启动服务..."
ssh -S "${SSH_CONTROL_SOCKET}" "${REMOTE_USER}@${REMOTE_HOST}" \
  REMOTE_DIR="${REMOTE_DIR}" \
  bash -s <<'REMOTE_SCRIPT'
set -euo pipefail
cd "${REMOTE_DIR}"

if ! command -v docker >/dev/null 2>&1; then
  echo ">>> 未检测到 docker，正在安装 docker.io 与 docker-compose-v2 ..."
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -qq
  apt-get install -y docker.io docker-compose-v2
fi

systemctl enable docker >/dev/null 2>&1 || true
systemctl start docker >/dev/null 2>&1 || true

if [ ! -f .env ]; then
  echo ">>> 警告：远端缺少 .env，docker-compose 可能失败。请从本机复制 .env 或手动创建。"
  exit 1
fi

echo ">>> docker compose build（首次或依赖变更会较久）..."
docker compose build

echo ">>> docker compose up -d"
docker compose up -d

echo ">>> 容器状态："
docker compose ps
REMOTE_SCRIPT

echo "==> 完成。浏览器访问: http://${REMOTE_HOST}/ （确保阿里云安全组已放行 TCP 80）"

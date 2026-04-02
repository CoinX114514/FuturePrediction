#!/usr/bin/env bash
# 一键同步代码到 EC2 并重建/启动 Docker。
# 用法（在本机仓库根目录或任意目录）：
#   chmod +x scripts/deploy_ec2.sh
#   PEM=~/Documents/Quant_webui/future.pem HOST=ubuntu@54.95.187.92 ./scripts/deploy_ec2.sh
#
# 若 SSH 报 “banner exchange” 超时：在安全组放行本机 IP、检查实例负载、或稍后重试。
# 云端行情：MARKET_DATA_SOURCE=json|tushare；json 时维护 MARKET_DATA_JSON；tushare 需 TUSHARE_TOKEN（东京常超时则回退 JSON）。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PEM="${PEM:-$REPO_ROOT/future.pem}"
HOST="${HOST:-ubuntu@54.95.187.92}"

if [[ ! -f "$PEM" ]]; then
  echo "找不到密钥: $PEM （可 export PEM=/path/to/future.pem）"
  exit 1
fi

chmod 600 "$PEM" 2>/dev/null || true

echo "==> rsync 到 $HOST:~/app（排除 .env / node_modules）"
rsync -avz \
  --exclude 'node_modules' \
  --exclude '.git' \
  --exclude '.env' \
  --exclude 'FuturePrediction-main' \
  --exclude 'future_prediction' \
  --exclude '__pycache__' \
  --exclude '*.pyc' \
  --exclude 'venv' \
  --exclude 'dist' \
  -e "ssh -i $PEM -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30" \
  "$REPO_ROOT/" \
  "$HOST:~/app/"

echo "==> docker compose build + up"
ssh -i "$PEM" -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=30 "$HOST" \
  'cd ~/app && docker compose build backend frontend nginx && docker compose up -d'

echo "==> 本机探活（须在服务器上监听 80）"
ssh -i "$PEM" -o ConnectTimeout=15 "$HOST" \
  'curl -s "http://127.0.0.1/api/health"; echo; curl -s -o /dev/null -w "kline_http=%{http_code}\n" "http://127.0.0.1/api/v1/kline/TL2603?period=365" --max-time 30'

echo "==> 完成"

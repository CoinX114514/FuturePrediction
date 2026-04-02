#!/usr/bin/env bash
#
# 在阿里云 ECS 上执行 sync_tushare_futures_to_db.py：
# 用 fut_mapping 取各品种当前主力月合约，每个「交易所+品种」仅一帖，换月时更新同帖 contract_code。
#
# 前置：ECS 上项目已部署；backend 容器内可访问数据库；环境变量 TUSHARE_TOKEN 已配置（.env 注入 compose）。
#
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-47.238.72.203}"
REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_DIR="${REMOTE_DIR:-/root/Quant_webui}"

echo "==> SSH 到 ${REMOTE_USER}@${REMOTE_HOST}，在 ${REMOTE_DIR} 执行期货帖子同步..."
ssh "${REMOTE_USER}@${REMOTE_HOST}" \
  "cd ${REMOTE_DIR} && docker compose exec -T backend python sync_tushare_futures_to_db.py"

echo "==> 完成（日志在上方；Tushare 需积分与有效 Token）。"

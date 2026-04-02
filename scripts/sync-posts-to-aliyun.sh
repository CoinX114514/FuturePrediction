#!/usr/bin/env bash
#
# 将本机 Docker Compose 中「帖子相关表」的数据导出并恢复到阿里云 ECS 上的同一数据库。
#
# 包含表：posts, likes, collections, browse_histories, drafts（与帖子/草稿及互动直接相关）。
#
# 设计原因：
# - 帖子行引用 users.author_id、sectors.sector_id；若云端不存在对应 user_id，pg_restore 会因外键失败。
#   请先在云端同步用户（如 create_test_users）或保证两端用户 id 一致（例如都做完整库同步后再增量）。
# - 恢复前会 TRUNCATE 上述表（RESTART IDENTITY），云端这些表上的旧数据会被清空后再写入本机数据。
# - 只 stop backend（连库的应用容器）；nginx/frontend 保持运行。收尾用 bring_up_stack，不吞掉 docker 错误。
#
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-47.238.72.203}"
REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_DIR="${REMOTE_DIR:-/root/Quant_webui}"
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE_DUMP_NAME="posts_only_data.sync.dump"

SSH_CONTROL_DIR="${HOME}/.ssh"
SSH_CONTROL_SOCKET="${SSH_CONTROL_DIR}/cm-quant-posts-%r@%h:%p"

mkdir -p "${SSH_CONTROL_DIR}"
chmod 700 "${SSH_CONTROL_DIR}" 2>/dev/null || true

cleanup() {
  rm -f "${DUMP_FILE:-}"
  ssh -S "${SSH_CONTROL_SOCKET}" -O exit "${REMOTE_USER}@${REMOTE_HOST}" 2>/dev/null || true
}
trap cleanup EXIT

DUMP_FILE="$(mktemp -t quant-posts-XXXXXX.dump)"

echo "==> 本机：导出帖子相关表（仅数据，-Fc）..."
cd "${LOCAL_DIR}"
if ! docker compose exec -T db pg_isready -U postgres >/dev/null 2>&1; then
  echo "错误：本机 db 不可用。请先: docker compose up -d db"
  exit 1
fi

docker compose exec -T db pg_dump -U postgres -d futures_trading \
  --data-only -Fc \
  -t posts \
  -t likes \
  -t collections \
  -t browse_histories \
  -t drafts \
  > "${DUMP_FILE}"

echo "    导出完成，大小: $(du -h "${DUMP_FILE}" | cut -f1)"

echo "==> 建立 SSH 控制连接（请输入一次 root 密码）..."
ssh -MNf \
  -o ControlMaster=yes \
  -o ControlPath="${SSH_CONTROL_SOCKET}" \
  -o ControlPersist=300 \
  -o StrictHostKeyChecking=accept-new \
  "${REMOTE_USER}@${REMOTE_HOST}"

echo "==> 上传 dump 到 ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/"
rsync -avz \
  -e "ssh -S ${SSH_CONTROL_SOCKET}" \
  "${DUMP_FILE}" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_DIR}/${REMOTE_DUMP_NAME}"

echo "==> 远端：清空帖子相关表并恢复数据 ..."
ssh -S "${SSH_CONTROL_SOCKET}" "${REMOTE_USER}@${REMOTE_HOST}" \
  REMOTE_DIR="${REMOTE_DIR}" \
  REMOTE_DUMP_NAME="${REMOTE_DUMP_NAME}" \
  bash -s <<'REMOTE_SCRIPT'
set -euo pipefail
cd "${REMOTE_DIR}"
export REMOTE_DIR

bring_up_stack() {
  cd "${REMOTE_DIR}" || { echo ">>> [收尾] cd 失败: ${REMOTE_DIR}"; return 1; }
  echo ">>> [收尾] docker compose up -d（拉回 backend 等）..."
  docker compose up -d
  docker compose ps -a
}
trap 'bring_up_stack' EXIT

if [ ! -f docker-compose.yml ]; then
  echo "错误：${REMOTE_DIR} 下没有 docker-compose.yml"
  exit 1
fi

if [ ! -f "${REMOTE_DUMP_NAME}" ]; then
  echo "错误：找不到 ${REMOTE_DUMP_NAME}"
  exit 1
fi

echo ">>> 仅停止 backend（释放数据库连接），nginx/frontend 保持运行"
docker compose stop backend 2>/dev/null || true
docker compose up -d db

echo ">>> 等待 Postgres 就绪..."
for _ in $(seq 1 30); do
  if docker compose exec -T db pg_isready -U postgres >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

echo ">>> TRUNCATE 帖子相关表（清空云端旧帖与草稿、点赞收藏浏览记录）..."
docker compose exec -T db psql -U postgres -d futures_trading -v ON_ERROR_STOP=1 <<'SQL'
-- 草稿仅依赖 users；先清空避免与帖子/CASCADE 顺序纠缠
TRUNCATE TABLE drafts RESTART IDENTITY;
-- 帖子及其外键指向它的 likes / collections / browse_histories 一并清空
TRUNCATE TABLE posts RESTART IDENTITY CASCADE;
SQL

docker compose cp "${REMOTE_DUMP_NAME}" db:/tmp/posts_restore.dump

set +e
docker compose exec -T db pg_restore \
  -U postgres \
  -d futures_trading \
  --data-only \
  --no-owner \
  --no-acl \
  /tmp/posts_restore.dump
restore_rc=$?
set -euo pipefail
if [ "${restore_rc}" -ne 0 ] && [ "${restore_rc}" -ne 1 ]; then
  echo ">>> pg_restore 失败，退出码: ${restore_rc}"
  exit "${restore_rc}"
fi

docker compose exec -T db rm -f /tmp/posts_restore.dump
rm -f "${REMOTE_DUMP_NAME}"

echo ">>> 修正序列，避免自增主键冲突 ..."
docker compose exec -T db psql -U postgres -d futures_trading -v ON_ERROR_STOP=1 <<'SQL'
SELECT setval(pg_get_serial_sequence('posts', 'post_id'), COALESCE((SELECT MAX(post_id) FROM posts), 0) + 1, false);
SELECT setval(pg_get_serial_sequence('likes', 'like_id'), COALESCE((SELECT MAX(like_id) FROM likes), 0) + 1, false);
SELECT setval(pg_get_serial_sequence('collections', 'collection_id'), COALESCE((SELECT MAX(collection_id) FROM collections), 0) + 1, false);
SELECT setval(pg_get_serial_sequence('browse_histories', 'history_id'), COALESCE((SELECT MAX(history_id) FROM browse_histories), 0) + 1, false);
SELECT setval(pg_get_serial_sequence('drafts', 'draft_id'), COALESCE((SELECT MAX(draft_id) FROM drafts), 0) + 1, false);
SQL

echo ">>> 帖子数据已写入，正在拉回 backend 等容器"
trap - EXIT
bring_up_stack

echo ">>> 帖子同步完成"
REMOTE_SCRIPT

echo "==> 完成。请在云端验证帖子列表与作者是否正确。"

#!/usr/bin/env bash
#
# 将「本机 Docker Compose 中的 PostgreSQL（futures_trading）」导出并恢复到阿里云 ECS 上
# 同名 compose 项目里的 db 容器。
#
# 前置条件（全部在 Mac 本机满足即可）：
# - 已在项目根目录通过 docker compose 启动过数据库（服务名 db 可访问）
# - 远端 /root/Quant_webui 已部署且可 docker compose（与 deploy-aliyun.sh 一致）
#
# 说明：数据在 Docker 卷里，不参与 rsync；必须用 pg_dump / pg_restore 迁数据。
# 恢复前只停 backend（释放 Postgres 连接）；nginx/frontend 保持运行，减少整站不可用时间。
# 收尾用 bring_up_stack + EXIT trap，且不再隐藏 docker compose 失败信息。
#
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-47.238.72.203}"
REMOTE_USER="${REMOTE_USER:-root}"
REMOTE_DIR="${REMOTE_DIR:-/root/Quant_webui}"
LOCAL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REMOTE_DUMP_NAME="postgres_futures_trading.sync.dump"

SSH_CONTROL_DIR="${HOME}/.ssh"
SSH_CONTROL_SOCKET="${SSH_CONTROL_DIR}/cm-quant-db-%r@%h:%p"

mkdir -p "${SSH_CONTROL_DIR}"
chmod 700 "${SSH_CONTROL_DIR}" 2>/dev/null || true

cleanup() {
  rm -f "${DUMP_FILE:-}"
  ssh -S "${SSH_CONTROL_SOCKET}" -O exit "${REMOTE_USER}@${REMOTE_HOST}" 2>/dev/null || true
}
trap cleanup EXIT

DUMP_FILE="$(mktemp -t quant-pg-XXXXXX.dump)"

echo "==> 本机：从 db 容器导出 futures_trading（自定义格式 -Fc）..."
cd "${LOCAL_DIR}"
if ! docker compose exec -T db pg_isready -U postgres >/dev/null 2>&1; then
  echo "错误：本机 db 容器不可用或未就绪。"
  echo "请先在 ${LOCAL_DIR} 执行: docker compose up -d db"
  exit 1
fi

docker compose exec -T db pg_dump -U postgres -Fc futures_trading > "${DUMP_FILE}"
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

echo "==> 远端：停止占用数据库的服务并执行 pg_restore ..."
ssh -S "${SSH_CONTROL_SOCKET}" "${REMOTE_USER}@${REMOTE_HOST}" \
  REMOTE_DIR="${REMOTE_DIR}" \
  REMOTE_DUMP_NAME="${REMOTE_DUMP_NAME}" \
  bash -s <<'REMOTE_SCRIPT'
set -euo pipefail
cd "${REMOTE_DIR}"
export REMOTE_DIR

# 无论正常结束还是中途 set -e 退出，都执行一次 up -d，且不隐藏失败信息。
bring_up_stack() {
  cd "${REMOTE_DIR}" || { echo ">>> [收尾] cd 失败: ${REMOTE_DIR}"; return 1; }
  echo ">>> [收尾] docker compose up -d（拉回 backend 等）..."
  docker compose up -d
  docker compose ps -a
}
trap 'bring_up_stack' EXIT

if [ ! -f docker-compose.yml ]; then
  echo "错误：${REMOTE_DIR} 下没有 docker-compose.yml，请先部署代码。"
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
for i in $(seq 1 30); do
  if docker compose exec -T db pg_isready -U postgres >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

docker compose cp "${REMOTE_DUMP_NAME}" db:/tmp/pg_restore.dump

# --no-owner --no-acl：避免本机/远端角色名不一致导致失败
# pg_restore 在仅有警告时可能返回 1，仍视为成功
set +e
docker compose exec -T db pg_restore \
  -U postgres \
  -d futures_trading \
  --clean \
  --if-exists \
  --no-owner \
  --no-acl \
  /tmp/pg_restore.dump
restore_rc=$?
set -euo pipefail
if [ "${restore_rc}" -ne 0 ] && [ "${restore_rc}" -ne 1 ]; then
  echo ">>> pg_restore 失败，退出码: ${restore_rc}"
  exit "${restore_rc}"
fi

docker compose exec -T db rm -f /tmp/pg_restore.dump
rm -f "${REMOTE_DUMP_NAME}"

echo ">>> 数据库恢复步骤已完成，正在拉回 backend 等容器"
trap - EXIT
bring_up_stack

echo ">>> 恢复完成"
REMOTE_SCRIPT

echo "==> 数据库已同步到 ${REMOTE_HOST}，可通过站点验证数据是否正确。"

# EC2 上「更新帖子」返回 404 的排查与修复

## 原因说明

接口 `PUT /api/v1/posts/{post_id}` 返回 **404（帖子不存在或无权编辑）** 时，通常是：

1. **EC2 上的后端未更新**  
   旧逻辑要求「只有帖子作者本人」才能编辑。若当前登录的是超级管理员但不是该帖作者，`post_service.update_post` 会返回 `None`，路由就会返回 404。  
   **修复**：在 EC2 上重新部署**最新后端**（含「管理员可编辑任意帖子」的改动）。

2. **帖子不存在或已删除**  
   若 `post_id` 在数据库中不存在，或该帖 `status != 1`（已软删除），也会返回 404。  
   **修复**：确认该帖子在 EC2 数据库中存在且 `status = 1`。

## 操作步骤（推荐）

在 EC2 上拉取最新代码并重新构建、启动后端：

```bash
# 在项目根目录
git pull   # 或把你的最新代码同步上去

# 只重新构建并启动后端（保证用到最新 post_service 等逻辑）
docker compose build backend --no-cache
docker compose up -d backend
```

若你是一台机器上同时跑前后端，也可以整体重建并启动：

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

## 验证

- 用**超级管理员**账号登录，打开任意一篇帖子（不必是本人发的），点击「编辑帖子」并保存。  
- 若仍返回 404，查看后端日志：  
  `docker compose logs backend --tail=100`  
  确认请求是否到达、是否有权限或数据库相关报错。

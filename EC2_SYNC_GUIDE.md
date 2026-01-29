# EC2 同步指南

## 快速同步

使用快速同步脚本（推荐）：

```bash
./sync_to_ec2.sh [EC2-IP] [用户名]
```

示例：
```bash
./sync_to_ec2.sh 1.2.3.4 ec2-user
```

如果不提供参数，脚本会提示您输入 EC2 IP 地址。

## 完整部署流程

如果需要完整部署（包括打包和上传）：

```bash
./deploy.sh <EC2-IP> <密钥文件路径> [用户名]
```

示例：
```bash
./deploy.sh 1.2.3.4 ./future.pem ec2-user
```

然后 SSH 到服务器执行部署：
```bash
ssh -i future.pem ec2-user@1.2.3.4
./deploy-on-server.sh
```

## 同步的内容

脚本会自动排除以下文件/目录：
- `node_modules` - Node.js 依赖（服务器上会重新安装）
- `venv` / `.venv` - Python 虚拟环境（服务器上会重新创建）
- `.git` - Git 仓库
- `__pycache__` / `*.pyc` - Python 缓存文件
- `.env` / `.env.local` - 环境变量文件（不会覆盖服务器上的配置）
- `dist` / `build` - 构建产物
- `*.log` - 日志文件
- `future_prediction` - 其他项目目录

## 重要提示

1. **环境变量**: 确保服务器上的 `.env` 文件包含正确的配置，特别是：
   - `TUSHARE_TOKEN` - Tushare API Token
   - `DATABASE_URL` - 数据库连接字符串
   - 其他必要的环境变量

2. **数据库迁移**: 如果数据库结构有变化，需要在服务器上执行迁移：
   ```bash
   ssh -i future.pem ec2-user@EC2-IP
   cd ~/app/backend
   # 执行数据库迁移或同步脚本
   python sync_tushare_futures_to_db.py
   ```

3. **依赖更新**: 如果添加了新的 Python 依赖，需要更新 `requirements.txt`，然后重新构建 Docker 镜像。

4. **服务重启**: 同步后，Docker 容器会自动重新构建和启动。如果需要手动重启：
   ```bash
   docker compose restart
   ```

## 故障排除

### 连接失败
- 检查 EC2 安全组是否允许 SSH 访问（端口 22）
- 检查密钥文件权限：`chmod 400 future.pem`
- 确认 EC2 IP 地址正确

### 部署失败
- 检查 Docker 是否运行：`sudo systemctl status docker`
- 查看日志：`docker compose logs`
- 检查磁盘空间：`df -h`

### 服务无法访问
- 检查安全组是否允许 HTTP/HTTPS 访问（端口 80/443）
- 检查 Nginx 配置：`docker compose logs nginx`
- 检查服务状态：`docker compose ps`

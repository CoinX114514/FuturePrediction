# 前端 Dockerfile
# 支持开发和生产两种模式

FROM node:20-alpine AS builder

# 构建阶段：安装依赖并构建生产版本
WORKDIR /usr/src/app

# 复制 package 文件并安装依赖
COPY frontend/package*.json ./
RUN npm ci --only=production=false

# 复制前端源代码
COPY frontend /usr/src/app

# 构建生产版本（静态文件）
# 注意：这里需要设置 VITE_API_BASE_URL 环境变量，因为前端需要知道 API 地址
# 在生产环境中，API 请求会通过 Nginx 代理，所以使用相对路径即可
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# 生产阶段：使用 Nginx 提供静态文件服务
FROM nginx:alpine

# 复制构建好的静态文件到 Nginx 默认目录
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

# 复制自定义 Nginx 配置（用于前端路由支持）
RUN echo 'server { \
    listen 80; \
    server_name _; \
    root /usr/share/nginx/html; \
    index index.html; \
    location / { \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]

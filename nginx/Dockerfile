# Nginx Dockerfile
# 用于提供反向代理服务

FROM nginx:alpine

# 复制 Nginx 配置文件
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# 暴露 80 端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]

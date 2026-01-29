# 使用可配置的 Node 基础镜像，方便切换镜像源
ARG NODE_BASE=node:20-alpine
FROM ${NODE_BASE}

WORKDIR /usr/src/app

COPY frontend/package*.json ./
RUN npm install

COPY frontend /usr/src/app

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]

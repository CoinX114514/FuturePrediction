# 使用可配置的基础镜像以便在国内环境中切换为镜像源
ARG PYTHON_BASE=python:3.11-slim
FROM ${PYTHON_BASE}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend /opt/app

EXPOSE 8000

# 使用模块方式运行数据库初始化脚本，确保可以正确找到 app 包
CMD ["sh", "-c", "python -m app.database.init_db && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

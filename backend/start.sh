#!/bin/bash
# 后端服务器启动脚本
# 自动激活虚拟环境并启动 FastAPI 服务器

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "已激活虚拟环境"
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "已激活虚拟环境"
else
    echo "错误: 未找到虚拟环境目录 (venv 或 .venv)"
    exit 1
fi

# 检查依赖是否安装
if ! python -c "import uvicorn" 2>/dev/null; then
    echo "警告: uvicorn 未安装，正在安装依赖..."
    pip install -r requirements.txt
fi

# 启动服务器
echo "正在启动后端服务器..."
python run_server.py

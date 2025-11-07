# 快速开始指南

## 前置要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

## 快速启动步骤

### 1. 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run_server.py
```

后端将在 `http://localhost:8000` 运行

### 2. 启动前端

打开新的终端窗口：

```bash
cd frontend
npm install
npm run dev
```

前端将在 `http://localhost:5173` 运行

### 3. 使用应用

1. 打开浏览器访问 `http://localhost:5173`
2. 上传 CSV 文件（参考 `example_data.csv` 格式）
3. 选择预测天数
4. 点击"开始预测"
5. 查看预测结果和图表

## 测试 CSV 文件

可以使用 `example_data.csv` 文件进行测试。

## 注意事项

- 确保后端服务正在运行（端口 8000）
- 确保前端可以访问后端 API（CORS 已配置）
- 如果模型未加载，将使用模拟预测模式

## 故障排除

### 后端启动失败
- 检查 Python 版本：`python --version`
- 检查端口 8000 是否被占用
- 检查依赖是否安装完整：`pip list`

### 前端启动失败
- 检查 Node.js 版本：`node --version`
- 检查端口 5173 是否被占用
- 删除 `node_modules` 并重新安装：`rm -rf node_modules && npm install`

### 文件上传失败
- 检查 CSV 文件格式是否正确
- 检查文件是否包含必需的列
- 查看浏览器控制台的错误信息


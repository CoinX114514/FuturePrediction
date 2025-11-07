# 期货价格趋势预测 Web 应用 - 完整计划

## 项目概述

这是一个基于预训练 Kronos 模型的 MVP Web 应用，允许用户上传 OHLCV CSV 数据并预测未来每日期货价格趋势。

## 技术架构

### 后端（FastAPI）
- **框架**: FastAPI - 现代、快速的 Python Web 框架
- **数据处理**: Pandas, NumPy
- **模型推理**: 根据 Kronos 模型需求（PyTorch/TensorFlow）
- **API 文档**: 自动生成的 Swagger UI（`/api/docs`）

### 前端（React + TypeScript）
- **框架**: React 18 + TypeScript
- **构建工具**: Vite
- **样式**: Tailwind CSS
- **图表**: Recharts
- **文件上传**: react-dropzone

## 项目结构

```
Quant_webui/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── main.py         # FastAPI 主应用
│   │   ├── routers/        # API 路由
│   │   │   ├── upload.py   # 文件上传路由
│   │   │   └── prediction.py # 预测路由
│   │   ├── services/       # 业务逻辑
│   │   │   ├── csv_parser.py      # CSV 解析
│   │   │   ├── data_validator.py  # 数据验证
│   │   │   └── model_inference.py  # 模型推理
│   │   └── models/         # 数据模型
│   ├── models/             # 预训练模型文件（kronos）
│   ├── uploads/            # 上传文件存储
│   ├── requirements.txt
│   └── run_server.py       # 启动脚本
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/     # React 组件
│   │   │   ├── FileUpload.tsx
│   │   │   ├── PredictionResults.tsx
│   │   │   └── Chart.tsx
│   │   ├── services/       # API 服务
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## 功能特性

### ✅ 已实现
1. **多种数据来源支持**
   - **CSV 文件上传**：支持拖拽上传，文件格式验证
   - **Tushare 数据获取**：直接通过期货合约代码获取数据
   - 数据源切换：选项卡式界面，轻松切换数据来源

2. **Tushare 集成**
   - 期货合约代码输入和验证
   - 合约搜索功能
   - 自动数据获取和验证
   - 支持所有主要期货交易所

3. **CSV 数据验证**
   - 自动识别中英文列名
   - 数据完整性检查
   - 价格逻辑验证（最高 >= 最低等）
   - 详细的错误提示

4. **预测功能**
   - 可配置预测天数（1-30 天）
   - 趋势方向判断（上涨/下跌/震荡）
   - 置信度计算

5. **数据可视化**
   - 交互式趋势图表
   - 预测值详细展示
   - 响应式设计

6. **中文界面**
   - 完整的中文用户界面
   - 中文错误提示
   - 中文 API 文档

7. **代码质量**
   - Google 风格注释
   - TypeScript 类型安全
   - 完整的错误处理

## 安装和运行

### 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置 Tushare Token（可选，如果使用 Tushare 功能）
export TUSHARE_TOKEN="your_token_here"  # Linux/Mac
# 或
set TUSHARE_TOKEN=your_token_here  # Windows

# 启动服务器
python run_server.py
# 或
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端将在 `http://localhost:8000` 运行
API 文档：`http://localhost:8000/api/docs`

**注意**：如果使用 Tushare 功能，需要先配置 TUSHARE_TOKEN。详细说明请参考 [TUSHARE_SETUP.md](./TUSHARE_SETUP.md)

### 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
# 或
yarn install

# 启动开发服务器
npm run dev
# 或
yarn dev
```

前端将在 `http://localhost:5173` 运行

### 模型集成

1. **准备模型文件**
   - 将预训练的 Kronos 模型文件放在 `backend/models/` 目录
   - 更新 `backend/app/services/model_inference.py` 中的模型加载逻辑

2. **配置模型路径**
   - 可以通过环境变量 `MODEL_PATH` 设置模型路径
   - 默认路径：`models/kronos_model.pth`

3. **实现模型推理**
   - 在 `ModelInference._load_model()` 中实现实际的模型加载
   - 在 `ModelInference._run_inference()` 中实现实际的推理逻辑

## CSV 文件格式要求

### 必需列
- **日期** (支持别名: date, Date, 时间, datetime)
- **开盘** (支持别名: open, Open, 开盘价)
- **最高** (支持别名: high, High, 最高价)
- **最低** (支持别名: low, Low, 最低价)
- **收盘** (支持别名: close, Close, 收盘价)
- **成交量** (支持别名: volume, Volume, vol, 成交量)

### 示例 CSV

```csv
日期,开盘,最高,最低,收盘,成交量
2024-01-01,100.0,105.0,99.0,103.0,1000000
2024-01-02,103.0,108.0,102.0,106.0,1200000
```

## API 端点

### 文件上传
- `POST /api/upload` - 上传 CSV 文件
- `GET /api/upload/validate` - 获取 CSV 格式要求

### Tushare 数据
- `POST /api/tushare/fetch` - 从 Tushare 获取期货数据
- `POST /api/tushare/search` - 搜索期货合约
- `GET /api/tushare/info` - 获取 Tushare 使用说明

### 预测
- `POST /api/predict` - 执行预测
- `GET /api/predict/status` - 获取模型状态

### 健康检查
- `GET /` - 根路径
- `GET /api/health` - 健康检查

## 开发计划

### 已完成 ✅
- [x] 项目结构搭建
- [x] 后端 API 开发
- [x] 前端 UI 开发
- [x] CSV 解析和验证
- [x] 模型推理框架
- [x] 数据可视化
- [x] 中文界面
- [x] 错误处理

### 待完成 🔲
- [ ] 集成实际的 Kronos 模型
- [ ] 添加单元测试
- [ ] 添加集成测试
- [ ] 性能优化
- [ ] 部署配置
- [ ] 用户认证（如需要）
- [ ] 历史预测记录（如需要）
- [x] Tushare 数据获取功能

## 注意事项

1. **模型集成**: 当前模型推理服务为占位符实现，需要根据实际的 Kronos 模型结构进行集成。

2. **数据安全**: 上传的文件存储在 `uploads/` 目录，生产环境应考虑：
   - 文件大小限制
   - 定期清理旧文件
   - 文件访问权限控制

3. **性能优化**: 
   - 对于大文件，考虑使用异步处理
   - 添加缓存机制
   - 优化模型推理速度

4. **错误处理**: 已实现基本的错误处理，可根据实际需求扩展。

## 许可证

[待定]

## 贡献

欢迎提交 Issue 和 Pull Request！


# 期货价格趋势预测 Web 应用

这是一个基于预训练 Kronos 模型的 MVP Web 应用，允许用户上传 OHLCV CSV 数据并预测未来每日期货价格趋势。

## 项目结构

```
Quant_webui/
├── backend/                 # 后端服务（FastAPI）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI 主应用
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   │   ├── csv_parser.py    # CSV 解析服务
│   │   │   ├── model_inference.py # 模型推理服务
│   │   │   └── data_validator.py # 数据验证服务
│   │   └── utils/          # 工具函数
│   ├── models/             # 预训练模型文件（kronos）
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # 前端应用（React + TypeScript）
│   ├── src/
│   │   ├── components/     # React 组件
│   │   │   ├── FileUpload.tsx
│   │   │   ├── PredictionResults.tsx
│   │   │   └── Chart.tsx
│   │   ├── services/       # API 服务
│   │   ├── utils/          # 工具函数
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── tsconfig.json
├── .gitignore
└── README.md
```

## 技术栈

### 后端
- **FastAPI**: 现代、快速的 Python Web 框架
- **Pandas**: CSV 数据处理
- **NumPy**: 数值计算
- **模型推理**: 根据 Kronos 模型需求选择（PyTorch/TensorFlow 等）

### 前端
- **React 18**: UI 框架
- **TypeScript**: 类型安全
- **Vite**: 构建工具
- **Tailwind CSS**: 样式框架
- **Recharts**: 数据可视化
- **Axios**: HTTP 客户端

## 功能特性

1. ✅ 用户友好的文件上传界面
2. ✅ CSV 数据验证和错误提示
3. ✅ 实时预测结果显示
4. ✅ 交互式图表可视化
5. ✅ 完整的中文界面
6. ✅ 响应式设计

## 开发计划

1. 项目初始化和配置
2. 后端 API 开发
3. 前端 UI 开发
4. 模型集成
5. 测试和优化


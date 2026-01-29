# Tushare Token 配置指南

## 快速配置

### 方法 1：使用 .env 文件（推荐）

1. 编辑 `backend/.env` 文件
2. 将 `TUSHARE_TOKEN=your_token_here` 中的 `your_token_here` 替换为您的实际 Token
3. 保存文件
4. 重启服务器（如果正在运行）

示例：
```env
TUSHARE_TOKEN=0452fa270e894673a8482870058e208f13e458e4542a2b1d3e736c45
```

### 方法 2：使用环境变量

在终端中运行：

```bash
# Linux/Mac
export TUSHARE_TOKEN="your_token_here"

# Windows
set TUSHARE_TOKEN=your_token_here
```

然后启动服务器。

### 方法 3：在启动命令中设置

```bash
# Linux/Mac
TUSHARE_TOKEN="your_token_here" python run_server.py

# Windows
set TUSHARE_TOKEN=your_token_here && python run_server.py
```

## 获取 Tushare Token

1. 访问 [Tushare 官网](https://tushare.pro/register?reg=1)
2. 注册账号并登录
3. 在个人中心找到您的 API Token
4. 复制 Token 并配置到上述任一方法中

## 验证配置

启动服务器后，如果看到以下消息表示配置成功：
```
✓ Tushare Token 已配置（长度: XX）
```

如果看到警告消息，说明 Token 未正确配置：
```
⚠️  警告: TUSHARE_TOKEN 未配置或使用默认值
```

## 注意事项

- `.env` 文件已添加到 `.gitignore`，不会提交到 Git
- 不要将 Token 分享给他人
- Token 是您账号的唯一标识，请妥善保管


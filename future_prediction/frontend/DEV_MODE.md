# 开发模式说明

## 功能说明

在开发模式下，系统会自动跳过登录验证，允许直接访问 dashboard，方便开发调试。

## 启用开发模式

### 方法 1：自动检测（推荐）

开发模式会在以下情况自动启用：
- 运行 `npm run dev` 时（Vite 的 `MODE` 环境变量为 `development`）

### 方法 2：手动启用

创建 `.env` 文件（在 `frontend/` 目录下）：

```env
VITE_DEV_MODE=true
```

或者设置环境变量：

```bash
export VITE_DEV_MODE=true
npm run dev
```

## 开发模式特性

### 1. 跳过登录验证
- 可以直接访问 `/dashboard`，无需登录
- 受保护的路由会自动放行

### 2. Mock 用户信息
- 自动使用 mock 用户信息：
  - 用户 ID: 1
  - 手机号: 13800138000
  - 昵称: 开发模式用户
  - 角色: 会员（user_role: 2）

### 3. API Mock 数据（可选）
- 如果后端 API 不可用，某些 API 会返回 mock 数据
- 目前支持：
  - 文件上传 API：返回 mock file_id
  - 预测 API：返回 mock 预测结果

## 使用示例

### 直接访问 Dashboard

```bash
# 启动开发服务器
cd frontend
npm run dev

# 在浏览器中直接访问
http://localhost:5173/dashboard
```

无需登录，直接进入 dashboard 页面。

### 禁用开发模式

如果需要测试真实的登录流程：

1. 删除 `.env` 文件中的 `VITE_DEV_MODE=true`
2. 或者使用生产模式构建：
   ```bash
   npm run build
   npm run preview
   ```

## 注意事项

1. **仅用于开发**：开发模式仅在开发环境中生效，生产构建会自动禁用
2. **API 调用**：开发模式下，如果后端不可用，某些 API 会返回 mock 数据
3. **数据持久化**：开发模式下的操作不会真正保存到后端（除非后端正常运行）

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_DEV_MODE` | 手动启用开发模式 | `false` |
| `MODE` | Vite 自动设置（development/production） | - |
| `VITE_API_BASE_URL` | API 基础 URL | `http://localhost:8000` |

## 代码位置

- 开发模式检测：`src/App.tsx`
- Mock 用户信息：`src/pages/Dashboard.tsx`
- API Mock：`src/services/api.ts`


# 用户认证 API 使用指南

## API 端点

### 1. 用户注册

**端点**: `POST /api/v1/auth/register`

**请求体**:
```json
{
  "phone_number": "13800138000",
  "password": "your_password",
  "email": "user@example.com",  // 可选
  "nickname": "用户昵称"  // 可选
}
```

**响应**:
```json
{
  "message": "注册成功",
  "user": {
    "user_id": 1,
    "phone_number": "13800138000",
    "email": "user@example.com",
    "nickname": "用户昵称",
    "user_role": 1
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### 2. 用户登录

**端点**: `POST /api/v1/auth/login`

**请求体**（使用手机号）:
```json
{
  "phone_number": "13800138000",
  "password": "your_password"
}
```

**请求体**（使用邮箱）:
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**响应**:
```json
{
  "message": "登录成功",
  "user": {
    "user_id": 1,
    "phone_number": "13800138000",
    "email": "user@example.com",
    "nickname": "用户昵称",
    "user_role": 1,
    "avatar_url": null
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### 3. 获取当前用户信息

**端点**: `GET /api/v1/auth/me`

**请求头**:
```
Authorization: Bearer {token}
```

**响应**:
```json
{
  "user_id": 1,
  "phone_number": "13800138000",
  "email": "user@example.com",
  "nickname": "用户昵称",
  "user_role": 1,
  "avatar_url": null,
  "prediction_count": 0,
  "daily_prediction_limit": 5,
  "member_expire_time": null,
  "created_at": "2024-01-01T00:00:00"
}
```

### 4. 获取预测次数限制

**端点**: `GET /api/v1/auth/prediction-limit`

**请求头**:
```
Authorization: Bearer {token}
```

**响应**:
```json
{
  "allowed": true,
  "remaining": 5,
  "limit": 5,
  "is_member": false,
  "current_count": 0
}
```

### 5. 用户登出

**端点**: `POST /api/v1/auth/logout`

**请求头**:
```
Authorization: Bearer {token}
```

**响应**:
```json
{
  "message": "登出成功"
}
```

## 权限说明

### 用户角色

- **1 - 普通用户**: 每日 5 次预测，不能上传 CSV
- **2 - 会员**: 无限次预测，可以上传 CSV
- **3 - 超级管理员**: 无限次预测，可以上传 CSV，可以管理数据源和用户

### 权限矩阵

| 功能 | 普通用户 | 会员 | 超级管理员 |
|------|---------|------|-----------|
| 基础行情查看 | ✓ | ✓ | ✓ |
| 板块榜单查看 | 部分(3个) | 全部 | 全部 |
| AI预测次数 | 5次/天 | 无限 | 无限 |
| CSV上传 | ✗ | ✓ | ✓ |
| 自定义头像 | ✗ | ✓ | ✓ |
| 数据源管理 | ✗ | ✗ | ✓ |
| 用户权限管理 | ✗ | ✗ | ✓ |

## 使用示例

### Python 示例

```python
import requests

# 注册
response = requests.post("http://localhost:8000/api/v1/auth/register", json={
    "phone_number": "13800138000",
    "password": "password123",
    "nickname": "测试用户"
})
token = response.json()["token"]

# 登录
response = requests.post("http://localhost:8000/api/v1/auth/login", json={
    "phone_number": "13800138000",
    "password": "password123"
})
token = response.json()["token"]

# 使用 Token 访问受保护接口
headers = {"Authorization": f"Bearer {token}"}
response = requests.get("http://localhost:8000/api/v1/auth/me", headers=headers)
user_info = response.json()
```

### JavaScript/TypeScript 示例

```typescript
// 登录
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    phone_number: '13800138000',
    password: 'password123',
  }),
});

const data = await response.json();
const token = data.token;

// 使用 Token
const userResponse = await fetch('http://localhost:8000/api/v1/auth/me', {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});

const userInfo = await userResponse.json();
```

## 错误处理

### 401 Unauthorized
- Token 无效或过期
- 用户不存在
- 用户账户被禁用

### 403 Forbidden
- 权限不足（如普通用户尝试上传 CSV）
- 预测次数已达上限

### 400 Bad Request
- 请求参数错误
- 手机号或邮箱格式错误
- 密码不符合要求

## 注意事项

1. **Token 存储**: 建议将 Token 存储在安全的地方（如 httpOnly cookie 或安全的本地存储）
2. **Token 过期**: Token 默认 24 小时过期，过期后需要重新登录
3. **密码安全**: 密码至少 6 位，建议使用强密码
4. **HTTPS**: 生产环境必须使用 HTTPS


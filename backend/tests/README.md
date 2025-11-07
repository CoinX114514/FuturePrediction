# 测试说明

## 运行测试

### 运行所有测试

```bash
cd backend
source venv/bin/activate
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_auth.py
pytest tests/test_permissions.py
pytest tests/test_auth_service.py
```

### 运行特定测试类

```bash
pytest tests/test_auth.py::TestUserRegistration
```

### 运行特定测试方法

```bash
pytest tests/test_auth.py::TestUserRegistration::test_register_with_phone
```

### 显示详细输出

```bash
pytest -v
pytest -vv  # 更详细
```

### 显示打印输出

```bash
pytest -s
```

## 测试覆盖范围

### 认证功能测试 (`test_auth.py`)

- ✅ 用户注册（手机号、邮箱）
- ✅ 用户登录（手机号、邮箱）
- ✅ Token 验证
- ✅ 获取当前用户信息
- ✅ 用户登出
- ✅ 预测次数限制查询

### 权限测试 (`test_permissions.py`)

- ✅ CSV 上传权限（普通用户/会员/管理员）
- ✅ 预测权限（普通用户/会员）
- ✅ 未登录用户访问控制

### 认证服务测试 (`test_auth_service.py`)

- ✅ 用户注册服务
- ✅ 用户认证服务
- ✅ 会话创建
- ✅ 预测限制检查
- ✅ 预测次数计数

## 测试数据库

测试使用 SQLite 内存数据库，每个测试函数都会创建新的数据库实例，测试结束后自动清理。

## 注意事项

1. 测试前确保已安装所有依赖：`pip install -r requirements.txt`
2. 测试数据库是独立的，不会影响开发数据库
3. 每个测试都是独立的，不会相互影响
4. 测试文件上传功能时，会在 `uploads/` 目录创建临时文件，测试结束后会自动清理


# 测试说明

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest tests/test_price_update_service.py
```

### 运行特定测试类
```bash
pytest tests/test_price_update_service.py::TestGetFuturesSpotPrice
```

### 运行特定测试方法
```bash
pytest tests/test_price_update_service.py::TestGetFuturesSpotPrice::test_get_price_success_with_symbol_column
```

### 显示详细输出
```bash
pytest -v
```

### 显示打印输出
```bash
pytest -s
```

## 测试覆盖的场景

### get_futures_spot_price 方法测试
- ✅ 成功获取价格（使用 'symbol' 列名）
- ✅ 成功获取价格（使用中文列名）
- ✅ 不区分大小写匹配
- ✅ akshare 返回空数据
- ✅ akshare 返回 None
- ✅ 合约代码不存在
- ✅ 找不到合约代码列
- ✅ 找不到价格列
- ✅ 价格值无法转换为浮点数
- ✅ 价格值为 NaN
- ✅ 网络错误处理
- ✅ 超时错误处理
- ✅ 多个匹配时返回第一个
- ✅ 部分匹配合约代码

### update_post_price 方法测试
- ✅ 成功更新帖子价格
- ✅ 帖子不存在
- ✅ 帖子已删除
- ✅ 帖子没有合约代码
- ✅ 获取价格失败
- ✅ 数据库更新失败

### update_all_posts_price 方法测试
- ✅ 成功批量更新所有帖子
- ✅ 没有帖子
- ✅ 异常处理

### update_posts_by_contract_code 方法测试
- ✅ 成功按合约代码更新
- ✅ 获取价格失败
- ✅ 没有匹配的帖子
- ✅ 部分帖子更新失败
- ✅ 数据库提交失败

## 注意事项

1. 这些测试使用 mock 对象，不会实际调用 akshare API
2. 测试不会连接真实数据库
3. 所有测试都是单元测试，测试隔离性良好
4. 如果需要集成测试（实际调用 akshare），需要单独编写


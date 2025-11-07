# Tushare API 使用示例

## 概述

已更新 Tushare 服务以支持完整的 API 参数，与官方 API 调用方式完全一致。

## API 调用方式

### 方式 1：通过合约代码查询（最常用）

```python
from app.services.tushare_service import TushareService

# 初始化服务（使用环境变量中的 token）
service = TushareService()

# 或者直接传入 token
# service = TushareService(token="your_token_here")

# 获取特定合约的数据
df = service.get_future_data(
    code="CU.SHF",  # 铜主力合约
    start_date="20240101",
    end_date="20241231"
)
```

### 方式 2：通过交易日期查询

```python
# 获取某一天所有合约的数据
df = service.get_future_data(
    trade_date="20241201"
)
```

### 方式 3：通过交易所查询

```python
# 获取某个交易所的所有合约数据
df = service.get_future_data(
    exchange="SHF",  # 上海期货交易所
    start_date="20240101",
    end_date="20241231"
)
```

### 方式 4：组合查询

```python
# 组合多个条件
df = service.get_future_data(
    code="CU.SHF",
    start_date="20240101",
    end_date="20241231",
    limit=100,  # 限制返回记录数
    offset=0    # 偏移量
)
```

## 支持的参数

| 参数 | 类型 | 说明 | 示例 |
|------|------|------|------|
| code | str | 期货合约代码（ts_code） | "CU.SHF" |
| trade_date | str | 交易日期（YYYYMMDD） | "20241201" |
| exchange | str | 交易所代码 | "SHF", "DCE", "CZCE", "CFX", "INE", "GFE" |
| start_date | str | 开始日期（YYYYMMDD） | "20240101" |
| end_date | str | 结束日期（YYYYMMDD） | "20241231" |
| limit | int | 返回记录数限制 | 100 |
| offset | int | 返回记录偏移量 | 0 |

## REST API 调用示例

### 通过合约代码获取数据

```bash
curl -X POST "http://localhost:8000/api/tushare/fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "CU.SHF",
    "start_date": "20240101",
    "end_date": "20241231"
  }'
```

### 通过交易日期获取数据

```bash
curl -X POST "http://localhost:8000/api/tushare/fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "trade_date": "20241201"
  }'
```

### 通过交易所获取数据

```bash
curl -X POST "http://localhost:8000/api/tushare/fetch" \
  -H "Content-Type: application/json" \
  -d '{
    "exchange": "SHF",
    "start_date": "20240101",
    "end_date": "20241231",
    "limit": 100
  }'
```

## 前端调用示例

### 使用 TypeScript/JavaScript

```typescript
import { fetchTushareData } from './services/api'

// 通过合约代码获取数据
const data = await fetchTushareData(
  'CU.SHF',
  '20240101',
  '20241231',
  100
)

// 或者使用完整的请求对象
const response = await fetch('http://localhost:8000/api/tushare/fetch', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    code: 'CU.SHF',
    start_date: '20240101',
    end_date: '20241231',
    limit: 100
  })
})
```

## 返回数据格式

所有返回的数据都会被标准化为以下格式：

```python
{
    "日期": "2024-01-01",  # datetime 类型
    "开盘": 100.0,
    "最高": 105.0,
    "最低": 99.0,
    "收盘": 103.0,
    "成交量": 1000000
}
```

## 注意事项

1. **参数要求**：必须至少指定以下参数之一：
   - `code`（合约代码）
   - `trade_date`（交易日期）
   - `start_date` 和 `end_date`（日期范围）

2. **多合约处理**：如果查询返回多个合约的数据，系统会自动选择第一个合约的数据进行后续处理。

3. **日期格式**：所有日期参数必须使用 `YYYYMMDD` 格式（如 `20241201`）。

4. **Token 配置**：确保已正确配置 Tushare Token：
   ```bash
   export TUSHARE_TOKEN="your_token_here"
   ```

5. **数据验证**：获取的数据会自动进行验证，确保包含所有必需的 OHLCV 字段。

## 与官方 API 的对应关系

我们的实现与官方 Tushare API 完全对应：

```python
# 官方 API 调用
df = pro.fut_daily(
    ts_code="CU.SHF",
    start_date="20240101",
    end_date="20241231",
    fields=["ts_code", "trade_date", "open", "high", "low", "close", "vol"]
)

# 我们的服务调用（等价）
df = service.get_future_data(
    code="CU.SHF",
    start_date="20240101",
    end_date="20241231"
)
```

## 常见问题

### Q: 如何获取最新的数据？

A: 不指定日期参数，或者只指定 `code`，系统会自动获取最近 100 天的数据。

### Q: 如何获取某个交易所的所有合约？

A: 使用 `exchange` 参数，例如 `exchange="SHF"`。

### Q: 如何分页获取大量数据？

A: 使用 `limit` 和 `offset` 参数进行分页。

### Q: 返回的数据格式是什么？

A: 返回的是 Pandas DataFrame，已转换为标准的中文列名，可以直接用于后续的预测处理。


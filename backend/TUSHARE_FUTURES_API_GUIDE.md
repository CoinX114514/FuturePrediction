# Tushare 期货合约 API 遍历指南

## 概述

`explore_tushare_futures.py` 脚本用于遍历 Tushare 提供的所有期货合约相关的 API，并获取正在交易中的期货合约信息列表。

## 脚本功能

脚本会依次调用以下 Tushare API：

### 1. `fut_basic` - 期货合约基本信息
- **功能**：获取所有期货合约的基本信息
- **返回字段**：
  - `ts_code`: Tushare 合约代码
  - `symbol`: 品种代码
  - `exchange`: 交易所代码
  - `name`: 合约名称
  - `fut_code`: 期货代码
  - `multiplier`: 合约乘数
  - `trade_unit`: 交易单位
  - `list_date`: 上市日期
  - `delist_date`: 退市日期
  - 等其他字段

### 2. `fut_daily` - 期货日线行情
- **功能**：获取期货日线行情数据
- **返回字段**：
  - `ts_code`: Tushare 合约代码
  - `trade_date`: 交易日期
  - `pre_close`: 昨收盘
  - `pre_settle`: 昨结算
  - `open`: 开盘价
  - `high`: 最高价
  - `low`: 最低价
  - `close`: 收盘价
  - `settle`: 结算价
  - `vol`: 成交量
  - `amount`: 成交额
  - `oi`: 持仓量

### 3. `fut_trade_cal` - 期货交易日历
- **功能**：获取期货交易日历
- **返回字段**：
  - `exchange`: 交易所代码
  - `cal_date`: 日历日期
  - `is_open`: 是否交易（1=交易，0=休市）
  - `pretrade_date`: 上一个交易日

### 4. `fut_mapping` - 期货合约映射关系
- **功能**：获取期货合约映射关系（新旧合约代码对应关系）
- **返回字段**：
  - `ts_code`: 当前合约代码
  - `ts_code_old`: 旧合约代码
  - `ts_code_new`: 新合约代码
  - `ts_code_listed`: 上市合约代码
  - `ts_code_delisted`: 退市合约代码
  - `ts_code_main`: 主力合约代码
  - `ts_code_prev`: 上一个合约代码
  - `ts_code_next`: 下一个合约代码
  - `trade_date`: 交易日期

### 5. `fut_settle` - 期货结算参数
- **功能**：获取期货结算参数
- **返回字段**：
  - `ts_code`: Tushare 合约代码
  - `trade_date`: 交易日期
  - `settle`: 结算价
  - `settle2`: 结算价2
  - `rate1` ~ `rate5`: 各种费率

## 使用方法

### 1. 安装依赖

```bash
cd backend
pip install tushare pandas
```

或者使用项目的 requirements.txt：

```bash
pip install -r requirements.txt
```

### 2. 设置 Tushare Token

**方法 1：使用环境变量（推荐）**

```bash
export TUSHARE_TOKEN="your_token_here"
```

**方法 2：在 .env 文件中设置**

在 `backend/.env` 文件中添加：

```env
TUSHARE_TOKEN=your_token_here
```

**方法 3：在启动命令中设置**

```bash
TUSHARE_TOKEN="your_token_here" python explore_tushare_futures.py
```

### 3. 运行脚本

```bash
cd backend
python explore_tushare_futures.py
```

或者如果使用虚拟环境：

```bash
cd backend
source venv/bin/activate  # 或 source .venv/bin/activate
python explore_tushare_futures.py
```

## 输出结果

脚本运行后会：

1. **显示每个 API 的调用结果**：
   - 成功获取的数据条数
   - 数据列名
   - 前5条数据预览

2. **过滤正在交易中的合约**：
   - 根据上市日期和退市日期过滤
   - 结合日线行情数据验证合约是否有交易
   - 按交易所分组统计

3. **保存结果到 CSV 文件**：
   - 文件名格式：`tushare_active_futures_YYYYMMDD_HHMMSS.csv`
   - 包含所有正在交易中的期货合约信息

## 输出示例

```
================================================================================
开始遍历 Tushare 期货合约 API
================================================================================

--------------------------------------------------------------------------------
1. 获取期货合约基本信息 (fut_basic)
--------------------------------------------------------------------------------
正在调用 fut_basic API 获取期货合约基本信息...
成功获取 1234 条期货合约基本信息
基本信息列名: ['ts_code', 'symbol', 'exchange', 'name', ...]

前5条数据预览:
   ts_code symbol exchange      name  ...
0  CU2501.SHF    CU     SHFE      铜2501  ...
...

--------------------------------------------------------------------------------
6. 过滤正在交易中的期货合约
--------------------------------------------------------------------------------
过滤后得到 456 个正在交易中的期货合约

按交易所分组统计:
  SHFE: 120 个合约
  DCE: 150 个合约
  CZCE: 130 个合约
  CFFEX: 56 个合约

前10个正在交易中的合约:
  1. 铜2501 (CU2501.SHF) - SHFE
  2. 铝2501 (AL2501.SHF) - SHFE
  ...

结果已保存到文件: tushare_active_futures_20260126_192338.csv
```

## 其他可用的 Tushare 期货 API

除了脚本中遍历的主要 API，Tushare 还提供以下期货相关的 API（可根据需要添加到脚本中）：

- `fut_wsr` - 期货仓单日报
- `fut_holding` - 期货持仓数据
- `fut_index` - 期货指数
- `fut_index_daily` - 期货指数日线行情
- `fut_weekly` - 期货周线行情
- `fut_monthly` - 期货月线行情

## 注意事项

1. **Token 权限**：不同级别的 Tushare 账号有不同的 API 访问权限，某些 API 可能需要高级权限
2. **调用频率限制**：Tushare 对 API 调用有频率限制，请遵守相关规则
3. **数据更新**：期货合约数据会定期更新，建议定期运行脚本获取最新数据
4. **日期格式**：所有日期参数使用 `YYYYMMDD` 格式（如 `20260126`）

## 获取 Tushare Token

1. 访问 [Tushare 官网](https://tushare.pro/register?reg=1)
2. 注册账号并登录
3. 在个人中心找到您的 API Token
4. 复制 Token 并配置到环境变量或 .env 文件中

## 故障排除

### 问题 1：Token 错误
**错误信息**：`您的token不对，请确认。`

**解决方法**：
- 检查 TUSHARE_TOKEN 环境变量是否正确设置
- 确认 Token 是否有效（未过期）
- 检查 Token 是否有访问相应 API 的权限

### 问题 2：模块未找到
**错误信息**：`ModuleNotFoundError: No module named 'tushare'`

**解决方法**：
```bash
pip install tushare pandas
```

### 问题 3：数据为空
**可能原因**：
- 指定的交易日期是休市日
- Token 权限不足，无法访问该 API
- 网络连接问题

**解决方法**：
- 检查交易日期是否为交易日（使用 `fut_trade_cal` 验证）
- 确认 Token 权限级别
- 检查网络连接

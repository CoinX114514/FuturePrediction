# Tushare 配置指南

## 概述

本项目现在支持从 [Tushare](https://tushare.pro/) 平台直接获取期货数据，无需手动上传 CSV 文件。

## 获取 Tushare Token

1. **注册账号**
   - 访问 [Tushare 官网](https://tushare.pro/register?reg=1)
   - 完成注册并登录

2. **获取 Token**
   - 登录后，在个人中心可以找到您的 API Token
   - Token 格式类似：`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

3. **配置 Token**

   **方法 1：环境变量（推荐）**
   
   ```bash
   # Linux/Mac
   export TUSHARE_TOKEN="your_token_here"
   
   # Windows
   set TUSHARE_TOKEN=your_token_here
   ```

   **方法 2：.env 文件**
   
   在 `backend/` 目录下创建 `.env` 文件：
   ```
   TUSHARE_TOKEN=your_token_here
   ```

   **方法 3：直接在代码中配置（不推荐用于生产环境）**
   
   修改 `backend/app/services/tushare_service.py`：
   ```python
   self.token = "your_token_here"  # 不推荐
   ```

## 期货合约代码格式

### 支持的交易所

| 交易所 | 后缀 | 示例 |
|--------|------|------|
| 上海期货交易所 | .SHF | CU.SHF |
| 大连商品交易所 | .DCE | A.DCE |
| 郑州商品交易所 | .CZCE | WH.CZCE |
| 中国金融期货交易所 | .CFX | IF.CFX |
| 上海国际能源交易所 | .INE | SC.INE |
| 广州期货交易所 | .GFE | SI.GFE |

### 合约类型

1. **主力合约**
   - 格式：`品种代码.交易所后缀`
   - 示例：`CU.SHF`（铜主力合约）

2. **连续合约**
   - 格式：`品种代码L.交易所后缀`
   - 示例：`CUL.SHF`（铜连续合约）

3. **普通合约**
   - 格式：`品种代码MMDD.交易所后缀`
   - 示例：`CU1811.SHF`（2018年11月合约）

### 常用合约代码示例

- `CU.SHF` - 铜主力合约（上海期货交易所）
- `IF.CFX` - 沪深300期货主力合约（中国金融期货交易所）
- `RB.SHF` - 螺纹钢主力合约（上海期货交易所）
- `A.DCE` - 豆一主力合约（大连商品交易所）
- `ZC.CZCE` - 动力煤主力合约（郑州商品交易所）

## 使用说明

### 在前端使用

1. 打开应用后，点击 **"从 Tushare 获取"** 选项卡
2. 输入期货合约代码（如 `CU.SHF`）
3. 点击 **"获取数据"** 按钮
4. 系统会自动从 Tushare 获取数据并进行验证
5. 获取成功后即可进行预测

### 搜索合约

如果不知道确切的合约代码：

1. 在搜索框中输入关键词（如 "铜"、"CU"、"螺纹钢"）
2. 点击 **"搜索"** 按钮
3. 从搜索结果中选择合适的合约
4. 点击结果项，代码会自动填入

### API 直接调用

```python
from app.services.tushare_service import TushareService

# 初始化服务
service = TushareService()

# 获取数据
df = service.get_future_data(
    code="CU.SHF",
    start_date="20240101",
    end_date="20241231",
    limit=100
)
```

## 数据限制

根据 Tushare 的积分规则：

- **积分 2000+**：可以正常调用期货数据接口
- **积分 5000+**：调用无限制，频率更高
- 免费用户：每日调用次数有限

具体限制请参考 [Tushare 官方文档](https://tushare.pro/document/2?doc_id=134)

## 故障排除

### 错误：Token 未配置

```
ValueError: Tushare Token 未配置
```

**解决方案**：按照上述步骤配置 TUSHARE_TOKEN 环境变量。

### 错误：未获取到数据

```
ValueError: 未获取到数据，请检查合约代码是否正确
```

**可能原因**：
1. 合约代码格式错误
2. 该合约在当前时间段没有数据
3. 积分不足或调用频率超限

**解决方案**：
1. 检查代码格式是否正确
2. 尝试使用搜索功能查找正确的合约代码
3. 检查 Tushare 账号积分和调用限制

### 错误：数据验证失败

如果获取的数据验证失败，系统会显示具体的错误信息。常见问题：
- 数据缺失
- 价格逻辑错误（如最高价 < 最低价）

根据错误提示修正数据或联系技术支持。

## 参考链接

- [Tushare 官网](https://tushare.pro/)
- [Tushare 期货数据文档](https://tushare.pro/document/2?doc_id=134)
- [Tushare API 文档](https://tushare.pro/document/2?doc_id=138)


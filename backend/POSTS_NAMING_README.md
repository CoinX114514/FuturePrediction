# 帖子命名规范与数据库清理

## 命名格式

帖子标题统一为三段式：**「交易所」「品类」「代码」**

示例：
- `大商所 铁矿石 I2603`
- `上期所 铜 CU2601`
- `郑商所 红枣 CJ2609`
- `中金所 沪深300 IF2603`

## 交易所简称

| 代码 | 简称 |
|------|------|
| SHFE | 上期所 |
| DCE | 大商所 |
| CZCE | 郑商所 |
| CFFEX | 中金所 |
| INE | 上能源 |
| GFEX | 广期所 |

## 规范化脚本

### 1. 预览（不写库）

```bash
cd backend
python normalize_posts_naming.py
```

会输出将要更新的标题数量、重复帖子数量等，不修改数据库。

### 2. 执行写库

```bash
python normalize_posts_naming.py --execute
```

- 将所有已发布帖子的 `title` 更新为三段式标题；
- 将 `contract_code` 统一为大写；
- 同一 `contract_code` 有多条帖子时，保留最早发布的一条，其余软删除（`status=0`）。

### 3. 不删重复、只改标题

```bash
python normalize_posts_naming.py --execute --no-dedup
```

## 同步脚本中的命名

`sync_tushare_futures_to_db.py` 已改为：

- 新建帖子时使用 `format_post_title(contract_code, exchange)` 作为标题；
- 更新已有帖子时同步更新标题为三段式；
- `contract_code` 统一为大写。

后续从 Tushare 同步的帖子会直接符合命名规范。

## 扩展品类名称

若出现未覆盖的品种（标题中显示为品种代码而非中文），在 `app/utils/futures_naming.py` 的 `SYMBOL_CATEGORY_NAMES` 中增加对应条目即可。

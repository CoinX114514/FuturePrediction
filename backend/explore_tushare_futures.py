"""遍历 Tushare 期货合约 API 的脚本。

此脚本用于探索 Tushare 提供的所有期货合约相关的 API，
并获取正在交易中的期货合约信息列表。

设计原因：
1. Tushare 提供了多个期货相关的 API，需要逐一测试以了解哪些可用
2. 不同 API 返回的数据格式和内容不同，需要统一处理
3. 需要过滤出正在交易中的合约（排除已过期和未上市的合约）
"""

import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional, Any
import pandas as pd
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 尝试导入 tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    logger.error("未安装 tushare 库，请运行: pip install tushare")
    TUSHARE_AVAILABLE = False
    sys.exit(1)

# 获取 Tushare Token
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
if not TUSHARE_TOKEN:
    logger.warning("未设置 TUSHARE_TOKEN 环境变量，将使用默认值（可能无法访问）")
    TUSHARE_TOKEN = "your_token_here"

# 初始化 Tushare Pro API
try:
    ts.set_token(TUSHARE_TOKEN)
    pro = ts.pro_api()
    logger.info(f"Tushare Pro API 初始化成功（Token 长度: {len(TUSHARE_TOKEN)}）")
except Exception as e:
    logger.error(f"初始化 Tushare Pro API 失败: {e}")
    sys.exit(1)


def get_futures_basic_info() -> Optional[pd.DataFrame]:
    """获取期货合约基本信息。
    
    使用 Tushare 的 fut_basic API 获取所有期货合约的基本信息。
    
    Returns:
        Optional[pd.DataFrame]: 期货合约基本信息 DataFrame，如果失败返回 None。
    """
    try:
        logger.info("正在调用 fut_basic API 获取期货合约基本信息...")
        df = pro.fut_basic(
            exchange='',  # 空字符串表示获取所有交易所
            fut_type='',  # 空字符串表示获取所有类型
            fields='ts_code,symbol,exchange,name,fut_code,multiplier,trade_unit,per_unit,open_limit,unit,quote_unit,quote_unit_desc,d_mode,d_month,list_date,delist_date,last_ddate,last_edate,last_odate,last_ddate_desc,last_edate_desc,last_odate_desc'
        )
        logger.info(f"成功获取 {len(df)} 条期货合约基本信息")
        return df
    except Exception as e:
        logger.error(f"获取期货合约基本信息失败: {e}")
        return None


def get_futures_daily_data(trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """获取期货日线行情数据。
    
    使用 Tushare 的 fut_daily API 获取期货日线行情。
    如果指定 trade_date，则获取该日期的所有合约数据；
    如果不指定，则获取最近一个交易日的数据。
    
    Args:
        trade_date: 交易日期，格式 YYYYMMDD。如果为 None，则获取最近交易日。
    
    Returns:
        Optional[pd.DataFrame]: 期货日线行情 DataFrame，如果失败返回 None。
    """
    try:
        if trade_date is None:
            # 获取最近一个交易日
            trade_date = datetime.now().strftime('%Y%m%d')
        
        logger.info(f"正在调用 fut_daily API 获取 {trade_date} 的期货日线行情...")
        df = pro.fut_daily(
            trade_date=trade_date,
            fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol,amount,oi'
        )
        logger.info(f"成功获取 {len(df)} 条期货日线行情数据")
        return df
    except Exception as e:
        logger.error(f"获取期货日线行情失败: {e}")
        return None


def get_futures_trade_cal(start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """获取期货交易日历。
    
    使用 Tushare 的 trade_cal API 获取期货交易日历。
    注意：Tushare 的交易日历 API 名称是 trade_cal，不是 fut_trade_cal。
    
    Args:
        start_date: 开始日期，格式 YYYYMMDD。
        end_date: 结束日期，格式 YYYYMMDD。
    
    Returns:
        Optional[pd.DataFrame]: 期货交易日历 DataFrame，如果失败返回 None。
    """
    try:
        logger.info(f"正在调用 trade_cal API 获取 {start_date} 到 {end_date} 的交易日历...")
        # 尝试获取所有主要期货交易所的交易日历
        exchanges = ['SHFE', 'DCE', 'CZCE', 'CFFEX', 'INE', 'GFEX']
        all_cal_data = []
        
        for exchange in exchanges:
            try:
                df = pro.trade_cal(
                    exchange=exchange,
                    start_date=start_date,
                    end_date=end_date,
                    fields='exchange,cal_date,is_open,pretrade_date'
                )
                if df is not None and not df.empty:
                    all_cal_data.append(df)
                    logger.info(f"  成功获取 {exchange} 交易所 {len(df)} 条交易日历数据")
            except Exception as e:
                logger.warning(f"  获取 {exchange} 交易所交易日历失败: {e}")
                continue
        
        if all_cal_data:
            combined_df = pd.concat(all_cal_data, ignore_index=True)
            logger.info(f"成功获取总计 {len(combined_df)} 条交易日历数据")
            return combined_df
        else:
            logger.warning("未能获取任何交易所的交易日历数据")
            return None
    except Exception as e:
        logger.error(f"获取期货交易日历失败: {e}")
        return None


def get_futures_mapping() -> Optional[pd.DataFrame]:
    """获取期货合约映射关系。
    
    使用 Tushare 的 fut_mapping API 获取期货合约映射关系。
    
    Returns:
        Optional[pd.DataFrame]: 期货合约映射关系 DataFrame，如果失败返回 None。
    """
    try:
        logger.info("正在调用 fut_mapping API 获取期货合约映射关系...")
        df = pro.fut_mapping(
            fields='ts_code,ts_code_old,ts_code_new,ts_code_listed,ts_code_delisted,ts_code_main,ts_code_prev,ts_code_next,trade_date'
        )
        logger.info(f"成功获取 {len(df)} 条期货合约映射关系")
        return df
    except Exception as e:
        logger.error(f"获取期货合约映射关系失败: {e}")
        return None


def get_futures_settle(trade_date: Optional[str] = None) -> Optional[pd.DataFrame]:
    """获取期货结算参数。
    
    使用 Tushare 的 fut_settle API 获取期货结算参数。
    
    Args:
        trade_date: 交易日期，格式 YYYYMMDD。如果为 None，则获取最近交易日。
    
    Returns:
        Optional[pd.DataFrame]: 期货结算参数 DataFrame，如果失败返回 None。
    """
    try:
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
        
        logger.info(f"正在调用 fut_settle API 获取 {trade_date} 的期货结算参数...")
        df = pro.fut_settle(
            trade_date=trade_date,
            fields='ts_code,trade_date,settle,settle2,rate1,rate2,rate3,rate4,rate5'
        )
        logger.info(f"成功获取 {len(df)} 条期货结算参数")
        return df
    except Exception as e:
        logger.error(f"获取期货结算参数失败: {e}")
        return None


def filter_active_contracts(basic_df: pd.DataFrame, daily_df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """过滤出正在交易中的期货合约。
    
    根据合约的上市日期和退市日期，以及是否有交易数据来判断合约是否正在交易中。
    
    Args:
        basic_df: 期货合约基本信息 DataFrame。
        daily_df: 期货日线行情 DataFrame（可选），用于验证合约是否有交易数据。
    
    Returns:
        pd.DataFrame: 正在交易中的期货合约 DataFrame。
    """
    if basic_df is None or basic_df.empty:
        logger.warning("期货合约基本信息为空，无法过滤")
        return pd.DataFrame()
    
    today = date.today()
    today_str = today.strftime('%Y%m%d')
    
    # 复制 DataFrame 避免修改原数据
    df = basic_df.copy()
    
    # 转换日期列为日期类型
    if 'list_date' in df.columns:
        df['list_date'] = pd.to_datetime(df['list_date'], format='%Y%m%d', errors='coerce')
    if 'delist_date' in df.columns:
        df['delist_date'] = pd.to_datetime(df['delist_date'], format='%Y%m%d', errors='coerce')
    
    # 过滤条件：
    # 1. 已上市（list_date <= today）
    # 2. 未退市（delist_date 为空 或 delist_date >= today）
    active_mask = True
    
    if 'list_date' in df.columns:
        active_mask = active_mask & (df['list_date'].notna()) & (df['list_date'] <= pd.Timestamp(today))
    
    if 'delist_date' in df.columns:
        active_mask = active_mask & (
            df['delist_date'].isna() | (df['delist_date'] >= pd.Timestamp(today))
        )
    
    active_contracts = df[active_mask].copy()
    
    # 如果有日线行情数据，进一步过滤出有交易数据的合约
    if daily_df is not None and not daily_df.empty:
        if 'ts_code' in daily_df.columns:
            active_ts_codes = set(daily_df['ts_code'].unique())
            active_contracts = active_contracts[
                active_contracts['ts_code'].isin(active_ts_codes)
            ]
    
    logger.info(f"过滤后得到 {len(active_contracts)} 个正在交易中的期货合约")
    return active_contracts


def format_contract_info(contracts_df: pd.DataFrame) -> List[Dict[str, Any]]:
    """格式化期货合约信息为字典列表。
    
    Args:
        contracts_df: 期货合约 DataFrame。
    
    Returns:
        List[Dict]: 格式化后的期货合约信息列表。
    """
    if contracts_df is None or contracts_df.empty:
        return []
    
    contracts_list = []
    for _, row in contracts_df.iterrows():
        contract_info = {
            'ts_code': row.get('ts_code', ''),
            'symbol': row.get('symbol', ''),
            'exchange': row.get('exchange', ''),
            'name': row.get('name', ''),
            'fut_code': row.get('fut_code', ''),
            'multiplier': row.get('multiplier', None),
            'trade_unit': row.get('trade_unit', ''),
            'list_date': row.get('list_date', None),
            'delist_date': row.get('delist_date', None),
        }
        
        # 转换日期为字符串格式
        if contract_info['list_date'] is not None:
            if isinstance(contract_info['list_date'], pd.Timestamp):
                contract_info['list_date'] = contract_info['list_date'].strftime('%Y%m%d')
            else:
                contract_info['list_date'] = str(contract_info['list_date'])
        
        if contract_info['delist_date'] is not None:
            if isinstance(contract_info['delist_date'], pd.Timestamp):
                contract_info['delist_date'] = contract_info['delist_date'].strftime('%Y%m%d')
            else:
                contract_info['delist_date'] = str(contract_info['delist_date'])
        
        contracts_list.append(contract_info)
    
    return contracts_list


def generate_markdown_file(
    basic_df: pd.DataFrame,
    daily_df: Optional[pd.DataFrame] = None,
    active_contracts: Optional[pd.DataFrame] = None
) -> str:
    """生成包含所有期货信息的 Markdown 文件。
    
    Args:
        basic_df: 期货合约基本信息 DataFrame。
        daily_df: 期货日线行情 DataFrame（可选）。
        active_contracts: 正在交易中的期货合约 DataFrame（可选）。
    
    Returns:
        str: 生成的 Markdown 文件路径。
    """
    if basic_df is None or basic_df.empty:
        logger.warning("期货合约基本信息为空，无法生成 Markdown 文件")
        return ""
    
    # 交易所中文名称映射
    exchange_names = {
        'SHFE': '上海期货交易所',
        'DCE': '大连商品交易所',
        'CZCE': '郑州商品交易所',
        'CFFEX': '中国金融期货交易所',
        'INE': '上海国际能源交易中心',
        'GFEX': '广州期货交易所',
    }
    
    # 合并日线行情数据（如果有）
    merged_df = basic_df.copy()
    if daily_df is not None and not daily_df.empty:
        # 合并日线行情数据
        daily_latest = daily_df.groupby('ts_code').first().reset_index()
        merged_df = merged_df.merge(
            daily_latest[['ts_code', 'close', 'settle', 'vol', 'amount', 'oi']],
            on='ts_code',
            how='left',
            suffixes=('', '_daily')
        )
    
    # 如果提供了活跃合约列表，优先使用它
    if active_contracts is not None and not active_contracts.empty:
        display_df = active_contracts.copy()
        if daily_df is not None and not daily_df.empty:
            daily_latest = daily_df.groupby('ts_code').first().reset_index()
            display_df = display_df.merge(
                daily_latest[['ts_code', 'close', 'settle', 'vol', 'amount', 'oi']],
                on='ts_code',
                how='left',
                suffixes=('', '_daily')
            )
    else:
        display_df = merged_df
    
    # 生成 Markdown 内容
    md_content = []
    md_content.append("# Tushare 期货合约信息完整列表\n")
    md_content.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md_content.append(f"**数据来源**: Tushare Pro API\n")
    md_content.append(f"**总合约数**: {len(display_df)}\n")
    
    if active_contracts is not None and not active_contracts.empty:
        md_content.append(f"**正在交易中的合约数**: {len(active_contracts)}\n")
    
    md_content.append("\n---\n")
    
    # 按交易所分组
    if 'exchange' in display_df.columns:
        exchanges = sorted(display_df['exchange'].unique())
        
        for exchange in exchanges:
            exchange_df = display_df[display_df['exchange'] == exchange].copy()
            exchange_name = exchange_names.get(exchange, exchange)
            
            md_content.append(f"\n## {exchange_name} ({exchange})\n")
            md_content.append(f"**合约数量**: {len(exchange_df)}\n")
            
            # 生成表格
            md_content.append("\n| 合约代码 | 品种代码 | 合约名称 | 上市日期 | 退市日期 | 收盘价 | 结算价 | 成交量 | 持仓量 |")
            md_content.append("|---------|---------|---------|---------|---------|--------|--------|--------|--------|")
            
            # 按合约代码排序
            exchange_df = exchange_df.sort_values('ts_code')
            
            for _, row in exchange_df.iterrows():
                ts_code = str(row.get('ts_code', ''))
                symbol = str(row.get('symbol', ''))
                name = str(row.get('name', ''))
                
                # 处理日期
                list_date = row.get('list_date', '')
                if pd.notna(list_date):
                    if isinstance(list_date, pd.Timestamp):
                        list_date = list_date.strftime('%Y-%m-%d')
                    else:
                        list_date = str(list_date)
                else:
                    list_date = '-'
                
                delist_date = row.get('delist_date', '')
                if pd.notna(delist_date):
                    if isinstance(delist_date, pd.Timestamp):
                        delist_date = delist_date.strftime('%Y-%m-%d')
                    else:
                        delist_date = str(delist_date)
                else:
                    delist_date = '-'
                
                # 处理价格和交易数据
                close = row.get('close', '')
                if pd.notna(close):
                    close = f"{float(close):.2f}"
                else:
                    close = '-'
                
                settle = row.get('settle', '')
                if pd.notna(settle):
                    settle = f"{float(settle):.2f}"
                else:
                    settle = '-'
                
                vol = row.get('vol', '')
                if pd.notna(vol):
                    vol = f"{int(vol):,}"
                else:
                    vol = '-'
                
                oi = row.get('oi', '')
                if pd.notna(oi):
                    oi = f"{int(oi):,}"
                else:
                    oi = '-'
                
                md_content.append(
                    f"| {ts_code} | {symbol} | {name} | {list_date} | {delist_date} | "
                    f"{close} | {settle} | {vol} | {oi} |"
                )
    
    # 添加统计信息
    md_content.append("\n---\n")
    md_content.append("\n## 统计信息\n")
    
    if 'exchange' in display_df.columns:
        md_content.append("\n### 按交易所统计\n")
        md_content.append("| 交易所 | 代码 | 合约数量 |")
        md_content.append("|--------|------|---------|")
        exchange_counts = display_df['exchange'].value_counts().sort_index()
        for exchange, count in exchange_counts.items():
            exchange_name = exchange_names.get(exchange, exchange)
            md_content.append(f"| {exchange_name} | {exchange} | {count} |")
    
    # 添加数据字段说明
    md_content.append("\n---\n")
    md_content.append("\n## 数据字段说明\n")
    md_content.append("""
| 字段名 | 说明 |
|--------|------|
| 合约代码 (ts_code) | Tushare 标准合约代码，格式：品种代码+年月.交易所 |
| 品种代码 (symbol) | 期货品种代码 |
| 合约名称 (name) | 合约中文名称 |
| 上市日期 (list_date) | 合约上市日期 |
| 退市日期 (delist_date) | 合约退市日期 |
| 收盘价 (close) | 最新收盘价（如有日线行情数据） |
| 结算价 (settle) | 最新结算价（如有日线行情数据） |
| 成交量 (vol) | 最新成交量（如有日线行情数据） |
| 持仓量 (oi) | 最新持仓量（如有日线行情数据） |

### 交易所代码说明
- **SHFE**: 上海期货交易所
- **DCE**: 大连商品交易所
- **CZCE**: 郑州商品交易所
- **CFFEX**: 中国金融期货交易所
- **INE**: 上海国际能源交易中心
- **GFEX**: 广州期货交易所
""")
    
    # 保存文件
    output_file = f"tushare_futures_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    
    logger.info(f"Markdown 文件已生成: {output_file}")
    return output_file


def main():
    """主函数：遍历所有 Tushare 期货 API 并获取正在交易中的合约信息。"""
    logger.info("=" * 80)
    logger.info("开始遍历 Tushare 期货合约 API")
    logger.info("=" * 80)
    
    results = {}
    
    # 1. 获取期货合约基本信息
    logger.info("\n" + "-" * 80)
    logger.info("1. 获取期货合约基本信息 (fut_basic)")
    logger.info("-" * 80)
    basic_df = get_futures_basic_info()
    if basic_df is not None and not basic_df.empty:
        results['basic_info'] = basic_df
        logger.info(f"基本信息列名: {list(basic_df.columns)}")
        logger.info(f"\n前5条数据预览:\n{basic_df.head()}")
    
    # 2. 获取期货日线行情（最近交易日）
    logger.info("\n" + "-" * 80)
    logger.info("2. 获取期货日线行情 (fut_daily)")
    logger.info("-" * 80)
    daily_df = get_futures_daily_data()
    if daily_df is not None and not daily_df.empty:
        results['daily_data'] = daily_df
        logger.info(f"日线行情列名: {list(daily_df.columns)}")
        logger.info(f"\n前5条数据预览:\n{daily_df.head()}")
    
    # 3. 获取期货交易日历
    logger.info("\n" + "-" * 80)
    logger.info("3. 获取期货交易日历 (trade_cal)")
    logger.info("-" * 80)
    today = datetime.now()
    start_date = (today - pd.Timedelta(days=30)).strftime('%Y%m%d')
    end_date = today.strftime('%Y%m%d')
    trade_cal_df = get_futures_trade_cal(start_date, end_date)
    if trade_cal_df is not None and not trade_cal_df.empty:
        results['trade_cal'] = trade_cal_df
        logger.info(f"交易日历列名: {list(trade_cal_df.columns)}")
        logger.info(f"\n前5条数据预览:\n{trade_cal_df.head()}")
    
    # 4. 获取期货合约映射关系
    logger.info("\n" + "-" * 80)
    logger.info("4. 获取期货合约映射关系 (fut_mapping)")
    logger.info("-" * 80)
    mapping_df = get_futures_mapping()
    if mapping_df is not None and not mapping_df.empty:
        results['mapping'] = mapping_df
        logger.info(f"映射关系列名: {list(mapping_df.columns)}")
        logger.info(f"\n前5条数据预览:\n{mapping_df.head()}")
    
    # 5. 获取期货结算参数
    logger.info("\n" + "-" * 80)
    logger.info("5. 获取期货结算参数 (fut_settle)")
    logger.info("-" * 80)
    settle_df = get_futures_settle()
    if settle_df is not None and not settle_df.empty:
        results['settle'] = settle_df
        logger.info(f"结算参数列名: {list(settle_df.columns)}")
        logger.info(f"\n前5条数据预览:\n{settle_df.head()}")
    
    # 6. 过滤出正在交易中的合约
    logger.info("\n" + "-" * 80)
    logger.info("6. 过滤正在交易中的期货合约")
    logger.info("-" * 80)
    if 'basic_info' in results:
        active_contracts = filter_active_contracts(
            results['basic_info'],
            results.get('daily_data')
        )
        
        if not active_contracts.empty:
            results['active_contracts'] = active_contracts
            
            # 格式化并显示结果
            contracts_list = format_contract_info(active_contracts)
            
            logger.info(f"\n共找到 {len(contracts_list)} 个正在交易中的期货合约")
            logger.info("\n按交易所分组统计:")
            if 'exchange' in active_contracts.columns:
                exchange_counts = active_contracts['exchange'].value_counts()
                for exchange, count in exchange_counts.items():
                    logger.info(f"  {exchange}: {count} 个合约")
            
            logger.info("\n前10个正在交易中的合约:")
            for i, contract in enumerate(contracts_list[:10], 1):
                logger.info(f"  {i}. {contract['name']} ({contract['ts_code']}) - {contract['exchange']}")
            
            # 保存结果到 CSV 文件
            output_file = f"tushare_active_futures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            active_contracts.to_csv(output_file, index=False, encoding='utf-8-sig')
            logger.info(f"\n结果已保存到文件: {output_file}")
            
            # 生成 Markdown 文件
            logger.info("\n正在生成 Markdown 文件...")
            md_file = generate_markdown_file(
                results['basic_info'],
                results.get('daily_data'),
                active_contracts
            )
            if md_file:
                logger.info(f"Markdown 文件已生成: {md_file}")
    
    # 总结
    logger.info("\n" + "=" * 80)
    logger.info("遍历完成！")
    logger.info("=" * 80)
    logger.info(f"成功调用的 API 数量: {len(results)}")
    for api_name, df in results.items():
        if df is not None and not df.empty:
            logger.info(f"  - {api_name}: {len(df)} 条数据")
    
    return results


if __name__ == "__main__":
    main()

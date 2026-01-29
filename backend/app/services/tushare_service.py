"""Tushare 数据服务。

负责封装所有 Tushare API 调用，提供统一的接口获取期货数据。

设计原因：
1. 统一管理 Tushare API 调用，便于维护和更新
2. 提供错误处理和重试机制
3. 统一数据格式转换，便于其他服务使用
4. 支持缓存机制，减少 API 调用次数
"""

import os
import re
import logging
from typing import Optional, Dict, List
from datetime import datetime, date
import pandas as pd
import numpy as np

# 配置日志
logger = logging.getLogger(__name__)

# 尝试导入 tushare
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    logger.error("未安装 tushare 库，请运行: pip install tushare")
    TUSHARE_AVAILABLE = False
    ts = None

# 初始化 Tushare Pro API
TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
if TUSHARE_TOKEN and TUSHARE_AVAILABLE:
    try:
        ts.set_token(TUSHARE_TOKEN)
        pro = ts.pro_api()
        logger.info(f"Tushare Pro API 初始化成功（Token 长度: {len(TUSHARE_TOKEN)}）")
    except Exception as e:
        logger.error(f"初始化 Tushare Pro API 失败: {e}")
        pro = None
else:
    if not TUSHARE_TOKEN:
        logger.warning("未设置 TUSHARE_TOKEN 环境变量")
    pro = None


class TushareService:
    """Tushare 数据服务类。

    提供统一的接口获取期货数据，封装所有 Tushare API 调用。
    """

    def __init__(self):
        """初始化 Tushare 服务。"""
        if not TUSHARE_AVAILABLE:
            raise ImportError("tushare 库未安装，请运行: pip install tushare")
        if pro is None:
            raise ValueError("Tushare Pro API 未初始化，请检查 TUSHARE_TOKEN 环境变量")

    def get_futures_basic_info(self, exchange: str = '') -> Optional[pd.DataFrame]:
        """获取期货合约基本信息。
        
        Args:
            exchange: 交易所代码，空字符串表示获取所有交易所。
        
        Returns:
            Optional[pd.DataFrame]: 期货合约基本信息 DataFrame。
        """
        try:
            df = pro.fut_basic(
                exchange=exchange,
                fut_type='',
                fields='ts_code,symbol,exchange,name,fut_code,multiplier,trade_unit,per_unit,quote_unit,quote_unit_desc,list_date,delist_date,last_ddate'
            )
            return df
        except Exception as e:
            logger.error(f"获取期货合约基本信息失败: {e}")
            return None

    def get_futures_daily(self, trade_date: Optional[str] = None, ts_code: Optional[str] = None) -> Optional[pd.DataFrame]:
        """获取期货日线行情数据。
        
        Args:
            trade_date: 交易日期，格式 YYYYMMDD。如果为 None，则获取最近交易日。
            ts_code: 合约代码（可选），如果指定则只获取该合约的数据。
        
        Returns:
            Optional[pd.DataFrame]: 期货日线行情 DataFrame。
        """
        try:
            if trade_date is None:
                trade_date = datetime.now().strftime('%Y%m%d')
            
            params = {
                'trade_date': trade_date,
                'fields': 'ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol,amount,oi'
            }
            
            if ts_code:
                params['ts_code'] = ts_code
            
            df = pro.fut_daily(**params)
            return df
        except Exception as e:
            logger.error(f"获取期货日线行情失败: {e}")
            return None

    def get_futures_price(self, contract_code: str) -> Optional[float]:
        """获取指定合约的现价（与 K 线图“最后一根收盘”同源，保证列表与详情一致）。

        优先用当日行情；若无则用近期日线区间取最近一根收盘价，与 K 线 API 逻辑一致。

        Args:
            contract_code: 合约代码，如 "CU2601.SHF" 或 "CU2601"。

        Returns:
            Optional[float]: 现价（最近收盘），失败返回 None。
        """
        try:
            ts_code = self.convert_contract_code_to_ts_code(contract_code)
            today = datetime.now().strftime('%Y%m%d')

            # 1) 先查当日该合约
            df = self.get_futures_daily(trade_date=today, ts_code=ts_code)
            if df is not None and not df.empty and 'close' in df.columns:
                close_price = df.iloc[0]['close']
                if pd.notna(close_price) and close_price != 0:
                    return float(close_price)
            if df is not None and not df.empty and 'settle' in df.columns:
                settle_price = df.iloc[0]['settle']
                if pd.notna(settle_price) and settle_price != 0:
                    return float(settle_price)

            # 2) 当日无数据时，用全量当日按 ts_code 精确匹配
            df = self.get_futures_daily(trade_date=today)
            if df is not None and not df.empty:
                exact = df[df['ts_code'].astype(str) == ts_code]
                if not exact.empty:
                    row = exact.iloc[0]
                    if 'close' in row.index:
                        close_price = row['close']
                        if pd.notna(close_price) and close_price != 0:
                            return float(close_price)
                    if 'settle' in row.index:
                        settle_price = row['settle']
                        if pd.notna(settle_price) and settle_price != 0:
                            return float(settle_price)

            # 3) 与 K 线同源：按日期区间取最近一根收盘（保证列表现价 = 详情 K 线最后一根）
            df = self.get_futures_kline(
                ts_code=ts_code,
                start_date=(datetime.now() - pd.Timedelta(days=60)).strftime('%Y%m%d'),
                end_date=today,
                period=60
            )
            if df is not None and isinstance(df, pd.DataFrame) and not df.empty and 'trade_date' in df.columns and 'close' in df.columns:
                df = df.sort_values('trade_date', ascending=True)
                last_row = df.iloc[-1]
                close_price = last_row.get('close')
                if pd.notna(close_price) and close_price != 0:
                    return float(close_price)
                settle_price = last_row.get('settle')
                if pd.notna(settle_price) and settle_price != 0:
                    return float(settle_price)

            logger.warning(f"无法获取合约价格，contract_code: {contract_code}，ts_code: {ts_code}")
            return None
            
        except Exception as e:
            logger.error(f"获取期货价格失败，contract_code: {contract_code}, 错误: {e}")
            return None

    def batch_get_futures_prices(self, contract_codes: List[str]) -> Dict[str, Optional[float]]:
        """批量获取多个合约的价格。
        
        先尝试一次性拉取当日全量日线，再对未命中的合约按 ts_code 单独查询
        （避免因 Tushare 返回条数限制导致铁矿石等合约漏掉）。
        
        Args:
            contract_codes: 合约代码列表。
        
        Returns:
            Dict[str, Optional[float]]: 合约代码到价格的映射。
        """
        price_map = {}
        
        try:
            # 1. 一次性获取当日全量日线（可能被接口条数截断）
            df = self.get_futures_daily()
            
            if df is not None and not df.empty:
                for contract_code in contract_codes:
                    if contract_code in price_map:
                        continue
                    code_clean = (contract_code or '').strip().upper()
                    if not code_clean:
                        continue
                    
                    # 只按「代码.交易所」精确匹配，避免 I2603 匹配到 NI2603 等
                    ts_code_exact = self.convert_contract_code_to_ts_code(code_clean)
                    exact = df[df['ts_code'].astype(str) == ts_code_exact]
                    
                    if not exact.empty:
                        row = exact.iloc[0]
                        if 'close' in row.index:
                            close_price = row['close']
                            if pd.notna(close_price) and close_price != 0:
                                price_map[contract_code] = float(close_price)
                                continue
                        if 'settle' in row.index:
                            settle_price = row['settle']
                            if pd.notna(settle_price) and settle_price != 0:
                                price_map[contract_code] = float(settle_price)
            
            # 2. 对未命中的合约按 ts_code 单独查询（解决全量被截断或非交易日无全量数据）
            missing = [c for c in contract_codes if c not in price_map or price_map[c] is None]
            if missing:
                logger.info(f"批量结果中未命中 {len(missing)} 个合约，改为按合约单独查询")
                for contract_code in missing:
                    if contract_code in price_map and price_map[contract_code] is not None:
                        continue
                    p = self.get_futures_price(contract_code)
                    if p is not None:
                        price_map[contract_code] = p
            
            logger.info(f"批量获取完成，成功获取 {len(price_map)}/{len(contract_codes)} 个合约的价格")
            return price_map
            
        except Exception as e:
            logger.error(f"批量获取期货价格失败: {e}")
            return price_map

    def get_futures_kline(
        self,
        ts_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: int = 365
    ) -> Optional[pd.DataFrame]:
        """获取期货合约的历史 K 线数据。
        
        Args:
            ts_code: Tushare 合约代码，如 "CU2601.SHF"。
            start_date: 开始日期，格式 YYYYMMDD。
            end_date: 结束日期，格式 YYYYMMDD。
            period: 获取最近多少天的数据（当 start_date 为 None 时使用）。
        
        Returns:
            Optional[pd.DataFrame]: K 线数据 DataFrame。
        """
        try:
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
            
            if start_date is None:
                start_date_obj = datetime.now() - pd.Timedelta(days=period)
                start_date = start_date_obj.strftime('%Y%m%d')
            
            # 使用 fut_daily 按合约 + 日期区间拉取历史日线（供帖子内 K 线图使用）
            df = pro.fut_daily(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                fields='trade_date,open,high,low,close,settle,vol,amount,oi'
            )
            if df is None or not isinstance(df, pd.DataFrame):
                return None
            return df
            
        except Exception as e:
            logger.error(f"获取期货 K 线数据失败，ts_code: {ts_code}, 错误: {e}")
            return None

    def convert_ts_code_to_contract_code(self, ts_code: str) -> str:
        """将 Tushare 合约代码转换为标准合约代码。
        
        例如：CU2601.SHF -> CU2601
        
        Args:
            ts_code: Tushare 合约代码。
        
        Returns:
            str: 标准合约代码。
        """
        if '.' in ts_code:
            return ts_code.split('.')[0]
        return ts_code

    def convert_contract_code_to_ts_code(self, contract_code: str, exchange: Optional[str] = None) -> str:
        """将标准合约代码转换为 Tushare 合约代码。
        
        例如：I2603 -> I2603.DCE（铁矿石），CU2601 -> CU2601.SHF
        单字母品种（如 I 铁矿石、C 玉米）必须用完整品种-交易所映射，否则会误判为 SHF。
        
        Args:
            contract_code: 标准合约代码。
            exchange: 交易所代码（可选），如果不提供则尝试推断。
        
        Returns:
            str: Tushare 合约代码。
        """
        if '.' in contract_code:
            return contract_code
        
        # 交易所后缀映射
        exchange_suffix_map = {
            'SHFE': 'SHF',
            'DCE': 'DCE',
            'CZCE': 'ZCE',
            'CFFEX': 'CFX',
            'INE': 'INE',
            'GFEX': 'GFE',
        }
        
        if exchange and exchange in exchange_suffix_map:
            return f"{contract_code}.{exchange_suffix_map[exchange]}"
        
        # 从合约代码中提取品种部分（仅字母）：I2603->I, CU2601->CU, SS2606->SS
        symbol_match = re.match(r'^([A-Za-z]+)', contract_code)
        symbol = symbol_match.group(1).upper() if symbol_match else contract_code[:1].upper()
        
        # 品种 -> Tushare 交易所后缀（SHF/DCE/ZCE/CFX/INE/GFE）
        # 单字母品种：C/A/M/Y/P/L/V/I/J/T 等易被 contract_code[:2] 误判，必须显式映射
        SYMBOL_EXCHANGE_SUFFIX = {
            # 中金所 CFFEX -> CFX
            'IF': 'CFX', 'IH': 'CFX', 'IC': 'CFX', 'IM': 'CFX',
            'T': 'CFX', 'TF': 'CFX', 'TS': 'CFX', 'TL': 'CFX',
            # 大商所 DCE -> DCE
            'C': 'DCE', 'A': 'DCE', 'M': 'DCE', 'Y': 'DCE', 'P': 'DCE', 'JD': 'DCE',
            'L': 'DCE', 'V': 'DCE', 'PP': 'DCE', 'EB': 'DCE', 'EG': 'DCE',
            'I': 'DCE', 'J': 'DCE', 'JM': 'DCE', 'FB': 'DCE', 'BB': 'DCE', 'LG': 'DCE',
            # 郑商所 CZCE -> ZCE
            'CF': 'ZCE', 'SR': 'ZCE', 'TA': 'ZCE', 'OI': 'ZCE', 'MA': 'ZCE', 'FG': 'ZCE',
            'RM': 'ZCE', 'ZC': 'ZCE', 'SF': 'ZCE', 'SM': 'ZCE', 'AP': 'ZCE', 'CJ': 'ZCE',
            'UR': 'ZCE', 'SA': 'ZCE', 'PF': 'ZCE', 'PK': 'ZCE', 'LH': 'ZCE', 'RI': 'ZCE',
            'LR': 'ZCE', 'JR': 'ZCE', 'PM': 'ZCE', 'WH': 'ZCE', 'CY': 'ZCE', 'PL': 'ZCE',
            'SH': 'ZCE',
            # 上期所 SHFE -> SHF
            'CU': 'SHF', 'AL': 'SHF', 'ZN': 'SHF', 'PB': 'SHF', 'NI': 'SHF', 'SN': 'SHF',
            'AU': 'SHF', 'AG': 'SHF', 'RB': 'SHF', 'HC': 'SHF', 'SS': 'SHF', 'BU': 'SHF',
            'RU': 'SHF', 'FU': 'SHF', 'WR': 'SHF', 'SP': 'SHF', 'AO': 'SHF', 'BC': 'SHF', 'BR': 'SHF',
            # 上期能源 INE -> INE
            'SC': 'INE', 'LU': 'INE', 'NR': 'INE', 'EC': 'INE',
            # 广期所 GFEX -> GFE
            'SI': 'GFE', 'LC': 'GFE',
        }
        
        if symbol in SYMBOL_EXCHANGE_SUFFIX:
            return f"{contract_code}.{SYMBOL_EXCHANGE_SUFFIX[symbol]}"
        
        # 未匹配时默认 SHFE（历史兼容）
        return f"{contract_code}.SHF"

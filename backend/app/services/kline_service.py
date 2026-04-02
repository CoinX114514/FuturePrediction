"""K 线数据服务。

负责从行情后端（Tushare 或本地 JSON）组装期货历史 K 线（OHLCV）。
"""

import logging
import re
import time
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from app.services.market_backend import get_market_backend
from app.database.connection import SessionLocal
from app.database.models import FuturesContract

# 配置日志
logger = logging.getLogger(__name__)


class KlineService:
    """K 线数据服务类。

    数据源由 MARKET_DATA_SOURCE 决定。
    """
    
    def __init__(self):
        """初始化 K 线服务。"""
        self.market_data_service = get_market_backend()

    def get_futures_daily_kline(
        self,
        contract_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: int = 365
    ) -> List[Dict]:
        """获取期货合约的历史日线 K 线数据。

        使用 Tushare fut_daily 或 JSON klines 拉取日线。

        Args:
            contract_code: 合约代码，如 "IF2603"、"CU2601"。
            start_date: 开始日期，格式 "YYYYMMDD"，如果为 None 则使用 period 计算。
            end_date: 结束日期，格式 "YYYYMMDD"，如果为 None 则使用当前日期。
            period: 获取最近多少天的数据（当 start_date 为 None 时使用），默认 365 天。

        Returns:
            List[Dict]: K 线数据列表，每个字典包含：
                {
                    "time": "2024-01-01",  # 日期字符串
                    "open": 3500.5,        # 开盘价
                    "high": 3520.0,        # 最高价
                    "low": 3490.0,         # 最低价
                    "close": 3510.5,       # 收盘价
                    "volume": 123456       # 成交量（可选）
                }
        """
        t_wall = time.monotonic()
        try:
            # 统一为去掉首尾空格、大写的合约代码（与现价逻辑一致）
            code_clean = (contract_code or "").strip().upper()
            if not code_clean:
                logger.warning("合约代码为空")
                return []

            logger.info(f"正在获取期货历史 K 线数据，合约代码: {code_clean}")

            # 如果没有指定日期，使用 period 计算开始日期
            if end_date is None:
                end_date = datetime.now().strftime("%Y%m%d")
            
            if start_date is None:
                start_date_obj = datetime.now() - timedelta(days=period)
                start_date = start_date_obj.strftime("%Y%m%d")

            logger.info(f"获取日期范围: {start_date} 到 {end_date} (请求 {period} 天数据)")

            # 若库里有该合约记录（futures_sync 写入），优先用语义正确的交易所推断 ts_code，避免 PT/PR 等默认误判为 SHF
            exchange_hint = None
            _db = SessionLocal()
            try:
                _fc = (
                    _db.query(FuturesContract)
                    .filter(FuturesContract.contract_code == code_clean)
                    .first()
                )
                if _fc and getattr(_fc, "exchange_code", None):
                    exchange_hint = str(_fc.exchange_code).strip().upper() or None
            finally:
                _db.close()

            ts_code = self.market_data_service.convert_contract_code_to_ts_code(
                code_clean, exchange_hint
            )
            logger.info(
                "K线 ts_code=%s（合约=%s，exchange_hint=%s）",
                ts_code,
                code_clean,
                exchange_hint or "无，走品种映射/默认",
            )
            
            kline_data = self.market_data_service.get_futures_kline(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                period=period
            )

            # 库中 futures_contracts.exchange 若与 Tushare 不一致（如 PT 误存为 CZCE），首次会空表；再按品种映射不重试 exchange_hint
            if (
                (kline_data is None or not isinstance(kline_data, pd.DataFrame) or kline_data.empty)
                and exchange_hint
            ):
                ts_fb = self.market_data_service.convert_contract_code_to_ts_code(code_clean, None)
                if ts_fb != ts_code:
                    logger.warning(
                        "K线首次无数据，忽略库交易所=%s，改用品种映射 ts_code=%s",
                        exchange_hint,
                        ts_fb,
                    )
                    ts_code = ts_fb
                    kline_data = self.market_data_service.get_futures_kline(
                        ts_code=ts_code,
                        start_date=start_date,
                        end_date=end_date,
                        period=period,
                    )

            # 广期所铂 PT 曾易被误判为郑商所/上期所；最后再强制试 GFE
            if (kline_data is None or not isinstance(kline_data, pd.DataFrame) or kline_data.empty) and re.match(
                r"^PT\d+", code_clean
            ):
                ts_pt = f"{code_clean}.GFE"
                if ts_pt != ts_code:
                    logger.warning("K线仍无数据，PT 合约强制尝试广期所 ts_code=%s", ts_pt)
                    ts_code = ts_pt
                    kline_data = self.market_data_service.get_futures_kline(
                        ts_code=ts_code,
                        start_date=start_date,
                        end_date=end_date,
                        period=period,
                    )

            if kline_data is None or not isinstance(kline_data, pd.DataFrame) or kline_data.empty:
                logger.warning(f"无法获取合约 {code_clean} 的 K 线数据，最后 ts_code={ts_code}")
                return []

            logger.info(f"成功获取 {len(kline_data)} 条 K 线数据")

            # 处理数据：转换为标准格式
            kline_list = []
            
            # 与 fut_daily 风格一致的列名（JSON 转 DataFrame 后相同）
            date_col = 'trade_date'
            open_col = 'open'
            high_col = 'high'
            low_col = 'low'
            close_col = 'close'
            volume_col = 'vol'
            
            # 检查必需的列是否存在
            required_cols = [date_col, open_col, high_col, low_col, close_col]
            if not all(col in kline_data.columns for col in required_cols):
                logger.error(f"无法找到必需的列，合约={code_clean}。可用列: {list(kline_data.columns)}")
                return []
            
            # 转换数据
            for _, row in kline_data.iterrows():
                try:
                    # 处理日期（YYYYMMDD 字符串）
                    date_value = row[date_col]
                    if isinstance(date_value, str):
                        # 八位数字 YYYYMMDD
                        if len(date_value) == 8:
                            time_str = f"{date_value[:4]}-{date_value[4:6]}-{date_value[6:8]}"
                        else:
                            try:
                                date_obj = pd.to_datetime(date_value)
                                time_str = date_obj.strftime("%Y-%m-%d")
                            except:
                                time_str = str(date_value)
                    elif pd.notna(date_value):
                        if isinstance(date_value, float):
                            date_value = int(date_value)
                        ds = str(date_value).strip()
                        if len(ds) >= 8 and ds[:8].isdigit():
                            ds = ds[:8]
                            time_str = f"{ds[:4]}-{ds[4:6]}-{ds[6:8]}"
                        else:
                            time_str = pd.to_datetime(ds).strftime("%Y-%m-%d")
                    else:
                        continue
                    
                    # 处理价格（转换为浮点数）；Tushare 部分行 OHLC 空缺时用 settle 补全
                    settle_price = None
                    if 'settle' in kline_data.columns and pd.notna(row.get('settle')):
                        try:
                            settle_price = float(row['settle'])
                            if np.isnan(settle_price):
                                settle_price = None
                        except (TypeError, ValueError):
                            settle_price = None

                    open_price = float(row[open_col]) if pd.notna(row[open_col]) else None
                    high_price = float(row[high_col]) if pd.notna(row[high_col]) else None
                    low_price = float(row[low_col]) if pd.notna(row[low_col]) else None
                    close_price = float(row[close_col]) if pd.notna(row[close_col]) else None

                    if open_price is None or np.isnan(open_price):
                        open_price = settle_price
                    if high_price is None or np.isnan(high_price):
                        high_price = settle_price
                    if low_price is None or np.isnan(low_price):
                        low_price = settle_price
                    if close_price is None or np.isnan(close_price):
                        close_price = settle_price

                    if any(p is None or (isinstance(p, float) and np.isnan(p)) for p in [open_price, high_price, low_price, close_price]):
                        continue

                    # lightweight-charts 要求 high/low 包住实体与影线，源数据偶发错乱时做一次修正
                    high_price = float(max(high_price, open_price, close_price))
                    low_price = float(min(low_price, open_price, close_price))
                    if high_price < low_price:
                        high_price = low_price = float(close_price)
                    
                    # 处理成交量（可选）
                    volume = None
                    if volume_col in kline_data.columns:
                        vol_value = row[volume_col]
                        if pd.notna(vol_value):
                            try:
                                volume = int(float(vol_value))
                            except:
                                pass
                    
                    kline_item = {
                        "time": time_str,
                        "open": open_price,
                        "high": high_price,
                        "low": low_price,
                        "close": close_price,
                    }
                    
                    if volume is not None:
                        kline_item["volume"] = volume
                    
                    kline_list.append(kline_item)
                    
                except Exception as e:
                    logger.warning(f"处理 K 线数据行时出错: {str(e)}")
                    continue
            
            # 按日期排序（从早到晚）；同一日多行时保留最后一行（避免 lightweight-charts 报重复时间）
            kline_list.sort(key=lambda x: x["time"])
            dedup: Dict[str, dict] = {}
            for it in kline_list:
                dedup[it["time"]] = it
            kline_list = [dedup[k] for k in sorted(dedup.keys())]
            
            # 记录实际获取到的日期范围
            if kline_list:
                first_date = kline_list[0]["time"]
                last_date = kline_list[-1]["time"]
                logger.info(f"成功处理 {len(kline_list)} 条 K 线数据，实际日期范围: {first_date} 到 {last_date}")
                
                # 检查数据是否是最新的
                today = datetime.now().strftime("%Y-%m-%d")
                if last_date < today:
                    logger.warning(f"⚠️ 数据可能不是最新的，最后日期: {last_date}，今天: {today}")
            else:
                logger.warning("处理后的 K 线数据为空")
            
            elapsed_ms = (time.monotonic() - t_wall) * 1000
            logger.info(
                "[K线服务] 合约=%s 总耗时=%.0fms 输出条数=%s",
                code_clean,
                elapsed_ms,
                len(kline_list),
            )
            return kline_list
            
        except Exception as e:
            code_clean = (contract_code or "").strip().upper()
            elapsed_ms = (time.monotonic() - t_wall) * 1000
            logger.error(
                "获取 K 线数据时发生错误，合约代码: %s, 耗时=%.0fms, 错误: %s",
                code_clean,
                elapsed_ms,
                str(e),
                exc_info=True,
            )
            return []

    def get_futures_kline_for_chart(
        self,
        contract_code: str,
        period: int = 365
    ) -> Dict:
        """获取期货合约的 K 线数据，格式化为图表库需要的格式。

        Args:
            contract_code: 合约代码。
            period: 获取最近多少天的数据，默认 365 天。

        Returns:
            Dict: 包含 K 线数据和元信息的字典：
                {
                    "contract_code": "IF2312",
                    "data": [...],  # K 线数据列表
                    "count": 100,   # 数据条数
                    "period": 365   # 数据周期
                }
        """
        kline_data = self.get_futures_daily_kline(contract_code, period=period)
        
        return {
            "contract_code": contract_code,
            "data": kline_data,
            "count": len(kline_data),
            "period": period
        }


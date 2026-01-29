"""K 线数据服务。

负责从 Tushare 获取期货合约的历史 K 线数据（OHLCV）。
"""

import logging
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from app.services.tushare_service import TushareService

# 配置日志
logger = logging.getLogger(__name__)


class KlineService:
    """K 线数据服务类。

    提供从 Tushare 获取期货历史 K 线数据的功能。
    """
    
    def __init__(self):
        """初始化 K 线服务。"""
        self.tushare_service = TushareService()

    def get_futures_daily_kline(
        self,
        contract_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: int = 365
    ) -> List[Dict]:
        """获取期货合约的历史日线 K 线数据。

        使用 Tushare 的 fut_daily 接口获取历史日线数据。

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

            # 将合约代码转换为 Tushare 格式（如 PP2603 -> PP2603.DCE）
            ts_code = self.tushare_service.convert_contract_code_to_ts_code(code_clean)
            
            # 使用 Tushare fut_daily 拉取历史日线（按 ts_code + 日期区间）
            kline_data = self.tushare_service.get_futures_kline(
                ts_code=ts_code,
                start_date=start_date,
                end_date=end_date,
                period=period
            )

            if kline_data is None or not isinstance(kline_data, pd.DataFrame) or kline_data.empty:
                logger.warning(f"无法获取合约 {code_clean} 的 K 线数据，ts_code={ts_code}")
                return []

            logger.info(f"成功获取 {len(kline_data)} 条 K 线数据")

            # 处理数据：转换为标准格式
            kline_list = []
            
            # Tushare 返回的列名
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
                    # 处理日期（Tushare 返回 YYYYMMDD 格式）
                    date_value = row[date_col]
                    if isinstance(date_value, str):
                        # Tushare 返回 YYYYMMDD 格式
                        if len(date_value) == 8:
                            time_str = f"{date_value[:4]}-{date_value[4:6]}-{date_value[6:8]}"
                        else:
                            try:
                                date_obj = pd.to_datetime(date_value)
                                time_str = date_obj.strftime("%Y-%m-%d")
                            except:
                                time_str = str(date_value)
                    elif pd.notna(date_value):
                        time_str = pd.to_datetime(str(date_value)).strftime("%Y-%m-%d")
                    else:
                        continue
                    
                    # 处理价格（转换为浮点数）
                    open_price = float(row[open_col]) if pd.notna(row[open_col]) else None
                    high_price = float(row[high_col]) if pd.notna(row[high_col]) else None
                    low_price = float(row[low_col]) if pd.notna(row[low_col]) else None
                    close_price = float(row[close_col]) if pd.notna(row[close_col]) else None
                    
                    # 检查价格是否有效
                    if any(p is None or np.isnan(p) for p in [open_price, high_price, low_price, close_price]):
                        continue
                    
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
            
            # 按日期排序（从早到晚）
            kline_list.sort(key=lambda x: x["time"])
            
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
            
            return kline_list
            
        except Exception as e:
            code_clean = (contract_code or "").strip().upper()
            logger.error(f"获取 K 线数据时发生错误，合约代码: {code_clean}, 错误: {str(e)}", exc_info=True)
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


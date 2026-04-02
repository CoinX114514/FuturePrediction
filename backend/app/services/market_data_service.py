"""本地行情数据服务（可调试、无第三方行情 SDK）。

设计原因：
1. 境外服务器常无法稳定访问 Tushare 等大陆网关，外部 SDK 增加排障难度。
2. 用单一 JSON 文件作为「现价 + K 线」数据源，改文件即生效（每次请求重新读取），调试路径清晰。
3. 生产环境可将 MARKET_DATA_JSON 指向挂载卷中的文件，无需改代码发版。

JSON 结构示例见 backend/data/market_data.json。
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)

# 默认数据文件：backend/data/market_data.json（Docker 内为 /opt/app/backend/data/market_data.json）
_DEFAULT_REL = Path(__file__).resolve().parent.parent.parent / "data" / "market_data.json"


def _env_path() -> Path:
    """返回 MARKET_DATA_JSON 配置的绝对路径。"""
    raw = os.getenv("MARKET_DATA_JSON", "").strip()
    if raw:
        return Path(raw).expanduser()
    return _DEFAULT_REL


def _load_raw() -> Dict[str, Any]:
    """从磁盘读取 JSON；失败则返回空字典并打日志。"""
    path = _env_path()
    if not path.is_file():
        logger.warning("[行情JSON] 文件不存在: %s（可设置环境变量 MARKET_DATA_JSON）", path)
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            logger.error("[行情JSON] 根节点必须是对象: %s", path)
            return {}
        return data
    except Exception as e:
        logger.error("[行情JSON] 读取失败 %s: %s", path, e, exc_info=True)
        return {}


def _normalize_contract_key(code: str) -> str:
    """统一合约主键：大写、去空格。"""
    return (code or "").strip().upper()


class MarketDataService:
    """本地 JSON 驱动的期货现价与 K 线服务。"""

    def __init__(self) -> None:
        """初始化服务（不抛错，缺失文件时各接口返回空/None）。"""
        pass

    def convert_contract_code_to_ts_code(
        self, contract_code: str, exchange: Optional[str] = None
    ) -> str:
        """将标准合约代码转为「带交易所后缀」的代码（与旧 Tushare 命名兼容，便于 JSON 键一致）。

        Args:
            contract_code: 如 CU2601、TL2603。
            exchange: 可选交易所简称。

        Returns:
            str: 如 CU2601.SHF、TL2603.CFX。
        """
        if "." in contract_code:
            return contract_code

        exchange_suffix_map = {
            "SHFE": "SHF",
            "DCE": "DCE",
            "CZCE": "ZCE",
            "CFFEX": "CFX",
            "INE": "INE",
            "GFEX": "GFE",
        }
        if exchange and exchange in exchange_suffix_map:
            return f"{contract_code}.{exchange_suffix_map[exchange]}"

        symbol_match = re.match(r"^([A-Za-z]+)", contract_code)
        symbol = (
            symbol_match.group(1).upper() if symbol_match else contract_code[:1].upper()
        )

        SYMBOL_EXCHANGE_SUFFIX = {
            "IF": "CFX",
            "IH": "CFX",
            "IC": "CFX",
            "IM": "CFX",
            "T": "CFX",
            "TF": "CFX",
            "TS": "CFX",
            "TL": "CFX",
            "C": "DCE",
            "A": "DCE",
            "M": "DCE",
            "Y": "DCE",
            "P": "DCE",
            "JD": "DCE",
            "L": "DCE",
            "V": "DCE",
            "PP": "DCE",
            "EB": "DCE",
            "EG": "DCE",
            "I": "DCE",
            "J": "DCE",
            "JM": "DCE",
            "FB": "DCE",
            "BB": "DCE",
            "LG": "DCE",
            "CF": "ZCE",
            "SR": "ZCE",
            "TA": "ZCE",
            "OI": "ZCE",
            "MA": "ZCE",
            "FG": "ZCE",
            "RM": "ZCE",
            "ZC": "ZCE",
            "SF": "ZCE",
            "SM": "ZCE",
            "AP": "ZCE",
            "CJ": "ZCE",
            "UR": "ZCE",
            "SA": "ZCE",
            "PF": "ZCE",
            "PK": "ZCE",
            "LH": "ZCE",
            "RI": "ZCE",
            "LR": "ZCE",
            "JR": "ZCE",
            "PM": "ZCE",
            "WH": "ZCE",
            "CY": "ZCE",
            "PL": "ZCE",
            "SH": "ZCE",
            "PR": "ZCE",
            "CU": "SHF",
            "AL": "SHF",
            "ZN": "SHF",
            "PB": "SHF",
            "NI": "SHF",
            "SN": "SHF",
            "AU": "SHF",
            "AG": "SHF",
            "RB": "SHF",
            "HC": "SHF",
            "SS": "SHF",
            "BU": "SHF",
            "RU": "SHF",
            "FU": "SHF",
            "WR": "SHF",
            "SP": "SHF",
            "AO": "SHF",
            "BC": "SHF",
            "BR": "SHF",
            "SC": "INE",
            "LU": "INE",
            "NR": "INE",
            "EC": "INE",
            "SI": "GFE",
            "LC": "GFE",
            "PT": "GFE",
            "PD": "GFE",
        }
        if symbol in SYMBOL_EXCHANGE_SUFFIX:
            return f"{contract_code}.{SYMBOL_EXCHANGE_SUFFIX[symbol]}"
        return f"{contract_code}.SHF"

    def convert_ts_code_to_contract_code(self, ts_code: str) -> str:
        """ts_code 转无后缀合约代码。"""
        if "." in ts_code:
            return ts_code.split(".")[0]
        return ts_code

    def _pick_price(self, raw: Dict[str, Any], contract_code: str) -> Optional[float]:
        """从已加载的 raw 中取现价。"""
        prices = raw.get("prices")
        if not isinstance(prices, dict):
            return None
        key = _normalize_contract_key(contract_code)
        if key in prices:
            v = prices[key]
            return float(v) if v is not None else None
        base = self.convert_ts_code_to_contract_code(key)
        if base != key and base in prices:
            v = prices[base]
            return float(v) if v is not None else None
        return None

    def get_futures_price(self, contract_code: str) -> Optional[float]:
        """读取指定合约的现价（来自 JSON prices 字段）。

        Args:
            contract_code: 如 CU2601 或 CU2601.SHF。

        Returns:
            Optional[float]: 无则 None。
        """
        raw = _load_raw()
        path = _env_path()
        price = self._pick_price(raw, contract_code)
        logger.info(
            "[行情JSON] get_futures_price contract=%s path=%s ok=%s",
            contract_code,
            path,
            price is not None,
        )
        return price

    def batch_get_futures_prices(
        self, contract_codes: List[str]
    ) -> Dict[str, Optional[float]]:
        """批量读取现价（单次读文件，多次查键）。

        Args:
            contract_codes: 合约代码列表。

        Returns:
            Dict[str, Optional[float]]: 合约到价格。
        """
        raw = _load_raw()
        path = _env_path()
        out: Dict[str, Optional[float]] = {}
        for c in contract_codes:
            if not c:
                continue
            key = _normalize_contract_key(c)
            out[key] = self._pick_price(raw, key)
        logger.info(
            "[行情JSON] batch_get path=%s 请求数=%s 命中=%s",
            path,
            len(contract_codes),
            sum(1 for v in out.values() if v is not None),
        )
        return out

    def _pick_kline_rows(self, raw: Dict[str, Any], ts_code: str) -> List[Dict[str, Any]]:
        """从 raw['klines'] 取 K 线数组，键可为 ts_code 或无后缀代码。"""
        klines = raw.get("klines")
        if not isinstance(klines, dict):
            return []
        ts = _normalize_contract_key(ts_code)
        if ts in klines and isinstance(klines[ts], list):
            return klines[ts]
        base = self.convert_ts_code_to_contract_code(ts)
        if base in klines and isinstance(klines[base], list):
            return klines[base]
        return []

    def get_futures_kline(
        self,
        ts_code: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        period: int = 365,
    ) -> Optional[pd.DataFrame]:
        """从 JSON 构建与旧接口兼容的 DataFrame（列含 trade_date, open, high, low, close, vol）。

        Args:
            ts_code: 如 TL2603.CFX。
            start_date: YYYYMMDD。
            end_date: YYYYMMDD。
            period: 当未给 start_date 时用于回推天数。

        Returns:
            Optional[pd.DataFrame]: 无数据则 None 或空表。
        """
        from datetime import datetime, timedelta

        raw = _load_raw()
        path = _env_path()
        rows_in = self._pick_kline_rows(raw, ts_code)
        if not rows_in:
            logger.warning("[行情JSON] 无 K 线数据 ts_code=%s path=%s", ts_code, path)
            return None

        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=period)).strftime("%Y%m%d")

        rows_out: List[Dict[str, Any]] = []
        for row in rows_in:
            if not isinstance(row, dict):
                continue
            t = row.get("time") or row.get("trade_date")
            if not t:
                continue
            if isinstance(t, str) and len(t) >= 10 and t[4] == "-":
                td = t[:4] + t[5:7] + t[8:10]
            elif isinstance(t, str) and len(t) == 8 and t.isdigit():
                td = t
            else:
                continue
            if td < start_date or td > end_date:
                continue
            try:
                o = float(row["open"])
                h = float(row["high"])
                l = float(row["low"])
                cl = float(row["close"])
            except (KeyError, TypeError, ValueError):
                continue
            vol = row.get("volume") or row.get("vol")
            try:
                vol_i = int(float(vol)) if vol is not None else None
            except (TypeError, ValueError):
                vol_i = None
            rec: Dict[str, Any] = {
                "trade_date": td,
                "open": o,
                "high": h,
                "low": l,
                "close": cl,
            }
            if vol_i is not None:
                rec["vol"] = vol_i
            rows_out.append(rec)

        rows_out.sort(key=lambda x: x["trade_date"])
        logger.info(
            "[行情JSON] get_futures_kline ts_code=%s path=%s 条数=%s 区间=%s~%s",
            ts_code,
            path,
            len(rows_out),
            start_date,
            end_date,
        )
        if not rows_out:
            return pd.DataFrame()
        return pd.DataFrame(rows_out)

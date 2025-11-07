"""CSV 解析服务。

负责解析和标准化上传的 CSV 文件。
"""

import io
from typing import Dict, List, Optional

import pandas as pd


class CSVParser:
    """CSV 文件解析器。

    此类负责解析 CSV 文件，处理不同的编码格式，
    并标准化列名（支持中英文列名）。
    """

    # 列名映射表：标准列名 -> 可能的别名
    COLUMN_MAPPING: Dict[str, List[str]] = {
        "日期": ["date", "Date", "DATE", "时间", "datetime", "时间戳"],
        "开盘": ["open", "Open", "OPEN", "开盘价"],
        "最高": ["high", "High", "HIGH", "最高价"],
        "最低": ["low", "Low", "LOW", "最低价"],
        "收盘": ["close", "Close", "CLOSE", "收盘价"],
        "成交量": ["volume", "Volume", "VOLUME", "vol", "成交量", "VOL"],
    }

    def __init__(self):
        """初始化 CSV 解析器。"""
        pass

    def parse_csv(self, file_contents: bytes, encoding: str = "utf-8") -> pd.DataFrame:
        """解析 CSV 文件内容。

        Args:
            file_contents: CSV 文件的字节内容。
            encoding: 文件编码，默认为 UTF-8。

        Returns:
            pd.DataFrame: 解析后的数据框。

        Raises:
            ValueError: 当文件无法解析时抛出。
        """
        try:
            # 尝试使用指定编码读取
            # 注意：不自动解析日期，保持CSV的原始顺序
            try:
                df = pd.read_csv(
                    io.BytesIO(file_contents),
                    encoding=encoding,
                    parse_dates=False,  # 不自动解析日期，保持原始顺序
                    keep_default_na=False,  # 保持空值为空字符串，不转换为NaN
                )
            except UnicodeDecodeError:
                # 如果 UTF-8 失败，尝试其他常见编码
                for enc in ["gbk", "gb2312", "latin1"]:
                    try:
                        df = pd.read_csv(
                            io.BytesIO(file_contents),
                            encoding=enc,
                            parse_dates=False,  # 不自动解析日期，保持原始顺序
                            keep_default_na=False,  # 保持空值为空字符串，不转换为NaN
                        )
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    raise ValueError("无法解析文件编码，请确保文件为 UTF-8 或 GBK 编码")

            # 标准化列名
            df = self._normalize_columns(df)

            return df

        except pd.errors.EmptyDataError:
            raise ValueError("CSV 文件为空")
        except Exception as e:
            raise ValueError(f"CSV 解析失败: {str(e)}")

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """标准化列名。

        将各种可能的列名映射为标准的中文列名。

        Args:
            df: 原始数据框。

        Returns:
            pd.DataFrame: 列名已标准化的数据框。
        """
        column_mapping = {}

        # 创建反向映射：别名 -> 标准名
        for standard_name, aliases in self.COLUMN_MAPPING.items():
            for alias in aliases:
                column_mapping[alias.lower()] = standard_name
                column_mapping[alias] = standard_name

        # 标准化列名（去除空格，转为小写进行匹配）
        new_columns = {}
        for col in df.columns:
            col_clean = col.strip()
            col_lower = col_clean.lower()

            # 检查是否在映射表中
            if col_lower in column_mapping:
                new_columns[col] = column_mapping[col_lower]
            elif col_clean in column_mapping:
                new_columns[col] = column_mapping[col_clean]
            else:
                # 如果不在映射表中，保持原样
                new_columns[col] = col_clean

        df = df.rename(columns=new_columns)

        return df


"""数据验证服务。

验证上传的 OHLCV 数据是否符合要求。
"""

from typing import Dict, List

import pandas as pd
import numpy as np


class DataValidator:
    """数据验证器。

    验证 OHLCV 数据的完整性和正确性。
    """

    # 必需的列名
    REQUIRED_COLUMNS = ["日期", "开盘", "最高", "最低", "收盘", "成交量"]

    def __init__(self):
        """初始化数据验证器。"""
        pass

    def validate_ohlcv(self, df: pd.DataFrame) -> Dict:
        """验证 OHLCV 数据。

        检查数据是否包含必需的列，以及数据的有效性。

        Args:
            df: 待验证的数据框。

        Returns:
            dict: 验证结果字典。
                - valid: 是否通过验证（bool）
                - errors: 错误信息列表（List[str]）
                - warnings: 警告信息列表（List[str]）
        """
        errors: List[str] = []
        warnings: List[str] = []
        
        # 创建数据框副本，避免修改原始数据
        df = df.copy()

        # 检查必需列是否存在
        missing_columns = []
        for col in self.REQUIRED_COLUMNS:
            if col not in df.columns:
                missing_columns.append(col)

        if missing_columns:
            errors.append(
                f"缺少必需的列: {', '.join(missing_columns)}。"
                f"请确保 CSV 文件包含以下列：{', '.join(self.REQUIRED_COLUMNS)}"
            )

        # 如果缺少必需列，直接返回，不进行进一步验证
        if errors:
            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
            }

        # 检查数据是否为空
        if len(df) == 0:
            errors.append("数据文件为空，请上传包含数据的 CSV 文件")
            return {
                "valid": False,
                "errors": errors,
                "warnings": warnings,
            }

        # 检查数值列的数据类型和有效性
        numeric_columns = ["开盘", "最高", "最低", "收盘", "成交量"]

        for col in numeric_columns:
            # 对于成交量列，需要特殊处理（可能包含逗号）
            if col == "成交量":
                # 先转换为字符串，移除逗号和引号，再转换为数值
                try:
                    # 处理可能包含逗号和引号的字符串格式
                    df[col] = df[col].astype(str).str.replace(',', '').str.replace('"', '').str.strip()
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                except Exception as e:
                    errors.append(f"列 '{col}' 无法转换为数值类型: {str(e)}")
            else:
                # 其他数值列直接转换
                try:
                    df[col] = pd.to_numeric(df[col], errors="coerce")
                except Exception:
                    errors.append(f"列 '{col}' 无法转换为数值类型")

            # 检查缺失值
            missing_count = df[col].isna().sum()
            if missing_count > 0:
                errors.append(
                    f"列 '{col}' 包含 {missing_count} 个缺失值，"
                    "请确保数据完整"
                )

            # 检查负值（价格和成交量不应为负）
            if col == "成交量":
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    warnings.append(
                        f"列 '成交量' 包含 {negative_count} 个负值，"
                        "这可能是数据错误"
                    )
            else:
                # 价格列不应为负或零
                invalid_count = (df[col] <= 0).sum()
                if invalid_count > 0:
                    errors.append(
                        f"列 '{col}' 包含 {invalid_count} 个无效值（≤0），"
                        "价格数据必须为正数"
                    )

        # 检查价格逻辑：最高 >= 最低，最高 >= 开盘，最高 >= 收盘等
        if "最高" in df.columns and "最低" in df.columns:
            invalid_high_low = (df["最高"] < df["最低"]).sum()
            if invalid_high_low > 0:
                errors.append(
                    f"发现 {invalid_high_low} 行数据中最高价小于最低价，"
                    "这是不合逻辑的"
                )

        if "最高" in df.columns and "开盘" in df.columns:
            invalid_high_open = (df["最高"] < df["开盘"]).sum()
            if invalid_high_open > 0:
                warnings.append(
                    f"发现 {invalid_high_open} 行数据中最高价小于开盘价"
                )

        if "最高" in df.columns and "收盘" in df.columns:
            invalid_high_close = (df["最高"] < df["收盘"]).sum()
            if invalid_high_close > 0:
                warnings.append(
                    f"发现 {invalid_high_close} 行数据中最高价小于收盘价"
                )

        if "最低" in df.columns and "开盘" in df.columns:
            invalid_low_open = (df["最低"] > df["开盘"]).sum()
            if invalid_low_open > 0:
                warnings.append(
                    f"发现 {invalid_low_open} 行数据中最低价大于开盘价"
                )

        if "最低" in df.columns and "收盘" in df.columns:
            invalid_low_close = (df["最低"] > df["收盘"]).sum()
            if invalid_low_close > 0:
                warnings.append(
                    f"发现 {invalid_low_close} 行数据中最低价大于收盘价"
                )

        # 检查日期列
        if "日期" in df.columns:
            try:
                df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
                invalid_dates = df["日期"].isna().sum()
                if invalid_dates > 0:
                    errors.append(
                        f"日期列包含 {invalid_dates} 个无效日期，"
                        "请确保日期格式正确"
                    )
            except Exception:
                errors.append("日期列无法解析，请确保日期格式正确")

        # 检查数据量是否足够（至少需要一定数量的历史数据用于预测）
        if len(df) < 10:
            warnings.append(
                "数据量较少（少于 10 行），可能影响预测准确性。"
                "建议提供更多的历史数据"
            )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }


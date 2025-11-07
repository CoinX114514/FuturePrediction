"""文件上传路由模块。

处理用户上传的 CSV 文件。
"""

import os
from typing import List

import pandas as pd
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.services.csv_parser import CSVParser
from app.services.data_validator import DataValidator
from app.middleware.auth import get_current_user
from app.utils.permissions import check_csv_upload_permission
from app.database.models import User

router = APIRouter()

# 创建上传目录
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    """上传并验证 CSV 文件。

    此端点接收用户上传的 CSV 文件，验证其格式和内容，
    确保包含必要的 OHLCV 列。

    注意：只有会员和管理员可以上传 CSV 文件。

    Args:
        file: 上传的文件对象，必须是 CSV 格式。
        current_user: 当前登录用户（通过依赖注入获取）。

    Returns:
        JSONResponse: 包含文件信息和验证结果的响应。
            - file_id: 文件唯一标识符
            - filename: 文件名
            - rows: 数据行数
            - columns: 列名列表
            - validated: 验证是否通过

    Raises:
        HTTPException: 当权限不足、文件格式不正确或验证失败时抛出。
    """
    # 检查 CSV 上传权限
    if not check_csv_upload_permission(current_user):
        raise HTTPException(
            status_code=403,
            detail="CSV 上传功能仅限会员使用，请升级为会员",
        )
    # 验证文件类型
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="文件格式错误：仅支持 CSV 格式文件",
        )

    try:
        # 读取文件内容
        contents = await file.read()

        # 解析 CSV
        parser = CSVParser()
        df = parser.parse_csv(contents)

        # 验证数据
        validator = DataValidator()
        validation_result = validator.validate_ohlcv(df)

        if not validation_result["valid"]:
            # 将错误列表转换为字符串
            error_details = validation_result["errors"]
            if isinstance(error_details, list):
                error_message = "数据验证失败: " + "; ".join(error_details)
            else:
                error_message = f"数据验证失败: {error_details}"
            
            raise HTTPException(
                status_code=400,
                detail=error_message,
            )

        # 保存文件（可选，用于后续处理）
        file_id = f"{file.filename}_{hash(contents) % 10000}"
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}.csv")
        with open(file_path, "wb") as f:
            f.write(contents)

        # 将 DataFrame 转换为 JSON 格式（用于前端显示）
        # 确保列名标准化
        column_mapping = {
            "日期": "日期",
            "开盘": "开盘",
            "最高": "最高",
            "最低": "最低",
            "收盘": "收盘",
            "成交量": "成交量",
        }
        
        # 获取标准化的列名
        ohlcv_df = df[["日期", "开盘", "最高", "最低", "收盘", "成交量"]].copy()
        
        # 将日期转换为字符串格式（处理 pandas 的日期类型）
        if "日期" in ohlcv_df.columns:
            if pd.api.types.is_datetime64_any_dtype(ohlcv_df["日期"]):
                ohlcv_df["日期"] = ohlcv_df["日期"].dt.strftime("%Y-%m-%d")
            else:
                ohlcv_df["日期"] = ohlcv_df["日期"].astype(str)
        
        # 转换为字典列表，确保数值类型正确
        data_records = []
        for _, row in ohlcv_df.iterrows():
            # 处理成交量：可能是字符串格式（带逗号），需要转换
            volume = row["成交量"]
            if isinstance(volume, str):
                # 移除逗号并转换为浮点数
                volume = float(volume.replace(',', '').replace('"', ''))
            else:
                volume = float(volume)
            
            record = {
                "日期": str(row["日期"]),
                "开盘": float(row["开盘"]),
                "最高": float(row["最高"]),
                "最低": float(row["最低"]),
                "收盘": float(row["收盘"]),
                "成交量": volume,
            }
            data_records.append(record)

        return JSONResponse(
            content={
                "file_id": file_id,
                "filename": file.filename,
                "rows": len(df),
                "columns": df.columns.tolist(),
                "validated": True,
                "data": data_records,  # 添加解析后的OHLCV数据
                "message": "文件上传成功",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"文件处理失败: {str(e)}",
        )


@router.get("/upload/validate")
async def validate_csv_format():
    """获取 CSV 文件格式要求说明。

    Returns:
        dict: 包含 CSV 格式要求的详细信息。
    """
    return {
        "required_columns": ["日期", "开盘", "最高", "最低", "收盘", "成交量"],
        "column_aliases": {
            "日期": ["date", "Date", "DATE", "时间", "datetime"],
            "开盘": ["open", "Open", "OPEN", "开盘价"],
            "最高": ["high", "High", "HIGH", "最高价"],
            "最低": ["low", "Low", "LOW", "最低价"],
            "收盘": ["close", "Close", "CLOSE", "收盘价"],
            "成交量": ["volume", "Volume", "VOLUME", "vol", "成交量"],
        },
        "format": "CSV 文件必须包含上述列（支持中英文列名）",
        "encoding": "推荐使用 UTF-8 编码",
    }


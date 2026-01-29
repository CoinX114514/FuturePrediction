"""K 线数据路由模块。

提供获取期货合约历史 K 线数据的 API 接口。
从 Tushare 拉取历史日线（fut_daily）供帖子内图表展示。
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.kline_service import KlineService

router = APIRouter()


@router.get("/{contract_code}")
async def get_kline_data(
    contract_code: str,
    period: int = Query(365, ge=1, le=3650, description="获取最近多少天的数据，默认 365 天"),
    start_date: Optional[str] = Query(None, description="开始日期，格式 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式 YYYYMMDD"),
    db: Session = Depends(get_db),
):
    """获取指定合约的历史 K 线数据。

    从 Tushare fut_daily 接口拉取历史日线，供帖子详情页 K 线图展示。

    Args:
        contract_code: 合约代码，如 "PP2603"、"IF2312"、"CU2401"。
        period: 获取最近多少天的数据（当未指定日期范围时使用）。
        start_date: 开始日期，格式 "YYYYMMDD"。
        end_date: 结束日期，格式 "YYYYMMDD"。
        db: 数据库会话。

    Returns:
        dict: 包含 K 线数据的字典。
    """
    try:
        kline_service = KlineService()
    except ValueError as e:
        # Tushare 未初始化（多为 TUSHARE_TOKEN 未配置或无效）
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="K 线数据依赖 Tushare，当前不可用。请在服务器配置有效的 TUSHARE_TOKEN 环境变量。",
        ) from e
    except ImportError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="K 线数据依赖 tushare 库，当前未安装或不可用。",
        ) from e

    try:
        result = kline_service.get_futures_kline_for_chart(
            contract_code=contract_code,
            period=period
        )
        
        if result["count"] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"未找到合约 {contract_code} 的 K 线数据（可能合约未上市或 Tushare 暂无该区间数据）",
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 K 线数据失败: {str(e)}",
        )


"""K 线数据路由模块。

提供获取期货合约历史 K 线数据的 API 接口。
数据来自 Tushare 或本地 JSON（MARKET_DATA_SOURCE）。

设计原因：读文件与 pandas 处理为同步阻塞，用 run_in_threadpool 避免阻塞事件循环。
"""

import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from starlette.concurrency import run_in_threadpool

from app.services.kline_service import KlineService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{contract_code}")
async def get_kline_data(
    contract_code: str,
    period: int = Query(365, ge=1, le=3650, description="获取最近多少天的数据，默认 365 天"),
    start_date: Optional[str] = Query(None, description="开始日期，格式 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式 YYYYMMDD"),
):
    """获取指定合约的历史 K 线数据。

    从行情 JSON 的 klines 字段读取，供帖子详情页 K 线图展示。

    Args:
        contract_code: 合约代码，如 "PP2603"、"IF2312"、"CU2401"。
        period: 获取最近多少天的数据（当未指定日期范围时使用）。
        start_date: 开始日期，格式 "YYYYMMDD"。
        end_date: 结束日期，格式 "YYYYMMDD"。
    Returns:
        dict: 包含 K 线数据的字典。
    """
    kline_service = KlineService()

    try:
        # 阻塞 IO 与 pandas 处理放到线程池，避免阻塞事件循环
        result = await run_in_threadpool(
            kline_service.get_futures_kline_for_chart,
            contract_code,
            period,
        )
        logger.info(
            "[K线API] contract=%s period=%s count=%s",
            contract_code,
            period,
            result.get("count"),
        )
        
        if result["count"] == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"未找到合约 {contract_code} 的 K 线数据（Tushare 无数据或未在 JSON 的 klines 配置）",
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 K 线数据失败: {str(e)}",
        )


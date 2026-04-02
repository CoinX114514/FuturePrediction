"""价格更新路由模块。

提供价格更新相关的 API 接口。

设计原因：PriceUpdateService 内部会同步读 JSON/数据库，若在 async 路由中直接执行会阻塞事件循环，
导致其它 API 超时。故在独立线程中执行，并在该线程内新建数据库会话（Session 非线程安全）。
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from starlette.concurrency import run_in_threadpool

from app.database.connection import SessionLocal
from app.database.models import User
from app.middleware.auth import get_current_user
from app.services.price_update_service import PriceUpdateService
from app.services.scheduler_service import scheduler_service

router = APIRouter()
logger = logging.getLogger(__name__)


def _update_all_posts_price_sync() -> dict:
    """在线程内执行批量更新现价（独立 DB 会话）。"""
    db = SessionLocal()
    try:
        return PriceUpdateService(db).update_all_posts_price()
    finally:
        db.close()


def _update_by_contract_sync(contract_code: str) -> dict:
    """在线程内按合约更新现价。"""
    db = SessionLocal()
    try:
        return PriceUpdateService(db).update_posts_by_contract_code(contract_code)
    finally:
        db.close()


def _update_single_post_sync(post_id: int) -> bool:
    """在线程内更新单帖现价。"""
    db = SessionLocal()
    try:
        return PriceUpdateService(db).update_post_price(post_id)
    finally:
        db.close()


@router.post("/update-all", status_code=status.HTTP_200_OK)
async def update_all_posts_price(
    current_user: User = Depends(get_current_user),
):
    """批量更新所有帖子的现价。

    只有管理员（user_role >= 3）可以调用此接口。

    Args:
        current_user: 当前登录用户。

    Returns:
        dict: 更新结果统计信息。

    Raises:
        HTTPException: 如果用户不是管理员则返回 403 错误。
    """
    # 权限检查：只有管理员可以更新价格
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以更新价格",
        )

    result = await run_in_threadpool(_update_all_posts_price_sync)
    logger.info(
        "[价格更新API] update-all total=%s success=%s failed=%s",
        result.get("total"),
        result.get("success"),
        result.get("failed"),
    )

    return {
        "message": "价格更新完成",
        "total": result["total"],
        "success": result["success"],
        "failed": result["failed"],
    }


@router.post("/update-by-contract", status_code=status.HTTP_200_OK)
async def update_posts_by_contract(
    contract_code: str = Query(..., description="合约代码，如 IF2312"),
    current_user: User = Depends(get_current_user),
):
    """按合约代码更新所有相关帖子的现价。

    只有管理员（user_role >= 3）可以调用此接口。

    Args:
        contract_code: 合约代码。
        current_user: 当前登录用户。

    Returns:
        dict: 更新结果统计信息。

    Raises:
        HTTPException: 如果用户不是管理员则返回 403 错误。
    """
    # 权限检查：只有管理员可以更新价格
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以更新价格",
        )

    result = await run_in_threadpool(_update_by_contract_sync, contract_code)

    return {
        "message": f"合约 {contract_code} 的价格更新完成",
        "contract_code": contract_code,
        "total": result["total"],
        "success": result["success"],
        "failed": result["failed"],
    }


@router.post("/update-post/{post_id}", status_code=status.HTTP_200_OK)
async def update_single_post_price(
    post_id: int,
    current_user: User = Depends(get_current_user),
):
    """更新单个帖子的现价。

    只有管理员（user_role >= 3）可以调用此接口。

    Args:
        post_id: 帖子ID。
        current_user: 当前登录用户。

    Returns:
        dict: 更新结果。

    Raises:
        HTTPException: 如果用户不是管理员或帖子不存在则返回相应错误。
    """
    # 权限检查：只有管理员可以更新价格
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以更新价格",
        )

    success = await run_in_threadpool(_update_single_post_sync, post_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无法获取价格",
        )

    return {
        "message": "价格更新成功",
        "post_id": post_id,
    }


@router.get("/status", status_code=status.HTTP_200_OK)
async def get_price_update_status(
    current_user: User = Depends(get_current_user),
):
    """获取价格更新定时任务状态。

    只有管理员（user_role >= 3）可以调用此接口。

    Args:
        current_user: 当前登录用户。

    Returns:
        dict: 定时任务状态信息。
    """
    # 权限检查：只有管理员可以查看状态
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看定时任务状态",
        )

    jobs = scheduler_service.get_jobs()
    price_job = None
    
    for job in jobs:
        if job.id == "price_update_job":
            price_job = job
            break

    if price_job:
        return {
            "status": "running" if not price_job.pending else "pending",
            "job_id": price_job.id,
            "name": price_job.name,
            "next_run_time": price_job.next_run_time.isoformat() if price_job.next_run_time else None,
            "trigger": str(price_job.trigger),
        }
    else:
        return {
            "status": "not_found",
            "message": "价格更新定时任务未找到",
        }


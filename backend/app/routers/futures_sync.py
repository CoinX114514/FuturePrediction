"""期货合约同步路由模块。

提供期货合约同步相关的 API 接口。
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.middleware.auth import get_current_user
from app.services.futures_sync_service import FuturesSyncService

router = APIRouter()


@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_futures_contracts(
    update_existing: bool = Query(False, description="是否更新已存在的帖子"),
    include_continuous: bool = Query(False, description="是否包含加权连续合约"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """同步期货合约到帖子。

    从 akshare 获取所有可用期货合约，并为每个合约创建对应的帖子卡片。
    只有管理员（user_role >= 3）可以调用此接口。

    Args:
        update_existing: 是否更新已存在的帖子（默认 False，只创建新帖子）。
        include_continuous: 是否包含加权连续合约（默认 False，只同步主力合约）。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 同步结果统计信息。

    Raises:
        HTTPException: 如果用户不是管理员则返回 403 错误。
    """
    # 权限检查：只有管理员可以同步合约
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以同步期货合约",
        )

    sync_service = FuturesSyncService(db)
    result = sync_service.sync_futures_to_posts(
        author_id=current_user.user_id,
        update_existing=update_existing,
        include_continuous=include_continuous
    )

    return {
        "message": "期货合约同步完成",
        "total": result["total"],
        "created": result["created"],
        "updated": result["updated"],
        "skipped": result["skipped"],
        "failed": result["failed"],
    }


@router.get("/contracts", status_code=status.HTTP_200_OK)
async def get_futures_contracts(
    include_continuous: bool = Query(False, description="是否包含加权连续合约"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取所有可用的期货合约列表（不创建帖子）。

    只有管理员（user_role >= 3）可以调用此接口。

    Args:
        include_continuous: 是否包含加权连续合约（默认 False，只返回主力合约）。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 期货合约列表。

    Raises:
        HTTPException: 如果用户不是管理员则返回 403 错误。
    """
    # 权限检查：只有管理员可以查看合约列表
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以查看期货合约列表",
        )

    sync_service = FuturesSyncService(db)
    contracts = sync_service.get_all_futures_contracts(include_continuous=include_continuous)

    return {
        "message": "获取期货合约列表成功",
        "total": len(contracts),
        "contracts": contracts,
    }


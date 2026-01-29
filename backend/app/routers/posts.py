"""帖子路由模块。

处理帖子相关的API请求。
"""

from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.middleware.auth import get_current_user, get_optional_user
from app.services.post_service import PostService
from app.services.browse_history_service import BrowseHistoryService
from app.services.collection_service import CollectionService

router = APIRouter()


class PostCreateRequest(BaseModel):
    """创建帖子请求数据模型。"""

    title: str
    contract_code: str
    stop_loss: float
    content: str
    take_profit: Optional[float] = None
    strike_price: Optional[float] = None
    current_price: Optional[float] = None
    direction: Optional[str] = 'buy'  # 'buy' 做多, 'sell' 做空
    suggestion: Optional[str] = None
    k_line_image: Optional[str] = None
    sector_id: Optional[int] = None


class PostUpdateRequest(BaseModel):
    """更新帖子请求数据模型。"""

    title: Optional[str] = None
    contract_code: Optional[str] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    strike_price: Optional[float] = None
    current_price: Optional[float] = None
    direction: Optional[str] = None  # 'buy' 做多, 'sell' 做空
    suggestion: Optional[str] = None
    content: Optional[str] = None
    k_line_image: Optional[str] = None
    sector_id: Optional[int] = None


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_post(
    request: PostCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建新帖子。

    只有管理员（user_role >= 3）可以发布帖子。

    Args:
        request: 创建帖子请求数据。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 创建的帖子信息。

    Raises:
        HTTPException: 如果用户不是管理员则返回 403 错误。
    """
    # 权限检查：只有管理员可以发布帖子
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以发布帖子",
        )
    
    post_service = PostService(db)
    post = post_service.create_post(
        author_id=current_user.user_id,
        title=request.title,
        contract_code=request.contract_code,
        stop_loss=request.stop_loss,
        content=request.content,
        take_profit=request.take_profit,
        strike_price=request.strike_price,
        current_price=request.current_price,
        direction=request.direction or 'buy',
        suggestion=request.suggestion,
        k_line_image=request.k_line_image,
        sector_id=request.sector_id,
    )

    return {
        "post_id": post.post_id,
        "title": post.title,
        "contract_code": post.contract_code,
        "publish_time": post.publish_time.isoformat(),
    }


@router.get("")
async def get_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sector_id: Optional[int] = Query(None),
    author_id: Optional[Union[int, str]] = Query(None),
    search: Optional[str] = Query(None, description="搜索关键词，用于搜索合约代码或标题"),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """获取帖子列表。

    Args:
        page: 页码。
        page_size: 每页数量。
        sector_id: 板块ID筛选。
        author_id: 作者ID筛选。如果传入 'current' 字符串，则筛选当前用户的帖子。
        search: 搜索关键词，用于搜索合约代码或标题。
        current_user: 当前登录用户（可选，用于author_id='current'的情况）。
        db: 数据库会话。

    Returns:
        dict: 帖子列表和分页信息。
    """
    # 处理 author_id 过滤逻辑
    actual_author_id: Optional[int] = None
    if isinstance(author_id, str):
        if author_id == "current":
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录才能查看自己的帖子",
                )
            actual_author_id = current_user.user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="author_id 只能是数字或 'current'",
            )
    elif author_id is not None:
        actual_author_id = author_id

    post_service = PostService(db)
    result = post_service.get_posts(
        page=page,
        page_size=page_size,
        sector_id=sector_id,
        author_id=actual_author_id,
        search=search,
    )

    return {
        "posts": [
            {
                "post_id": p.post_id,
                "title": p.title,
                "contract_code": p.contract_code,
                "strike_price": float(p.strike_price) if p.strike_price else None,
                "stop_loss": float(p.stop_loss),
                "take_profit": float(p.take_profit) if p.take_profit else None,
                "current_price": float(p.current_price) if p.current_price else None,
                "direction": p.direction or 'buy',
                "suggestion": p.suggestion,
                "author_id": p.author_id,
                "author_nickname": p.author.nickname if p.author else None,
                "collect_count": p.collect_count,
                "publish_time": p.publish_time.isoformat(),
            }
            for p in result["posts"]
        ],
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"],
    }


@router.get("/{post_id}")
async def get_post_detail(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取帖子详情。

    Args:
        post_id: 帖子ID。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 帖子详细信息。
    """
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在",
        )

    # 记录浏览历史
    browse_service = BrowseHistoryService(db)
    browse_service.record_browse(current_user.user_id, post_id)

    # 检查是否已收藏
    collection_service = CollectionService(db)
    is_collected = collection_service.is_collected(current_user.user_id, post_id)

    return {
        "post_id": post.post_id,
        "title": post.title,
        "contract_code": post.contract_code,
        "strike_price": float(post.strike_price) if post.strike_price else None,
        "stop_loss": float(post.stop_loss),
        "take_profit": float(post.take_profit) if post.take_profit else None,
        "current_price": float(post.current_price) if post.current_price else None,
        "direction": post.direction or 'buy',
        "suggestion": post.suggestion,
        "content": post.content,
        "k_line_image": post.k_line_image,
        "author_id": post.author_id,
        "author_nickname": post.author.nickname if post.author else None,
        "author_avatar": post.author.avatar_url if post.author else None,
        "collect_count": post.collect_count,
        "is_collected": is_collected,
        "publish_time": post.publish_time.isoformat(),
    }


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除帖子（软删除）。

    Args:
        post_id: 帖子ID。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 操作结果。
    """
    post_service = PostService(db)
    success = post_service.delete_post(post_id, current_user.user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权限删除",
        )

    return {"message": "删除成功"}


@router.put("/{post_id}")
async def update_post(
    post_id: int,
    request: PostUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新帖子。

    管理员（user_role >= 3）可编辑任意帖子；非管理员仅能编辑本人帖子。
    """
    if current_user.user_role < 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有管理员可以编辑帖子",
        )

    post_service = PostService(db)
    updated = post_service.update_post(
        post_id=post_id,
        user_id=current_user.user_id,
        title=request.title,
        contract_code=request.contract_code,
        stop_loss=request.stop_loss,
        take_profit=request.take_profit,
        strike_price=request.strike_price,
        current_price=request.current_price,
        direction=request.direction,
        suggestion=request.suggestion,
        content=request.content,
        k_line_image=request.k_line_image,
        sector_id=request.sector_id,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在或无权编辑",
        )

    return {
        "message": "更新成功",
        "post_id": updated.post_id,
        "title": updated.title,
        "contract_code": updated.contract_code,
        "stop_loss": float(updated.stop_loss),
        "take_profit": float(updated.take_profit) if updated.take_profit else None,
        "current_price": float(updated.current_price) if updated.current_price else None,
        "suggestion": updated.suggestion,
        "content": updated.content,
        "updated_at": updated.updated_at.isoformat() if updated.updated_at else None,
    }


@router.post("/{post_id}/collect")
async def collect_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """收藏帖子。

    Args:
        post_id: 帖子ID。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 操作结果。
    """
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在",
        )

    collection_service = CollectionService(db)
    collection = collection_service.add_collection(current_user.user_id, post_id)

    if collection:
        post_service.increment_collect_count(post_id)
        return {"message": "收藏成功", "collected": True}
    else:
        # 取消收藏
        if collection_service.remove_collection(current_user.user_id, post_id):
            post_service.decrement_collect_count(post_id)
            return {"message": "取消收藏成功", "collected": False}
        return {"message": "操作失败", "collected": False}


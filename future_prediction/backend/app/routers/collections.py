"""收藏路由模块。

处理收藏相关的API请求。
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.middleware.auth import get_current_user
from app.services.collection_service import CollectionService

router = APIRouter()


@router.get("")
async def get_user_collections(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取用户的收藏列表。

    Args:
        page: 页码。
        page_size: 每页数量。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 收藏的帖子列表。
    """
    collection_service = CollectionService(db)
    posts = collection_service.get_user_collections(
        user_id=current_user.user_id,
        page=page,
        page_size=page_size,
    )

    return {
        "posts": [
            {
                "post_id": p.post_id,
                "title": p.title,
                "contract_code": p.contract_code,
                "stop_loss": float(p.stop_loss),
                "current_price": float(p.current_price) if p.current_price else None,
                "suggestion": p.suggestion,
                "publish_time": p.publish_time.isoformat(),
            }
            for p in posts
        ]
    }


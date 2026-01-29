"""草稿路由模块。

处理草稿相关的API请求。
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.middleware.auth import get_current_user
from app.services.draft_service import DraftService

router = APIRouter()


class DraftCreateRequest(BaseModel):
    """创建草稿请求数据模型。"""

    title: Optional[str] = None
    contract_code: Optional[str] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    content: Optional[str] = None
    k_line_image: Optional[str] = None


class DraftUpdateRequest(BaseModel):
    """更新草稿请求数据模型。"""

    title: Optional[str] = None
    contract_code: Optional[str] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    content: Optional[str] = None
    k_line_image: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_draft(
    request: DraftCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """创建新草稿。

    Args:
        request: 创建草稿请求数据。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 创建的草稿信息。
    """
    draft_service = DraftService(db)
    draft = draft_service.create_draft(
        user_id=current_user.user_id,
        title=request.title,
        contract_code=request.contract_code,
        stop_loss=request.stop_loss,
        take_profit=request.take_profit,
        content=request.content,
        k_line_image=request.k_line_image,
    )

    return {
        "draft_id": draft.draft_id,
        "title": draft.title,
        "update_time": draft.update_time.isoformat(),
    }


@router.get("")
async def get_user_drafts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取当前用户的所有草稿。

    Args:
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 草稿列表。
    """
    draft_service = DraftService(db)
    drafts = draft_service.get_user_drafts(current_user.user_id)

    return {
        "drafts": [
            {
                "draft_id": d.draft_id,
                "title": d.title,
                "contract_code": d.contract_code,
                "update_time": d.update_time.isoformat(),
            }
            for d in drafts
        ]
    }


@router.get("/{draft_id}")
async def get_draft(
    draft_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取草稿详情。

    Args:
        draft_id: 草稿ID。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 草稿详细信息。
    """
    draft_service = DraftService(db)
    draft = draft_service.get_draft_by_id(draft_id, current_user.user_id)

    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="草稿不存在",
        )

    return {
        "draft_id": draft.draft_id,
        "title": draft.title,
        "contract_code": draft.contract_code,
        "stop_loss": float(draft.stop_loss) if draft.stop_loss else None,
        "take_profit": float(draft.take_profit) if draft.take_profit else None,
        "content": draft.content,
        "k_line_image": draft.k_line_image,
        "update_time": draft.update_time.isoformat(),
    }


@router.put("/{draft_id}")
async def update_draft(
    draft_id: int,
    request: DraftUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新草稿。

    Args:
        draft_id: 草稿ID。
        request: 更新草稿请求数据。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 更新后的草稿信息。
    """
    draft_service = DraftService(db)
    draft = draft_service.update_draft(
        draft_id=draft_id,
        user_id=current_user.user_id,
        title=request.title,
        contract_code=request.contract_code,
        stop_loss=request.stop_loss,
        take_profit=request.take_profit,
        content=request.content,
        k_line_image=request.k_line_image,
    )

    if not draft:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="草稿不存在",
        )

    return {
        "draft_id": draft.draft_id,
        "title": draft.title,
        "update_time": draft.update_time.isoformat(),
    }


@router.delete("/{draft_id}")
async def delete_draft(
    draft_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除草稿。

    Args:
        draft_id: 草稿ID。
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 操作结果。
    """
    draft_service = DraftService(db)
    success = draft_service.delete_draft(draft_id, current_user.user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="草稿不存在",
        )

    return {"message": "删除成功"}


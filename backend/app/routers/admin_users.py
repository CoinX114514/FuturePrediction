"""管理员用户管理路由。

仅超级管理员可用：分页查询、创建、更新、删除用户。
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.middleware.auth import get_current_user
from app.utils.password import hash_password

router = APIRouter(prefix="/admin/users", tags=["管理 - 用户"])


def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """确保当前用户为超级管理员。"""
    if current_user.user_role != 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限",
        )
    return current_user


class UserOut(BaseModel):
    user_id: int
    phone_number: str
    email: Optional[str]
    nickname: Optional[str]
    user_role: int
    is_active: bool
    daily_prediction_limit: Optional[int]
    created_at: Optional[str]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    phone_number: str
    password: str
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    user_role: int = 1
    is_active: bool = True
    daily_prediction_limit: Optional[int] = 5


class UserUpdate(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    password: Optional[str] = None
    user_role: Optional[int] = None
    is_active: Optional[bool] = None
    daily_prediction_limit: Optional[int] = None


def serialize_user(u: User):
    return {
        "user_id": u.user_id,
        "phone_number": u.phone_number,
        "email": u.email,
        "nickname": u.nickname,
        "user_role": u.user_role,
        "is_active": u.is_active,
        "daily_prediction_limit": u.daily_prediction_limit,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


@router.get("/", response_model=dict)
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    keyword: Optional[str] = Query(None, description="手机号/邮箱/昵称模糊搜索"),
    _: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if keyword:
        kw = f"%{keyword}%"
        query = query.filter(
            (User.phone_number.ilike(kw))
            | (User.email.ilike(kw))
            | (User.nickname.ilike(kw))
        )

    total = query.count()
    users = (
        query.order_by(User.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "users": [serialize_user(u) for u in users],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    # 唯一性校验
    if db.query(User).filter(User.phone_number == payload.phone_number).first():
        raise HTTPException(status_code=400, detail="手机号已存在")
    if payload.email and db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="邮箱已存在")

    new_user = User(
        phone_number=payload.phone_number,
        email=payload.email,
        nickname=payload.nickname or payload.phone_number,
        password_hash=hash_password(payload.password),
        user_role=payload.user_role,
        is_active=payload.is_active,
        daily_prediction_limit=payload.daily_prediction_limit,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return serialize_user(new_user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate = Body(default={}),
    admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 避免删除/禁用自己导致锁死
    if admin.user_id == user_id and payload.user_role is not None and payload.user_role != 3:
        raise HTTPException(status_code=400, detail="不能修改自身为非超级管理员")
    if admin.user_id == user_id and payload.is_active is False:
        raise HTTPException(status_code=400, detail="不能禁用自身账户")

    if payload and payload.phone_number and payload.phone_number != user.phone_number:
        if db.query(User).filter(User.phone_number == payload.phone_number).first():
            raise HTTPException(status_code=400, detail="手机号已存在")
        user.phone_number = payload.phone_number

    if payload and payload.email is not None and payload.email != user.email:
        if payload.email and db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(status_code=400, detail="邮箱已存在")
        user.email = payload.email

    if payload and payload.nickname is not None:
        user.nickname = payload.nickname

    if payload and payload.password:
        user.password_hash = hash_password(payload.password)

    if payload and payload.user_role is not None:
        user.user_role = payload.user_role

    if payload and payload.is_active is not None:
        user.is_active = payload.is_active

    if payload and payload.daily_prediction_limit is not None:
        user.daily_prediction_limit = payload.daily_prediction_limit

    db.commit()
    db.refresh(user)
    return serialize_user(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    admin: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if admin.user_id == user_id:
        raise HTTPException(status_code=400, detail="不能删除自身账户")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}


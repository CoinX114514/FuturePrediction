"""认证中间件。

提供认证相关的依赖注入和权限验证。
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import User
from app.utils.jwt import verify_token

# HTTP Bearer Token 安全方案
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """获取当前登录用户。

    这是一个依赖注入函数，用于需要认证的路由中。

    Args:
        credentials: HTTP Bearer Token 凭证。
        db: 数据库会话。

    Returns:
        User: 当前用户对象。

    Raises:
        HTTPException: 当 Token 无效或用户不存在时抛出 401 错误。
    """
    token = credentials.credentials

    # 验证 Token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的 Token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 获取用户 ID
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token 中缺少用户信息",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 从数据库获取用户
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查用户是否激活
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已被禁用",
        )

    return user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """获取当前用户（可选）。

    如果用户未登录，返回 None 而不是抛出异常。
    用于某些可选认证的路由。

    Args:
        credentials: HTTP Bearer Token 凭证（可选）。
        db: 数据库会话。

    Returns:
        Optional[User]: 用户对象，如果未登录则返回 None。
    """
    if not credentials:
        return None

    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None


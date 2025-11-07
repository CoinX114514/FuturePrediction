"""JWT Token 工具函数。

负责生成和验证 JWT Token。
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict

from jose import JWTError, jwt

# JWT 配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24"))


def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌。

    Args:
        data: 要编码到 Token 中的数据（通常是 user_id, user_role 等）。
        expires_delta: 过期时间增量。如果为 None，使用默认的 JWT_EXPIRE_HOURS。

    Returns:
        str: JWT Token 字符串。
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict]:
    """验证 JWT Token。

    Args:
        token: JWT Token 字符串。

    Returns:
        Optional[Dict]: 如果验证成功，返回解码后的数据；否则返回 None。
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """从 Token 中提取用户 ID。

    Args:
        token: JWT Token 字符串。

    Returns:
        Optional[int]: 用户 ID，如果 Token 无效则返回 None。
    """
    payload = verify_token(token)
    if payload:
        return payload.get("user_id")
    return None


def get_user_role_from_token(token: str) -> Optional[int]:
    """从 Token 中提取用户角色。

    Args:
        token: JWT Token 字符串。

    Returns:
        Optional[int]: 用户角色（1:普通用户 2:会员 3:超级管理员），如果 Token 无效则返回 None。
    """
    payload = verify_token(token)
    if payload:
        return payload.get("user_role")
    return None


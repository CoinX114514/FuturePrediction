"""权限管理工具函数。

提供权限验证装饰器和函数。
"""

from functools import wraps
from typing import List, Callable
from fastapi import HTTPException, status

from app.database.models import User


# 用户角色常量
class UserRole:
    """用户角色常量类。"""

    NORMAL = 1  # 普通用户
    MEMBER = 2  # 会员
    ADMIN = 3  # 超级管理员


def require_role(allowed_roles: List[int]):
    """权限验证装饰器。

    用于验证用户是否具有指定的角色权限。

    Args:
        allowed_roles: 允许的角色列表。

    Returns:
        装饰器函数。
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 从 kwargs 中获取 current_user
            user: User = kwargs.get("current_user")
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="需要登录",
                )

            if user.user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"需要以下角色之一: {allowed_roles}",
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_member(func: Callable):
    """要求会员权限的装饰器。

    Args:
        func: 被装饰的函数。

    Returns:
        装饰后的函数。
    """
    return require_role([UserRole.MEMBER, UserRole.ADMIN])(func)


def require_admin(func: Callable):
    """要求管理员权限的装饰器。

    Args:
        func: 被装饰的函数。

    Returns:
        装饰后的函数。
    """
    return require_role([UserRole.ADMIN])(func)


def check_prediction_permission(user: User) -> bool:
    """检查用户是否有预测权限。

    Args:
        user: 用户对象。

    Returns:
        bool: 如果有权限返回 True。
    """
    # 会员和管理员无限次
    if user.user_role >= UserRole.MEMBER:
        return True

    # 普通用户检查次数限制
    # TODO: 这里应该检查当天的预测次数
    return user.prediction_count < user.daily_prediction_limit


def check_csv_upload_permission(user: User) -> bool:
    """检查用户是否有 CSV 上传权限。

    Args:
        user: 用户对象。

    Returns:
        bool: 如果有权限返回 True。
    """
    # 只有会员和管理员可以上传 CSV
    return user.user_role >= UserRole.MEMBER


def check_sector_view_permission(user: User, sector_count: int) -> int:
    """检查用户可以查看的板块数量。

    Args:
        user: 用户对象。
        sector_count: 总板块数量。

    Returns:
        int: 用户可以查看的板块数量。
    """
    if user.user_role >= UserRole.MEMBER:
        return sector_count  # 会员和管理员可以查看全部

    # 普通用户只能查看 3 个
    return min(3, sector_count)


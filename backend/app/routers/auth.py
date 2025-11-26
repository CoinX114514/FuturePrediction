"""用户认证路由模块。

处理用户注册、登录、登出等认证相关请求。
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, validator
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.services.auth_service import AuthService
from app.middleware.auth import get_current_user, security
from app.database.models import User

router = APIRouter()


class RegisterRequest(BaseModel):
    """用户注册请求数据模型。

    Attributes:
        phone_number: 手机号码。
        password: 密码。
        email: 邮箱地址（可选）。
        nickname: 昵称（可选）。
    """

    phone_number: str
    password: str
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None

    @validator("phone_number")
    def validate_phone(cls, v):
        """验证手机号格式。

        Args:
            v: 手机号字符串。

        Returns:
            str: 验证后的手机号。

        Raises:
            ValueError: 当手机号格式不正确时抛出。
        """
        # 简单的手机号验证（11位数字）
        # 注意：验证逻辑已经在服务层实现，这里只做基本检查
        if not v or not isinstance(v, str):
            raise ValueError("手机号不能为空")
        if not v.isdigit() or len(v) != 11:
            raise ValueError("手机号必须是11位数字")
        return v

    @validator("password")
    def validate_password(cls, v):
        """验证密码强度。

        Args:
            v: 密码字符串。

        Returns:
            str: 验证后的密码。

        Raises:
            ValueError: 当密码不符合要求时抛出。
        """
        # 注意：详细的密码验证已经在服务层实现
        if not v or not isinstance(v, str):
            raise ValueError("密码不能为空")
        if len(v) < 6:
            raise ValueError("密码长度至少为6位")
        return v


class LoginRequest(BaseModel):
    """用户登录请求数据模型。

    Attributes:
        phone_number: 手机号码（与 email 二选一）。
        email: 邮箱地址（与 phone_number 二选一）。
        password: 密码。
    """

    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    @validator("password")
    def validate_has_credential(cls, v, values):
        """验证至少提供手机号或邮箱之一。

        Args:
            v: 密码值。
            values: 其他字段的值。

        Returns:
            str: 密码值。

        Raises:
            ValueError: 当手机号和邮箱都未提供时抛出。
        """
        # 在验证密码时检查是否至少有一个凭证
        phone = values.get("phone_number")
        email = values.get("email")
        if not phone and not email:
            raise ValueError("必须提供手机号或邮箱")
        return v


@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """用户注册接口。

    注册成功后自动创建会话并返回 Token，用户可以直接使用。

    Args:
        request: 注册请求数据。
        db: 数据库会话。

    Returns:
        JSONResponse: 包含用户信息和 Token 的响应。

    Raises:
        HTTPException: 当注册失败时抛出。
    """
    try:
        auth_service = AuthService(db)
        
        # 注册新用户（包含数据验证和事务处理）
        # register_user 现在直接返回 User 对象，避免额外的数据库查询
        user = auth_service.register_user(
            phone_number=request.phone_number,
            password=request.password,
            email=request.email,
            nickname=request.nickname,
        )

        # 创建会话（自动登录）
        try:
            session_data = auth_service.create_session(user)
        except Exception as e:
            # 如果创建会话失败，用户已创建但无法自动登录
            # 这种情况应该很少见，但需要记录
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="注册成功，但创建会话失败，请重新登录",
            )

        return JSONResponse(
            content={
                "message": "注册成功",
                "user": {
                    "user_id": user.user_id,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "nickname": user.nickname,
                    "user_role": user.user_role,
                },
                "token": session_data["token"],
                "token_type": session_data["token_type"],
                "expires_in": session_data["expires_in"],
            },
            status_code=status.HTTP_201_CREATED,
        )

    except HTTPException:
        # 重新抛出 HTTPException
        raise
    except ValueError as e:
        # 业务逻辑验证错误（如手机号已存在、格式错误等）
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        # 其他未预期的错误
        import traceback
        error_detail = f"注册失败: {str(e)}"
        # 在生产环境中，不应该暴露详细的错误信息
        # 这里可以根据环境变量决定是否显示详细信息
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_detail,
        )


@router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """用户登录接口。

    Args:
        request: 登录请求数据。
        db: 数据库会话。

    Returns:
        JSONResponse: 包含用户信息和 Token 的响应。

    Raises:
        HTTPException: 当登录失败时抛出。
    """
    # 验证至少提供手机号或邮箱
    if not request.phone_number and not request.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供手机号或邮箱",
        )

    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(
            phone_number=request.phone_number,
            email=request.email,
            password=request.password,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="手机号/邮箱或密码错误",
            )

        # 创建会话
        session_data = auth_service.create_session(user)

        return JSONResponse(
            content={
                "message": "登录成功",
                "user": {
                    "user_id": user.user_id,
                    "phone_number": user.phone_number,
                    "email": user.email,
                    "nickname": user.nickname,
                    "user_role": user.user_role,
                    "avatar_url": user.avatar_url,
                },
                "token": session_data["token"],
                "token_type": session_data["token_type"],
                "expires_in": session_data["expires_in"],
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"登录失败: {str(e)}",
        )


@router.post("/logout")
async def logout(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
):
    """用户登出接口。

    即使 Token 无效也能执行登出操作（用于清除无效 Token）。

    Args:
        credentials: HTTP Bearer Token 凭证（可选）。
        db: 数据库会话。

    Returns:
        JSONResponse: 登出成功响应。
    """
    try:
        auth_service = AuthService(db)
        
        # 如果有 Token，尝试使会话失效
        if credentials:
            token = credentials.credentials
            try:
                auth_service.invalidate_session(token)
            except Exception:
                # Token 无效或会话不存在，忽略错误继续执行
                pass

        return JSONResponse(
            content={"message": "登出成功"},
        )

    except Exception as e:
        # 即使出错也返回成功，确保前端能清除本地 Token
        return JSONResponse(
            content={"message": "登出成功"},
        )


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息。

    Args:
        current_user: 当前登录用户（通过依赖注入获取）。

    Returns:
        dict: 用户信息。
    """
    return {
        "user_id": current_user.user_id,
        "phone_number": current_user.phone_number,
        "email": current_user.email,
        "nickname": current_user.nickname,
        "user_role": current_user.user_role,
        "avatar_url": current_user.avatar_url,
        "prediction_count": current_user.prediction_count,
        "daily_prediction_limit": current_user.daily_prediction_limit,
        "member_expire_time": current_user.member_expire_time.isoformat() if current_user.member_expire_time else None,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }


@router.get("/prediction-limit")
async def get_prediction_limit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """获取用户的预测次数限制信息。

    Args:
        current_user: 当前登录用户。
        db: 数据库会话。

    Returns:
        dict: 预测限制信息。
    """
    auth_service = AuthService(db)
    limit_info = auth_service.check_prediction_limit(current_user.user_id)

    return {
        "allowed": limit_info["allowed"],
        "remaining": limit_info["remaining"],
        "limit": limit_info["limit"],
        "is_member": limit_info["is_member"],
        "current_count": current_user.prediction_count,
    }


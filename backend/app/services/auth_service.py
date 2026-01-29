"""用户认证服务。

负责用户注册、登录、会话管理等认证相关业务逻辑。
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict
import hashlib
import secrets
import re

from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.database.models import User, UserSession
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token


class AuthService:
    """用户认证服务类。

    提供用户注册、登录、Token 管理等功能。
    """

    def __init__(self, db: Session):
        """初始化认证服务。

        Args:
            db: 数据库会话。
        """
        self.db = db

    def register_user(
        self,
        phone_number: str,
        password: str,
        email: Optional[str] = None,
        nickname: Optional[str] = None,
    ) -> User:
        """注册新用户。

        使用数据库事务确保数据一致性，如果任何步骤失败都会回滚。

        Args:
            phone_number: 手机号码。
            password: 密码（明文）。
            email: 邮箱地址（可选）。
            nickname: 昵称（可选）。

        Returns:
            User: 创建的用户对象。

        Raises:
            ValueError: 当手机号或邮箱已存在、格式不正确、或密码不符合要求时抛出。
        """
        # 验证手机号格式
        if not phone_number or not phone_number.isdigit() or len(phone_number) != 11:
            raise ValueError("手机号必须是11位数字")

        # 验证密码强度
        if not password or len(password) < 6:
            raise ValueError("密码长度至少为6位")
        if len(password) > 128:
            raise ValueError("密码长度不能超过128位")

        # 验证邮箱格式（如果提供了邮箱）
        if email:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                raise ValueError("邮箱格式不正确")
            if len(email) > 100:
                raise ValueError("邮箱长度不能超过100个字符")

        # 验证昵称长度（如果提供了昵称）
        if nickname and len(nickname) > 50:
            raise ValueError("昵称长度不能超过50个字符")

        # 检查手机号是否已存在
        existing_user = self.db.query(User).filter(
            User.phone_number == phone_number
        ).first()
        if existing_user:
            raise ValueError("手机号已被注册")

        # 检查邮箱是否已存在（如果提供了邮箱）
        if email:
            existing_email = self.db.query(User).filter(User.email == email).first()
            if existing_email:
                raise ValueError("邮箱已被注册")

        # 使用事务创建新用户
        try:
            # 获取当前时间（UTC）
            now = datetime.now(timezone.utc)

            # 哈希密码
            password_hash = hash_password(password)

            # 创建新用户
            user = User(
                phone_number=phone_number,
                email=email,
                password_hash=password_hash,
                nickname=nickname or phone_number,
                user_role=1,  # 默认为普通用户
                daily_prediction_limit=5,  # 普通用户每日 5 次预测
                is_active=True,
                created_at=now,  # 显式设置创建时间
                updated_at=now,  # 显式设置更新时间
            )

            self.db.add(user)
            self.db.commit()  # 提交事务
            self.db.refresh(user)  # 刷新对象以获取数据库生成的字段（如 user_id）

            # 直接返回用户对象，避免在路由中再次查询数据库
            return user

        except IntegrityError as e:
            # 数据库完整性错误（如唯一约束违反）
            self.db.rollback()
            error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
            if 'phone_number' in error_msg.lower():
                raise ValueError("手机号已被注册")
            elif 'email' in error_msg.lower():
                raise ValueError("邮箱已被注册")
            else:
                raise ValueError("注册失败：数据冲突")
        except Exception as e:
            # 其他错误，回滚事务
            self.db.rollback()
            raise ValueError(f"注册失败：{str(e)}")

    def authenticate_user(
        self,
        phone_number: Optional[str] = None,
        email: Optional[str] = None,
        password: str = "",
    ) -> Optional[User]:
        """验证用户身份。

        Args:
            phone_number: 手机号码（与 email 二选一）。
            email: 邮箱地址（与 phone_number 二选一）。
            password: 密码（明文）。

        Returns:
            Optional[User]: 如果验证成功返回用户对象，否则返回 None。
        """
        if not phone_number and not email:
            return None

        # 根据手机号或邮箱查找用户
        if phone_number:
            user = self.db.query(User).filter(User.phone_number == phone_number).first()
        else:
            user = self.db.query(User).filter(User.email == email).first()

        if not user:
            return None

        # 验证密码
        if not verify_password(password, user.password_hash):
            return None

        # 检查用户是否激活
        if not user.is_active:
            return None

        # 更新最后登录时间
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

        return user

    def create_session(
        self,
        user: User,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Dict:
        """创建用户会话。

        Args:
            user: 用户对象。
            user_agent: 用户代理字符串。
            ip_address: IP 地址。

        Returns:
            dict: 包含 Token 和会话信息的字典。
        """
        # 生成 Token
        token_data = {
            "user_id": user.user_id,
            "user_role": user.user_role,
            "phone_number": user.phone_number,
        }
        token = create_access_token(token_data)

        # 计算 Token 哈希（用于存储）
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # 创建会话记录
        now = datetime.now(timezone.utc)
        session = UserSession(
            user_id=user.user_id,
            token_hash=token_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            expire_at=now + timedelta(hours=24),
        )

        self.db.add(session)
        self.db.commit()

        return {
            "token": token,
            "token_type": "bearer",
            "user_id": user.user_id,
            "user_role": user.user_role,
            "nickname": user.nickname,
            "expires_in": 24 * 3600,  # 秒
        }

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据用户 ID 获取用户。

        Args:
            user_id: 用户 ID。

        Returns:
            Optional[User]: 用户对象，如果不存在则返回 None。
        """
        return self.db.query(User).filter(User.user_id == user_id).first()

    def get_user_by_token(self, token: str) -> Optional[User]:
        """根据 Token 获取用户。

        Args:
            token: JWT Token。

        Returns:
            Optional[User]: 用户对象，如果 Token 无效则返回 None。
        """
        from app.utils.jwt import verify_token

        payload = verify_token(token)
        if not payload:
            return None

        user_id = payload.get("user_id")
        if not user_id:
            return None

        return self.get_user_by_id(user_id)

    def invalidate_session(self, token: str) -> bool:
        """使会话失效。

        Args:
            token: JWT Token。

        Returns:
            bool: 如果成功使会话失效返回 True。
        """
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        session = self.db.query(UserSession).filter(
            UserSession.token_hash == token_hash
        ).first()

        if session:
            self.db.delete(session)
            self.db.commit()
            return True

        return False

    def check_prediction_limit(self, user_id: int) -> Dict:
        """检查用户的预测次数限制。

        Args:
            user_id: 用户 ID。

        Returns:
            dict: 包含限制信息的字典。
                - allowed: 是否允许预测
                - remaining: 剩余次数
                - limit: 每日限制
                - is_member: 是否为会员
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return {
                "allowed": False,
                "remaining": 0,
                "limit": 0,
                "is_member": False,
            }

        # 检查是否为会员
        is_member = user.user_role >= 2
        if is_member:
            # 会员无限次
            return {
                "allowed": True,
                "remaining": -1,  # -1 表示无限
                "limit": -1,
                "is_member": True,
            }

        # 普通用户检查每日限制
        # TODO: 这里应该检查当天的预测次数，而不是总次数
        # 当前简化实现，使用 prediction_count
        remaining = max(0, user.daily_prediction_limit - user.prediction_count)

        return {
            "allowed": remaining > 0,
            "remaining": remaining,
            "limit": user.daily_prediction_limit,
            "is_member": False,
        }

    def increment_prediction_count(self, user_id: int) -> None:
        """增加用户的预测次数计数。

        Args:
            user_id: 用户 ID。
        """
        user = self.get_user_by_id(user_id)
        if user and user.user_role == 1:  # 只对普通用户计数
            user.prediction_count += 1
            self.db.commit()


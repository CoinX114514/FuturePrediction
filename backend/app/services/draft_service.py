"""草稿服务。

负责草稿的创建、查询、更新、删除等业务逻辑。
"""

from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.models import Draft


class DraftService:
    """草稿服务类。

    提供草稿的增删改查功能。
    """

    def __init__(self, db: Session):
        """初始化草稿服务。

        Args:
            db: 数据库会话。
        """
        self.db = db

    def create_draft(
        self,
        user_id: int,
        title: Optional[str] = None,
        contract_code: Optional[str] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        content: Optional[str] = None,
        k_line_image: Optional[str] = None,
    ) -> Draft:
        """创建新草稿。

        Args:
            user_id: 用户ID。
            title: 标题（可选）。
            contract_code: 合约代码（可选）。
            stop_loss: 止损价（可选）。
            take_profit: 止盈价（可选）。
            content: 内容正文（可选）。
            k_line_image: K线图URL（可选）。

        Returns:
            Draft: 创建的草稿对象。
        """
        draft = Draft(
            user_id=user_id,
            title=title,
            contract_code=contract_code,
            stop_loss=stop_loss,
            take_profit=take_profit,
            content=content,
            k_line_image=k_line_image,
        )

        self.db.add(draft)
        self.db.commit()
        self.db.refresh(draft)

        return draft

    def get_draft_by_id(self, draft_id: int, user_id: int) -> Optional[Draft]:
        """根据ID获取草稿（只能获取自己的草稿）。

        Args:
            draft_id: 草稿ID。
            user_id: 用户ID。

        Returns:
            Optional[Draft]: 草稿对象，如果不存在或不属于该用户则返回None。
        """
        return self.db.query(Draft).filter(
            Draft.draft_id == draft_id,
            Draft.user_id == user_id,
        ).first()

    def get_user_drafts(self, user_id: int) -> List[Draft]:
        """获取用户的所有草稿。

        Args:
            user_id: 用户ID。

        Returns:
            List[Draft]: 草稿列表，按更新时间倒序排列。
        """
        return (
            self.db.query(Draft)
            .filter(Draft.user_id == user_id)
            .order_by(desc(Draft.update_time))
            .all()
        )

    def update_draft(
        self,
        draft_id: int,
        user_id: int,
        title: Optional[str] = None,
        contract_code: Optional[str] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        content: Optional[str] = None,
        k_line_image: Optional[str] = None,
    ) -> Optional[Draft]:
        """更新草稿。

        Args:
            draft_id: 草稿ID。
            user_id: 用户ID。
            title: 标题（可选）。
            contract_code: 合约代码（可选）。
            stop_loss: 止损价（可选）。
            take_profit: 止盈价（可选）。
            content: 内容正文（可选）。
            k_line_image: K线图URL（可选）。

        Returns:
            Optional[Draft]: 更新后的草稿对象，如果不存在或不属于该用户则返回None。
        """
        draft = self.get_draft_by_id(draft_id, user_id)
        if not draft:
            return None

        if title is not None:
            draft.title = title
        if contract_code is not None:
            draft.contract_code = contract_code
        if stop_loss is not None:
            draft.stop_loss = stop_loss
        if take_profit is not None:
            draft.take_profit = take_profit
        if content is not None:
            draft.content = content
        if k_line_image is not None:
            draft.k_line_image = k_line_image

        draft.update_time = datetime.utcnow()
        self.db.commit()
        self.db.refresh(draft)

        return draft

    def delete_draft(self, draft_id: int, user_id: int) -> bool:
        """删除草稿。

        Args:
            draft_id: 草稿ID。
            user_id: 用户ID。

        Returns:
            bool: 如果成功删除返回True。
        """
        draft = self.get_draft_by_id(draft_id, user_id)
        if not draft:
            return False

        self.db.delete(draft)
        self.db.commit()
        return True


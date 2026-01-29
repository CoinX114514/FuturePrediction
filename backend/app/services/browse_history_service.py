"""浏览历史服务。

负责记录和查询用户浏览帖子的历史。
"""

from typing import List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.models import BrowseHistory, Post


class BrowseHistoryService:
    """浏览历史服务类。

    提供浏览历史的记录和查询功能。
    """

    def __init__(self, db: Session):
        """初始化浏览历史服务。

        Args:
            db: 数据库会话。
        """
        self.db = db

    def record_browse(self, user_id: int, post_id: int) -> BrowseHistory:
        """记录浏览历史。

        如果用户已浏览过该帖子，则更新浏览时间；否则创建新记录。

        Args:
            user_id: 用户ID。
            post_id: 帖子ID。

        Returns:
            BrowseHistory: 浏览历史对象。
        """
        # 检查是否已有记录
        history = (
            self.db.query(BrowseHistory)
            .filter(
                BrowseHistory.user_id == user_id,
                BrowseHistory.post_id == post_id,
            )
            .first()
        )

        if history:
            # 更新浏览时间
            history.browse_time = datetime.utcnow()
        else:
            # 创建新记录
            history = BrowseHistory(
                user_id=user_id,
                post_id=post_id,
            )
            self.db.add(history)

        self.db.commit()
        self.db.refresh(history)

        return history

    def get_user_browse_history(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> List[Post]:
        """获取用户的浏览历史。

        Args:
            user_id: 用户ID。
            page: 页码，从1开始。
            page_size: 每页数量。

        Returns:
            List[Post]: 浏览过的帖子列表，按浏览时间倒序排列。
        """
        histories = (
            self.db.query(BrowseHistory)
            .filter(BrowseHistory.user_id == user_id)
            .order_by(desc(BrowseHistory.browse_time))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        # 提取帖子ID列表
        post_ids = [h.post_id for h in histories]

        # 查询对应的帖子
        posts = (
            self.db.query(Post)
            .filter(Post.post_id.in_(post_ids), Post.status == 1)
            .all()
        )

        # 按浏览时间排序
        post_dict = {p.post_id: p for p in posts}
        return [post_dict[pid] for pid in post_ids if pid in post_dict]


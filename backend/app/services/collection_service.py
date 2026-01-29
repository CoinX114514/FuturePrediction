"""收藏服务。

负责用户收藏帖子的业务逻辑。
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.models import Collection, Post


class CollectionService:
    """收藏服务类。

    提供收藏的增删查功能。
    """

    def __init__(self, db: Session):
        """初始化收藏服务。

        Args:
            db: 数据库会话。
        """
        self.db = db

    def add_collection(self, user_id: int, post_id: int) -> Optional[Collection]:
        """添加收藏。

        Args:
            user_id: 用户ID。
            post_id: 帖子ID。

        Returns:
            Optional[Collection]: 收藏对象，如果已存在则返回None。
        """
        # 检查是否已收藏
        existing = self.db.query(Collection).filter(
            Collection.user_id == user_id,
            Collection.post_id == post_id,
        ).first()

        if existing:
            return None  # 已收藏，不重复添加

        collection = Collection(
            user_id=user_id,
            post_id=post_id,
        )

        self.db.add(collection)
        self.db.commit()
        self.db.refresh(collection)

        return collection

    def remove_collection(self, user_id: int, post_id: int) -> bool:
        """取消收藏。

        Args:
            user_id: 用户ID。
            post_id: 帖子ID。

        Returns:
            bool: 如果成功取消收藏返回True。
        """
        collection = self.db.query(Collection).filter(
            Collection.user_id == user_id,
            Collection.post_id == post_id,
        ).first()

        if not collection:
            return False

        self.db.delete(collection)
        self.db.commit()
        return True

    def is_collected(self, user_id: int, post_id: int) -> bool:
        """检查用户是否已收藏该帖子。

        Args:
            user_id: 用户ID。
            post_id: 帖子ID。

        Returns:
            bool: 如果已收藏返回True。
        """
        collection = self.db.query(Collection).filter(
            Collection.user_id == user_id,
            Collection.post_id == post_id,
        ).first()

        return collection is not None

    def get_user_collections(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> List[Post]:
        """获取用户的收藏列表。

        Args:
            user_id: 用户ID。
            page: 页码，从1开始。
            page_size: 每页数量。

        Returns:
            List[Post]: 收藏的帖子列表，按收藏时间倒序排列。
        """
        collections = (
            self.db.query(Collection)
            .filter(Collection.user_id == user_id)
            .order_by(desc(Collection.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        # 提取帖子ID列表
        post_ids = [c.post_id for c in collections]

        # 查询对应的帖子
        posts = (
            self.db.query(Post)
            .filter(Post.post_id.in_(post_ids), Post.status == 1)
            .all()
        )

        # 按收藏时间排序
        post_dict = {p.post_id: p for p in posts}
        return [post_dict[pid] for pid in post_ids if pid in post_dict]


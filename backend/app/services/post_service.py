"""帖子服务。

负责帖子的创建、查询、更新等业务逻辑。
"""

from typing import Optional, List, Dict
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_

from app.database.models import Post, User, Sector


class PostService:
    """帖子服务类。

    提供帖子的增删改查功能。
    """

    def __init__(self, db: Session):
        """初始化帖子服务。

        Args:
            db: 数据库会话。
        """
        self.db = db

    def create_post(
        self,
        author_id: int,
        title: str,
        contract_code: str,
        stop_loss: float,
        content: str,
        take_profit: Optional[float] = None,
        strike_price: Optional[float] = None,
        current_price: Optional[float] = None,
        suggestion: Optional[str] = None,
        k_line_image: Optional[str] = None,
        sector_id: Optional[int] = None,
    ) -> Post:
        """创建新帖子。

        Args:
            author_id: 作者用户ID。
            title: 标题。
            contract_code: 合约代码。
            stop_loss: 止损价。
            content: 内容正文。
            take_profit: 止盈价（可选）。
            strike_price: 行权价（可选）。
            current_price: 现价（可选）。
            suggestion: 简要建议（可选）。
            k_line_image: K线图URL（可选）。
            sector_id: 板块ID（可选）。

        Returns:
            Post: 创建的帖子对象。
        """
        post = Post(
            author_id=author_id,
            title=title,
            contract_code=contract_code,
            stop_loss=stop_loss,
            content=content,
            take_profit=take_profit,
            strike_price=strike_price,
            current_price=current_price,
            suggestion=suggestion,
            k_line_image=k_line_image,
            sector_id=sector_id,
            status=1,  # 已发布
            publish_time=datetime.now(timezone.utc),
        )

        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)

        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        """根据ID获取帖子。

        Args:
            post_id: 帖子ID。

        Returns:
            Optional[Post]: 帖子对象，如果不存在则返回None。
        """
        return self.db.query(Post).filter(
            and_(Post.post_id == post_id, Post.status == 1)
        ).first()

    def get_posts(
        self,
        page: int = 1,
        page_size: int = 20,
        sector_id: Optional[int] = None,
        author_id: Optional[int] = None,
    ) -> Dict:
        """获取帖子列表。

        Args:
            page: 页码，从1开始。
            page_size: 每页数量。
            sector_id: 板块ID筛选（可选）。
            author_id: 作者ID筛选（可选）。

        Returns:
            dict: 包含帖子列表和分页信息的字典。
        """
        query = self.db.query(Post).filter(Post.status == 1)

        if sector_id:
            query = query.filter(Post.sector_id == sector_id)
        if author_id:
            query = query.filter(Post.author_id == author_id)

        # 按发布时间倒序排列
        query = query.order_by(desc(Post.publish_time))

        # 分页
        total = query.count()
        posts = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            "posts": posts,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }

    def increment_collect_count(self, post_id: int) -> None:
        """增加帖子收藏数。

        Args:
            post_id: 帖子ID。
        """
        post = self.db.query(Post).filter(Post.post_id == post_id).first()
        if post:
            post.collect_count += 1
            self.db.commit()

    def decrement_collect_count(self, post_id: int) -> None:
        """减少帖子收藏数。

        Args:
            post_id: 帖子ID。
        """
        post = self.db.query(Post).filter(Post.post_id == post_id).first()
        if post and post.collect_count > 0:
            post.collect_count -= 1
            self.db.commit()

    def delete_post(self, post_id: int, user_id: int) -> bool:
        """删除帖子（软删除）。

        Args:
            post_id: 帖子ID。
            user_id: 用户ID（用于权限检查）。

        Returns:
            bool: 如果成功删除返回True。
        """
        post = self.db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            return False

        # 只有作者或管理员可以删除
        if post.author_id != user_id:
            # 检查是否为管理员（role >= 3）
            user = self.db.query(User).filter(User.user_id == user_id).first()
            if not user or user.user_role < 3:
                return False

        post.status = 0  # 软删除
        self.db.commit()
        return True

    def update_post(
        self,
        post_id: int,
        user_id: int,
        title: Optional[str] = None,
        contract_code: Optional[str] = None,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        strike_price: Optional[float] = None,
        current_price: Optional[float] = None,
        suggestion: Optional[str] = None,
        content: Optional[str] = None,
        k_line_image: Optional[str] = None,
        sector_id: Optional[int] = None,
    ) -> Optional[Post]:
        """更新帖子。

        仅允许作者本人（且具备管理员/超级管理员权限）修改自己的帖子。

        Args:
            post_id: 帖子ID。
            user_id: 当前用户ID。
            ... 其余字段同创建。

        Returns:
            Optional[Post]: 更新后的帖子对象。
        """
        post = self.db.query(Post).filter(Post.post_id == post_id, Post.status == 1).first()
        if not post:
            return None

        # 权限：必须是作者本人且具备管理员权限
        if post.author_id != user_id:
            return None

        author = self.db.query(User).filter(User.user_id == user_id).first()
        if not author or author.user_role < 3:
            return None

        if title is not None:
            post.title = title
        if contract_code is not None:
            post.contract_code = contract_code
        if stop_loss is not None:
            post.stop_loss = stop_loss
        if take_profit is not None:
            post.take_profit = take_profit
        if strike_price is not None:
            post.strike_price = strike_price
        if current_price is not None:
            post.current_price = current_price
        if suggestion is not None:
            post.suggestion = suggestion
        if content is not None:
            post.content = content
        if k_line_image is not None:
            post.k_line_image = k_line_image
        if sector_id is not None:
            post.sector_id = sector_id

        post.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(post)
        return post


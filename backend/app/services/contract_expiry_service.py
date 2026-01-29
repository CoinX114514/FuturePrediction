"""期货合约到期汰换服务。

负责检查已到期的期货合约，并自动软删除对应的帖子。
"""

import logging
from typing import Dict
from datetime import datetime, timezone, date
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models import Post
from app.services.futures_sync_service import FuturesSyncService

logger = logging.getLogger(__name__)


class ContractExpiryService:
    """期货合约到期汰换服务类。

    负责检查已到期的期货合约，并自动软删除对应的帖子。
    """

    def __init__(self, db: Session):
        """初始化合约到期汰换服务。

        Args:
            db: 数据库会话。
        """
        self.db = db
        self.futures_sync_service = FuturesSyncService(db)

    def cleanup_expired_contracts(self) -> Dict[str, int]:
        """清理已到期的期货合约帖子。

        检查所有活跃的帖子，如果对应的合约已到期，则软删除（status=0）该帖子。

        Returns:
            dict: 包含清理统计信息的字典。
        """
        result = {
            'total_checked': 0,
            'expired_count': 0,
            'deleted_count': 0,
            'error_count': 0,
        }

        try:
            # 获取所有活跃的帖子（status=1）
            active_posts = self.db.query(Post).filter(
                and_(
                    Post.status == 1,
                    Post.contract_code.isnot(None)
                )
            ).all()

            result['total_checked'] = len(active_posts)
            logger.info(f"开始检查 {result['total_checked']} 个活跃帖子的合约到期情况...")

            for post in active_posts:
                try:
                    contract_code = post.contract_code
                    if not contract_code:
                        continue

                    # 检查合约是否已到期
                    is_active, expiry_date = self.futures_sync_service.is_contract_active(contract_code)

                    if not is_active:
                        result['expired_count'] += 1
                        logger.info(
                            f"发现已到期合约: {contract_code} "
                            f"(到期日期: {expiry_date}, 帖子ID: {post.post_id})"
                        )

                        # 软删除帖子
                        post.status = 0
                        result['deleted_count'] += 1
                        logger.debug(f"已软删除帖子: post_id={post.post_id}, contract_code={contract_code}")

                except Exception as e:
                    result['error_count'] += 1
                    logger.error(
                        f"处理帖子 {post.post_id} (合约代码: {post.contract_code}) 时出错: {str(e)}",
                        exc_info=True
                    )
                    continue

            # 提交所有更改
            if result['deleted_count'] > 0:
                self.db.commit()
                logger.info(f"已提交 {result['deleted_count']} 个帖子的软删除操作")

            logger.info(
                f"合约到期清理完成: "
                f"检查总数={result['total_checked']}, "
                f"到期数量={result['expired_count']}, "
                f"删除数量={result['deleted_count']}, "
                f"错误数量={result['error_count']}"
            )

        except Exception as e:
            logger.error(f"清理到期合约时发生错误: {str(e)}", exc_info=True)
            result['error'] = str(e)
            # 发生错误时回滚
            self.db.rollback()

        return result


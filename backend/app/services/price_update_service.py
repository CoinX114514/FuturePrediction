"""价格更新服务。

负责从 Tushare 获取期货实时价格并更新到数据库。
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
import pandas as pd
import numpy as np

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models import Post, FuturesContract
from app.services.tushare_service import TushareService

# 配置日志
logger = logging.getLogger(__name__)


class PriceUpdateService:
    """价格更新服务类。

    提供从 Tushare 获取期货实时价格并更新到数据库的功能。
    """

    def __init__(self, db: Session):
        """初始化价格更新服务。

        Args:
            db: 数据库会话。
        """
        self.db = db
        self.tushare_service = TushareService()

    def get_futures_spot_price(self, contract_code: str) -> Optional[float]:
        """从 Tushare 获取指定合约的实时价格。

        Args:
            contract_code: 合约代码，如 "CU2601" 或 "CU2601.SHF"。

        Returns:
            Optional[float]: 实时价格，如果获取失败则返回 None。
        """
        logger.info(f"正在从 Tushare 获取期货实时行情，合约代码: {contract_code}")
        
        try:
            price = self.tushare_service.get_futures_price(contract_code)
            if price is not None:
                logger.info(f"✓ 成功获取价格: 合约代码={contract_code}, 价格={price}")
            else:
                logger.warning(f"❌ 无法获取价格，合约代码: {contract_code}")
            return price
        except Exception as e:
            logger.error(f"获取期货价格时发生错误，contract_code: {contract_code}, 错误: {e}")
            return None

    def update_post_price(self, post_id: int) -> bool:
        """更新单个帖子的现价。

        Args:
            post_id: 帖子ID。

        Returns:
            bool: 如果成功更新返回 True，否则返回 False。
        """
        try:
            # 获取帖子
            post = self.db.query(Post).filter(
                and_(Post.post_id == post_id, Post.status == 1)
            ).first()

            if not post:
                logger.warning(f"帖子不存在或已删除，post_id: {post_id}")
                return False

            if not post.contract_code:
                logger.warning(f"帖子没有合约代码，post_id: {post_id}")
                return False

            # 获取实时价格
            current_price = self.get_futures_spot_price(post.contract_code)

            if current_price is None:
                logger.warning(f"无法获取价格，post_id: {post_id}, contract_code: {post.contract_code}")
                return False

            # 更新价格
            post.current_price = current_price
            post.updated_at = datetime.utcnow()
            self.db.commit()

            logger.info(f"成功更新帖子价格，post_id: {post_id}, contract_code: {post.contract_code}, price: {current_price}")
            return True

        except Exception as e:
            logger.error(f"更新帖子价格时发生错误，post_id: {post_id}, 错误: {str(e)}", exc_info=True)
            self.db.rollback()
            return False

    def _batch_get_prices(self, contract_codes: List[str]) -> Dict[str, Optional[float]]:
        """批量获取多个合约的价格。

        优化版本：一次性获取所有价格，避免重复调用 Tushare 接口。

        Args:
            contract_codes: 合约代码列表，如 ["CU2601", "IF2603"]。

        Returns:
            dict: 合约代码到价格的映射，格式为 {contract_code: price}。
        """
        # 去重
        unique_codes = list(set(contract_codes))
        logger.info(f"批量获取价格，合约数量: {len(unique_codes)}")
        
        try:
            price_map = self.tushare_service.batch_get_futures_prices(unique_codes)
            logger.info(f"批量获取完成，成功获取 {len(price_map)}/{len(unique_codes)} 个合约的价格")
            return price_map
        except Exception as e:
            logger.error(f"批量获取价格失败: {e}")
            return {}

    def update_all_posts_price(self) -> Dict[str, int]:
        """批量更新所有已发布帖子的现价。

        优化版本：先批量获取所有价格，然后批量更新数据库，提高效率。

        Returns:
            dict: 包含更新统计信息的字典，格式为：
                {
                    "total": 总帖子数,
                    "success": 成功更新数,
                    "failed": 失败数
                }
        """
        try:
            # 获取所有已发布的帖子
            posts = self.db.query(Post).filter(Post.status == 1).all()

            total = len(posts)
            if total == 0:
                logger.info("没有需要更新价格的帖子")
                return {
                    "total": 0,
                    "success": 0,
                    "failed": 0,
                }

            logger.info(f"开始批量更新价格，总帖子数: {total}")

            # 收集所有需要更新的合约代码
            contract_codes = []
            post_contract_map = {}  # {contract_code: [post1, post2, ...]}
            
            for post in posts:
                if not post.contract_code:
                    continue
                
                contract_code = post.contract_code
                contract_codes.append(contract_code)
                
                if contract_code not in post_contract_map:
                    post_contract_map[contract_code] = []
                post_contract_map[contract_code].append(post)

            # 批量获取所有价格
            price_map = self._batch_get_prices(contract_codes)
            
            # 批量更新数据库
            success_count = 0
            failed_count = 0
            updated_at = datetime.utcnow()
            
            for contract_code, posts_list in post_contract_map.items():
                if contract_code in price_map and price_map[contract_code] is not None:
                    price = price_map[contract_code]
                    # 更新所有使用该合约的帖子
                    for post in posts_list:
                        try:
                            post.current_price = price
                            post.updated_at = updated_at
                            success_count += 1
                        except Exception as e:
                            logger.error(f"更新帖子价格失败，post_id: {post.post_id}, 错误: {str(e)}")
                            failed_count += 1
                else:
                    logger.warning(f"无法获取合约价格，contract_code: {contract_code}, 影响 {len(posts_list)} 个帖子")
                    failed_count += len(posts_list)

            # 提交所有更改
            self.db.commit()

            logger.info(f"批量更新完成，总数: {total}, 成功: {success_count}, 失败: {failed_count}")

            return {
                "total": total,
                "success": success_count,
                "failed": failed_count,
            }

        except Exception as e:
            logger.error(f"批量更新价格时发生错误: {str(e)}", exc_info=True)
            self.db.rollback()
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "error": str(e),
            }

    def update_posts_by_contract_code(self, contract_code: str) -> Dict[str, int]:
        """更新指定合约代码的所有帖子的现价。

        Args:
            contract_code: 合约代码，如 "IF2312"。

        Returns:
            dict: 包含更新统计信息的字典。
        """
        try:
            # 获取指定合约代码的所有已发布帖子
            posts = self.db.query(Post).filter(
                and_(
                    Post.contract_code == contract_code,
                    Post.status == 1
                )
            ).all()

            total = len(posts)
            success_count = 0
            failed_count = 0

            logger.info(f"开始更新指定合约的价格，contract_code: {contract_code}, 帖子数: {total}")

            # 先获取一次价格（避免重复请求）
            current_price = self.get_futures_spot_price(contract_code)

            if current_price is None:
                logger.warning(f"无法获取合约价格，contract_code: {contract_code}")
                return {
                    "total": total,
                    "success": 0,
                    "failed": total,
                }

            # 批量更新所有相关帖子
            for post in posts:
                try:
                    post.current_price = current_price
                    post.updated_at = datetime.utcnow()
                    success_count += 1
                except Exception as e:
                    logger.error(f"更新帖子价格失败，post_id: {post.post_id}, 错误: {str(e)}")
                    failed_count += 1

            self.db.commit()

            logger.info(f"更新指定合约价格完成，contract_code: {contract_code}, 总数: {total}, 成功: {success_count}, 失败: {failed_count}")

            return {
                "total": total,
                "success": success_count,
                "failed": failed_count,
            }

        except Exception as e:
            logger.error(f"更新指定合约价格时发生错误，contract_code: {contract_code}, 错误: {str(e)}", exc_info=True)
            self.db.rollback()
            return {
                "total": 0,
                "success": 0,
                "failed": 0,
                "error": str(e),
            }


"""规范化帖子命名并清理数据库。

将帖子标题统一为三段式：「交易所」「品类」「代码」；
可选：contract_code 统一大写、删除同一合约的重复帖子。
"""

import os
import sys
import logging
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.database.models import Post, FuturesContract
from app.utils.futures_naming import format_post_title, extract_symbol, get_exchange_name
from sqlalchemy import and_

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True,
)
logger = logging.getLogger(__name__)


def build_contract_exchange_map(db) -> dict:
    """从 futures_contracts 表构建 contract_code -> exchange_code 映射。"""
    mapping = {}
    for row in db.query(FuturesContract.contract_code, FuturesContract.exchange_code).all():
        if row.contract_code:
            mapping[row.contract_code.upper().strip()] = row.exchange_code
    return mapping


def normalize_posts(dry_run: bool = True, remove_duplicates: bool = True) -> dict:
    """
    规范化所有帖子标题为「交易所」「品类」「代码」，并可选清理重复。
    
    Args:
        dry_run: True 只打印将执行的变更，不写库；False 执行更新。
        remove_duplicates: 是否删除同一 contract_code 的重复帖子（保留 publish_time 最早的一条）。
    
    Returns:
        统计信息。
    """
    db = SessionLocal()
    stats = {
        'total': 0,
        'title_updated': 0,
        'contract_code_normalized': 0,
        'duplicates_removed': 0,
        'errors': 0,
    }
    
    try:
        # 只处理已发布的帖子
        posts = db.query(Post).filter(Post.status == 1).all()
        stats['total'] = len(posts)
        
        if not posts:
            logger.info("没有已发布的帖子需要处理")
            return stats
        
        contract_to_exchange = build_contract_exchange_map(db)
        logger.info(f"已加载 {len(contract_to_exchange)} 个合约的交易所映射")
        
        # 1. 删除重复：同一 contract_code 保留一条（保留最早发布的）
        if remove_duplicates:
            by_contract = defaultdict(list)
            for p in posts:
                code = (p.contract_code or '').strip().upper()
                if code:
                    by_contract[code].append(p)
            
            for code, group in by_contract.items():
                if len(group) <= 1:
                    continue
                # 按 publish_time 排序，保留最早的一条，其余软删除
                group.sort(key=lambda x: (x.publish_time or x.created_at or x.post_id))
                to_remove = group[1:]
                for p in to_remove:
                    if not dry_run:
                        p.status = 0
                    stats['duplicates_removed'] += 1
                    logger.info(f"  重复删除: contract_code={code}, post_id={p.post_id}, title={p.title}")
            
            if not dry_run and stats['duplicates_removed']:
                db.commit()
                # 重新查询，排除已软删除的
                posts = db.query(Post).filter(Post.status == 1).all()
        
        # 2. 更新标题与 contract_code 规范化
        for post in posts:
            try:
                code = (post.contract_code or '').strip().upper()
                if not code:
                    continue
                
                exchange_code = contract_to_exchange.get(code)
                new_title = format_post_title(code, exchange_code)
                
                changed = False
                if (post.title or '').strip() != new_title:
                    if not dry_run:
                        post.title = new_title
                    stats['title_updated'] += 1
                    changed = True
                    logger.debug(f"标题: {post.title} -> {new_title}")
                
                if (post.contract_code or '').strip() != code:
                    if not dry_run:
                        post.contract_code = code
                    stats['contract_code_normalized'] += 1
                    changed = True
                
                if changed and not dry_run:
                    db.add(post)
            except Exception as e:
                stats['errors'] += 1
                logger.exception(f"处理 post_id={post.post_id} 失败: {e}")
        
        if not dry_run and (stats['title_updated'] or stats['contract_code_normalized']):
            db.commit()
        
        return stats
    except Exception as e:
        logger.exception(f"执行失败: {e}")
        db.rollback()
        stats['errors'] += 1
        return stats
    finally:
        db.close()


def main():
    import argparse
    parser = argparse.ArgumentParser(description='规范化帖子命名并清理数据库')
    parser.add_argument('--execute', action='store_true', help='真正写库；默认仅预览')
    parser.add_argument('--no-dedup', action='store_true', help='不删除重复帖子')
    args = parser.parse_args()
    
    dry_run = not args.execute
    remove_duplicates = not args.no_dedup
    
    if dry_run:
        logger.info("===== 预览模式（不写库），使用 --execute 执行写库 =====")
    
    stats = normalize_posts(dry_run=dry_run, remove_duplicates=remove_duplicates)
    
    logger.info("===== 统计 =====")
    logger.info(f"  帖子总数: {stats['total']}")
    logger.info(f"  标题将更新/已更新: {stats['title_updated']}")
    logger.info(f"  合约代码规范化: {stats['contract_code_normalized']}")
    logger.info(f"  重复帖子将删除/已删除: {stats['duplicates_removed']}")
    logger.info(f"  错误: {stats['errors']}")


if __name__ == '__main__':
    main()

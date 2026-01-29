"""将 Tushare 期货合约同步到数据库的脚本。

此脚本会：
1. 从 Tushare 获取所有正在交易中的期货合约
2. 将合约信息添加到 futures_contracts 表
3. 为每个合约创建对应的帖子（如果不存在）
"""

import os
import sys
import logging
from datetime import datetime, date, timezone
from typing import List, Dict, Optional
import pandas as pd

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal, engine
from app.database.models import Base, FuturesContract, Post, User
from app.services.tushare_service import TushareService
from app.services.post_service import PostService
from app.utils.futures_naming import format_post_title
from sqlalchemy.orm import Session
from sqlalchemy import and_

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True  # 强制重新配置日志
)
logger = logging.getLogger(__name__)


def convert_ts_code_to_contract_code(ts_code: str) -> str:
    """将 Tushare 合约代码转换为标准合约代码。
    
    例如：CU2601.SHF -> CU2601
    
    Args:
        ts_code: Tushare 合约代码。
    
    Returns:
        str: 标准合约代码。
    """
    if '.' in ts_code:
        return ts_code.split('.')[0]
    return ts_code


def get_exchange_code(exchange: str) -> str:
    """将 Tushare 交易所代码转换为标准交易所代码。
    
    Args:
        exchange: Tushare 交易所代码。
    
    Returns:
        str: 标准交易所代码。
    """
    exchange_map = {
        'SHFE': 'SHFE',
        'DCE': 'DCE',
        'CZCE': 'CZCE',
        'CFFEX': 'CFFEX',
        'INE': 'INE',
        'GFEX': 'GFEX',
    }
    return exchange_map.get(exchange, exchange)


def sync_futures_to_database(db: Session, tushare_service: TushareService, author_id: int) -> Dict[str, int]:
    """将 Tushare 期货合约同步到数据库。
    
    Args:
        db: 数据库会话。
        tushare_service: Tushare 服务实例。
        author_id: 作者用户ID（用于创建帖子）。
    
    Returns:
        Dict: 同步结果统计。
    """
    result = {
        'contracts_total': 0,
        'contracts_created': 0,
        'contracts_updated': 0,
        'posts_created': 0,
        'posts_updated': 0,
        'errors': 0,
    }
    
    try:
        # 1. 获取所有期货合约基本信息
        logger.info("正在从 Tushare 获取期货合约基本信息...")
        basic_df = tushare_service.get_futures_basic_info()
        
        if basic_df is None or basic_df.empty:
            logger.error("未能获取期货合约基本信息")
            return result
        
        logger.info(f"成功获取 {len(basic_df)} 条期货合约基本信息")
        
        # 2. 获取最新日线行情数据（用于过滤活跃合约）
        logger.info("正在获取最新日线行情数据...")
        daily_df = tushare_service.get_futures_daily()
        
        # 3. 过滤出正在交易中的合约
        today = date.today()
        
        # 转换日期列
        if 'list_date' in basic_df.columns:
            basic_df['list_date'] = pd.to_datetime(basic_df['list_date'], format='%Y%m%d', errors='coerce')
        if 'delist_date' in basic_df.columns:
            basic_df['delist_date'] = pd.to_datetime(basic_df['delist_date'], format='%Y%m%d', errors='coerce')
        
        # 过滤条件：已上市且未退市
        active_mask = True
        if 'list_date' in basic_df.columns:
            active_mask = active_mask & (basic_df['list_date'].notna()) & (basic_df['list_date'] <= pd.Timestamp(today))
        if 'delist_date' in basic_df.columns:
            active_mask = active_mask & (
                basic_df['delist_date'].isna() | (basic_df['delist_date'] >= pd.Timestamp(today))
            )
        
        active_contracts = basic_df[active_mask].copy()
        
        # 不再用日线数据过滤，避免因 Tushare fut_daily 返回条数限制漏掉合约（如 I2603 铁矿石）
        # 仅按上市/退市日期判定活跃合约，日线数据仅用于填充 current_price
        logger.info(f"过滤后得到 {len(active_contracts)} 个正在交易中的期货合约（按上市/退市日期）")
        result['contracts_total'] = len(active_contracts)
        
        # 4. 获取现有合约和帖子
        existing_contracts = {
            contract.contract_code: contract
            for contract in db.query(FuturesContract).all()
        }
        
        existing_posts = {
            post.contract_code.upper(): post
            for post in db.query(Post).filter(
                and_(Post.status == 1, Post.contract_code.isnot(None))
            ).all()
        }
        
        post_service = PostService(db)
        
        # 5. 同步合约到数据库
        for _, row in active_contracts.iterrows():
            try:
                ts_code = str(row.get('ts_code', ''))
                contract_code = convert_ts_code_to_contract_code(ts_code).upper()
                exchange = get_exchange_code(str(row.get('exchange', '')))
                contract_name = str(row.get('name', contract_code))
                
                # 处理日期
                list_date = None
                if pd.notna(row.get('list_date')):
                    list_date = row['list_date'].date() if isinstance(row['list_date'], pd.Timestamp) else None
                
                expiry_date = None
                if pd.notna(row.get('delist_date')):
                    expiry_date = row['delist_date'].date() if isinstance(row['delist_date'], pd.Timestamp) else None
                
                # 处理数值字段
                multiplier = None
                if pd.notna(row.get('multiplier')):
                    try:
                        multiplier = float(row['multiplier'])
                    except (ValueError, TypeError):
                        pass
                
                # 获取价格（从日线行情）
                current_price = None
                if daily_df is not None and not daily_df.empty:
                    matched = daily_df[daily_df['ts_code'] == ts_code]
                    if not matched.empty:
                        if 'close' in matched.columns:
                            close_price = matched.iloc[0]['close']
                            if pd.notna(close_price) and close_price != 0:
                                current_price = float(close_price)
                
                # 检查合约是否已存在
                if contract_code in existing_contracts:
                    # 更新现有合约
                    contract = existing_contracts[contract_code]
                    contract.contract_name = contract_name
                    contract.exchange_code = exchange
                    contract.listed_date = list_date
                    contract.expiry_date = expiry_date
                    contract.is_active = True
                    if multiplier is not None:
                        contract.contract_multiplier = multiplier
                    result['contracts_updated'] += 1
                else:
                    # 创建新合约
                    contract = FuturesContract(
                        contract_code=contract_code,
                        contract_name=contract_name,
                        exchange_code=exchange,
                        listed_date=list_date,
                        expiry_date=expiry_date,
                        contract_multiplier=multiplier,
                        is_active=True,
                    )
                    db.add(contract)
                    db.flush()  # 获取 contract_id
                    existing_contracts[contract_code] = contract
                    result['contracts_created'] += 1
                
                # 统一使用三段式标题：「交易所」「品类」「代码」
                post_title = format_post_title(contract_code, exchange)
                
                # 检查帖子是否已存在
                if contract_code.upper() in existing_posts:
                    # 更新现有帖子
                    post = existing_posts[contract_code.upper()]
                    post.title = post_title
                    if current_price is not None:
                        post.current_price = current_price
                    post.updated_at = datetime.now(timezone.utc)
                    result['posts_updated'] += 1
                else:
                    # 创建新帖子
                    stop_loss = current_price * 0.95 if current_price is not None else 0.0
                    
                    content = f"期货合约 {contract_code} 的交易建议。\n\n"
                    content += f"品种代码: {row.get('symbol', '')}\n"
                    if current_price is not None:
                        content += f"当前价格: {current_price}\n"
                    content += "\n请管理员编辑此帖子的交易建议、止损价、止盈价等信息。"
                    
                    post = post_service.create_post(
                        author_id=author_id,
                        title=post_title,
                        contract_code=contract_code,
                        stop_loss=stop_loss,
                        content=content,
                        current_price=current_price,
                        direction='buy',
                        suggestion="待管理员编辑建议",
                    )
                    existing_posts[contract_code.upper()] = post
                    result['posts_created'] += 1
                
            except Exception as e:
                logger.error(f"处理合约时出错: {e}, ts_code: {row.get('ts_code', '')}", exc_info=True)
                result['errors'] += 1
                continue
        
        # 提交所有更改
        db.commit()
        
        logger.info(
            f"同步完成: "
            f"合约总数={result['contracts_total']}, "
            f"合约创建={result['contracts_created']}, "
            f"合约更新={result['contracts_updated']}, "
            f"帖子创建={result['posts_created']}, "
            f"帖子更新={result['posts_updated']}, "
            f"错误={result['errors']}"
        )
        
        return result
        
    except Exception as e:
        logger.error(f"同步期货合约到数据库失败: {e}", exc_info=True)
        db.rollback()
        result['errors'] += 1
        return result


def main():
    """主函数。"""
    logger.info("=" * 80)
    logger.info("开始将 Tushare 期货合约同步到数据库")
    logger.info("=" * 80)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 初始化 Tushare 服务
        tushare_service = TushareService()
        
        # 获取系统管理员用户（user_role >= 3）
        admin_user = db.query(User).filter(User.user_role >= 3).first()
        if not admin_user:
            logger.error("未找到系统管理员用户（user_role >= 3），请先创建管理员用户")
            logger.info("提示：可以使用 create_dev_user.py 创建管理员用户")
            return
        
        logger.info(f"使用管理员用户: user_id={admin_user.user_id}, nickname={admin_user.nickname}, role={admin_user.user_role}")
        
        # 同步期货合约到数据库
        result = sync_futures_to_database(db, tushare_service, admin_user.user_id)
        
        logger.info("=" * 80)
        logger.info("同步完成！")
        logger.info("=" * 80)
        
    except Exception as e:
        logger.error(f"执行失败: {e}", exc_info=True)
    finally:
        db.close()


if __name__ == "__main__":
    main()

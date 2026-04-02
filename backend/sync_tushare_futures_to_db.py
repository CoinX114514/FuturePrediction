"""将 Tushare 期货主力合约同步到数据库的脚本。

此脚本会：
1. 从 Tushare fut_basic 拉取六大所普通合约，并按上市/退市日过滤「当前可交易」合约池；
2. 用 fut_mapping(trade_date=最近交易日) 得到各品种当前主力月合约 mapping_ts_code；
3. 每个交易所+品种（symbol）只保留一条主力合约，并在 futures_contracts / posts 中各对应一行帖子；
   换月时更新已有帖子的 contract_code 与标题，避免同一品种多帖。
"""

import os
import re
import sys
import logging
from datetime import datetime, date, timezone
from typing import Dict, Optional

import pandas as pd

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.database.models import FuturesContract, Post, User
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


def extract_symbol_prefix(contract_code: str) -> str:
    """从合约代码中取出品种字母前缀（与 fut_basic.symbol 对齐），如 CU2501->CU、I2603->I。"""
    if not contract_code:
        return ''
    m = re.match(r'^([A-Za-z]+)', str(contract_code).strip())
    return m.group(1).upper() if m else ''


def row_variety_key(row: pd.Series) -> str:
    """用交易所 + Tushare 品种标识构造帖子去重键（每个品种一帖）。"""
    ex = get_exchange_code(str(row.get('exchange', '') or ''))
    sym = row.get('symbol')
    if pd.notna(sym) and str(sym).strip():
        sym_u = str(sym).strip().upper()
    else:
        fc = row.get('fut_code')
        sym_u = str(fc).strip().upper() if pd.notna(fc) and str(fc).strip() else ''
    if not sym_u:
        sym_u = extract_symbol_prefix(convert_ts_code_to_contract_code(str(row.get('ts_code', '') or '')))
    return f'{ex}_{sym_u}'


def build_existing_posts_by_variety(db: Session) -> Dict[str, Post]:
    """构建 品种键 -> 帖子，用于主力换月时更新同帖而非新建。"""
    out: Dict[str, Post] = {}
    posts = (
        db.query(Post)
        .filter(and_(Post.status == 1, Post.contract_code.isnot(None)))
        .all()
    )
    for post in posts:
        sym = extract_symbol_prefix(post.contract_code or '')
        if not sym:
            continue
        fc = (
            db.query(FuturesContract)
            .filter(FuturesContract.contract_code == post.contract_code)
            .first()
        )
        if fc:
            vk = f'{fc.exchange_code}_{sym}'
        else:
            vk = f'__NFC___{sym}'
        out[vk] = post
    return out


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
    """将各品种「当前主力月」合约写入 futures_contracts，并保证每个交易所+品种仅一帖。

    Args:
        db: 数据库会话。
        tushare_service: Tushare 服务实例。
        author_id: 作者用户 ID（用于新建帖子）。

    Returns:
        统计字段：主力品种数、合约与帖子的创建/更新数、错误数。
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
        logger.info('正在从 Tushare 获取期货合约基本信息（普通合约，六大所）...')
        basic_df = tushare_service.get_futures_basic_info()
        if basic_df is None or basic_df.empty:
            logger.error('未能获取期货合约基本信息')
            return result

        logger.info('正在获取 fut_mapping（主力月合约，最近可用交易日）...')
        mapping_df = tushare_service.get_fut_main_mapping_for_latest_trade()
        if mapping_df is None or mapping_df.empty:
            logger.error('未能获取 fut_mapping，无法确定主力合约（请检查积分与 TUSHARE_TOKEN）')
            return result

        logger.info('正在获取最新日线（填充现价，可能受接口条数限制）...')
        daily_df = tushare_service.get_futures_daily()

        today = date.today()
        for _col in ('list_date', 'delist_date'):
            if _col in basic_df.columns:
                _s = basic_df[_col]
                _bad = _s.isna() | _s.astype(str).str.strip().str.lower().isin(
                    ('', '0', '00000000', 'none', 'nat', 'nan')
                )
                basic_df.loc[_bad, _col] = pd.NA

        if 'list_date' in basic_df.columns:
            basic_df['list_date'] = pd.to_datetime(basic_df['list_date'], format='%Y%m%d', errors='coerce')
        if 'delist_date' in basic_df.columns:
            basic_df['delist_date'] = pd.to_datetime(basic_df['delist_date'], format='%Y%m%d', errors='coerce')

        active_mask = True
        if 'list_date' in basic_df.columns:
            active_mask = active_mask & (basic_df['list_date'].notna()) & (basic_df['list_date'] <= pd.Timestamp(today))
        if 'delist_date' in basic_df.columns:
            active_mask = active_mask & (
                basic_df['delist_date'].isna() | (basic_df['delist_date'] >= pd.Timestamp(today))
            )
        active_pool = basic_df[active_mask].copy()

        main_ts_set = set(
            str(x).strip()
            for x in mapping_df['mapping_ts_code'].dropna().astype(str).unique()
            if str(x).strip()
        )
        active_pool['_ts'] = active_pool['ts_code'].astype(str).str.strip()
        main_rows = active_pool[active_pool['_ts'].isin(main_ts_set)].copy()
        if main_rows.empty:
            logger.error(
                '主力 mapping_ts_code 与当前可交易合约池无交集，请检查是否非交易日或数据延迟。'
                ' mapping 样例=%s pool 样例=%s',
                list(main_ts_set)[:5],
                active_pool['_ts'].head(5).tolist(),
            )
            return result

        main_rows['_vk'] = main_rows.apply(row_variety_key, axis=1)
        main_contracts = main_rows.drop_duplicates(subset=['_vk'], keep='first')
        result['contracts_total'] = len(main_contracts)
        logger.info(
            '主力合约品种数=%s（fut_mapping ∩ 上市未退市池且按交易所+品种去重）',
            len(main_contracts),
        )

        existing_contracts = {c.contract_code: c for c in db.query(FuturesContract).all()}
        existing_posts_by_variety = build_existing_posts_by_variety(db)
        post_service = PostService(db)
        commit_every = int(os.getenv('FUTURES_SYNC_COMMIT_EVERY', '150'))
        row_idx = 0

        for _, row in main_contracts.iterrows():
            row_idx += 1
            try:
                ts_code = str(row.get('ts_code', '')).strip()
                contract_code = convert_ts_code_to_contract_code(ts_code).upper()
                exchange = get_exchange_code(str(row.get('exchange', '')))
                contract_name = str(row.get('name', contract_code))
                variety_key = row['_vk']

                list_date = None
                if pd.notna(row.get('list_date')):
                    list_date = row['list_date'].date() if isinstance(row['list_date'], pd.Timestamp) else None
                expiry_date = None
                if pd.notna(row.get('delist_date')):
                    expiry_date = row['delist_date'].date() if isinstance(row['delist_date'], pd.Timestamp) else None

                multiplier = None
                if pd.notna(row.get('multiplier')):
                    try:
                        multiplier = float(row['multiplier'])
                    except (ValueError, TypeError):
                        pass

                current_price = None
                if daily_df is not None and not daily_df.empty:
                    matched = daily_df[daily_df['ts_code'].astype(str).str.strip() == ts_code]
                    if not matched.empty and 'close' in matched.columns:
                        close_price = matched.iloc[0]['close']
                        if pd.notna(close_price) and close_price != 0:
                            current_price = float(close_price)

                if contract_code in existing_contracts:
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
                    db.flush()
                    existing_contracts[contract_code] = contract
                    result['contracts_created'] += 1

                post_title = format_post_title(contract_code, exchange)
                sym_disp = row.get('symbol', '') or row.get('fut_code', '')

                post = existing_posts_by_variety.get(variety_key)
                if post is None:
                    stop_loss = current_price * 0.95 if current_price is not None else 0.0
                    content = (
                        f'【主力】品种 {variety_key} 当前映射月份合约 {contract_code}。\n\n'
                        f'品种代码: {sym_disp}\n'
                    )
                    if current_price is not None:
                        content += f'当前价格: {current_price}\n'
                    content += '\n请管理员编辑交易建议、止损价、止盈价等信息。'

                    post = post_service.create_post(
                        author_id=author_id,
                        title=post_title,
                        contract_code=contract_code,
                        stop_loss=stop_loss,
                        content=content,
                        current_price=current_price,
                        direction='buy',
                        suggestion='待管理员编辑建议（主力合约）',
                    )
                    existing_posts_by_variety[variety_key] = post
                    result['posts_created'] += 1
                else:
                    old_code = (post.contract_code or '').upper()
                    post.contract_code = contract_code
                    post.title = post_title
                    if current_price is not None:
                        post.current_price = current_price
                    post.updated_at = datetime.now(timezone.utc)
                    hint = f'（主力已切换至 {contract_code}）' if old_code != contract_code else ''
                    post.content = (
                        f'【主力】品种 {variety_key} 当前映射月份合约 {contract_code}{hint}。\n\n'
                        f'品种代码: {sym_disp}\n'
                        + (f'当前价格: {current_price}\n' if current_price is not None else '')
                        + '\n请管理员编辑交易建议、止损价、止盈价等信息。'
                    )
                    result['posts_updated'] += 1

            except Exception as e:
                logger.error('处理主力品种行失败: %s, ts_code=%s', e, row.get('ts_code', ''), exc_info=True)
                result['errors'] += 1
                continue

            if commit_every > 0 and row_idx % commit_every == 0:
                db.commit()
                logger.info('已提交中间进度 %s/%s 条', row_idx, len(main_contracts))

        db.commit()
        logger.info(
            '同步完成: 主力品种=%s, 合约创建=%s, 合约更新=%s, 帖子创建=%s, 帖子更新=%s, 错误=%s',
            result['contracts_total'],
            result['contracts_created'],
            result['contracts_updated'],
            result['posts_created'],
            result['posts_updated'],
            result['errors'],
        )
        return result

    except Exception as e:
        logger.error('同步期货主力合约失败: %s', e, exc_info=True)
        db.rollback()
        result['errors'] += 1
        return result


def main():
    """主函数。"""
    logger.info("=" * 80)
    logger.info("开始将 Tushare 各品种主力合约同步到数据库（每品种一帖）")
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

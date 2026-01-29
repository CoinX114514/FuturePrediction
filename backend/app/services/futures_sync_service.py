"""期货合约同步服务。

负责从 Tushare 获取所有可用期货合约，并自动创建对应的帖子卡片。

注意：此服务已被 sync_tushare_futures_to_db.py 脚本替代，建议使用脚本进行同步。
保留此服务以保持向后兼容性。
"""

import logging
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone, date, timedelta
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database.models import Post, User
from app.services.post_service import PostService
from app.services.price_update_service import PriceUpdateService
from app.services.tushare_service import TushareService

# 配置日志
logger = logging.getLogger(__name__)

# 期货品种代码到中文名称的映射表
FUTURES_SYMBOL_NAMES = {
    # 农产品
    'C': '玉米', 'A': '豆一', 'M': '豆粕', 'Y': '豆油', 'P': '棕榈油',
    'JD': '鸡蛋', 'CF': '棉花', 'SR': '白糖', 'WH': '强麦', 'PM': '普麦',
    'RI': '早籼稻', 'LR': '晚籼稻', 'JR': '粳稻', 'FB': '纤维板', 'BB': '胶合板',
    'LH': '生猪', 'PK': '花生', 'UR': '尿素', 'SA': '纯碱', 'PF': '短纤',
    # 能源化工
    'L': '塑料', 'V': 'PVC', 'PP': '聚丙烯', 'EB': '苯乙烯', 'EG': '乙二醇',
    'TA': 'PTA', 'MA': '甲醇', 'FU': '燃料油', 'BU': '沥青', 'RU': '橡胶',
    'NR': '20号胶', 'LU': '低硫燃料油', 'PG': '液化石油气', 'BR': '丁二烯橡胶',
    # 黑色金属
    'I': '铁矿石', 'J': '焦炭', 'JM': '焦煤', 'RB': '螺纹钢', 'HC': '热轧卷板',
    'SS': '不锈钢', 'SF': '硅铁', 'SM': '锰硅', 'SI': '工业硅', 'LC': '碳酸锂',
    # 有色金属
    'CU': '铜', 'AL': '铝', 'ZN': '锌', 'PB': '铅', 'NI': '镍', 'SN': '锡',
    # 贵金属
    'AU': '黄金', 'AG': '白银',
    # 金融期货
    'IF': '沪深300', 'IH': '上证50', 'IC': '中证500', 'IM': '中证1000',
    'TS': '2年期国债', 'TF': '5年期国债', 'T': '10年期国债', 'TL': '30年期国债',
    # 其他
    'SP': '纸浆', 'WR': '线材', 'BC': '国际铜', 'AO': '氧化铝',
}


class FuturesSyncService:
    """期货合约同步服务类。

    负责从 Tushare 获取期货合约列表，并自动创建对应的帖子。
    
    注意：建议使用 sync_tushare_futures_to_db.py 脚本进行同步，此服务保留用于向后兼容。
    """

    def __init__(self, db: Session):
        """初始化期货合约同步服务。

        Args:
            db: 数据库会话。
        """
        self.db = db
        self.post_service = PostService(db)
        self.price_service = PriceUpdateService(db)
        self.tushare_service = TushareService()

    def parse_contract_date(self, contract_code: str) -> Tuple[Optional[int], Optional[int]]:
        """解析合约代码中的年份和月份。

        Args:
            contract_code: 合约代码（如 'C2407', 'IF2312'）。

        Returns:
            Tuple[年份后两位, 月份]，如果解析失败返回 (None, None)。
        """
        # 合约代码格式：品种代码 + 年份后两位 + 月份（如 C2407, IF2312）
        # 提取最后4位数字：年份后两位 + 月份
        match = re.search(r'(\d{2})(\d{2})$', contract_code)
        if match:
            year_suffix = int(match.group(1))  # 年份后两位
            month = int(match.group(2))  # 月份
            return year_suffix, month
        return None, None

    def is_contract_active(self, contract_code: str) -> Tuple[bool, Optional[date]]:
        """判断合约是否活跃（未过期）。

        Args:
            contract_code: 合约代码。

        Returns:
            Tuple[是否活跃, 到期日期]，如果无法解析返回 (False, None)。
        """
        year_suffix, month = self.parse_contract_date(contract_code)
        if year_suffix is None or month is None:
            return False, None

        # 获取当前日期
        now = datetime.now()
        current_year = now.year % 100  # 年份后两位
        current_month = now.month
        current_full_year = now.year

        # 计算完整年份
        # 期货合约年份通常在当前年份的前后几年范围内
        # 如果年份后两位小于等于当前年份后两位，可能是当前年份或未来年份
        # 如果年份后两位大于当前年份后两位，可能是过去年份
        if year_suffix <= current_year:
            # 可能是当前年份或未来年份
            full_year = 2000 + year_suffix
            # 如果年份后两位明显小于当前年份（差距超过5年），可能是未来年份
            if year_suffix < current_year - 5:
                full_year = 2000 + year_suffix + 100
        else:
            # 年份后两位大于当前年份，可能是过去年份
            # 例如：现在是2026年（26），如果看到40，可能是2040年（未来）或2040-100=1940年（过去，不合理）
            # 所以如果差距不大（小于50），可能是过去年份
            if year_suffix - current_year < 50:
                full_year = 2000 + year_suffix - 100
            else:
                # 差距太大，可能是未来年份
                full_year = 2000 + year_suffix

        # 合约到期日期通常是合约月份的最后一天
        # 但实际交割日期可能更早，我们使用月份的最后一天作为参考
        if month == 12:
            expiry_date = date(full_year, 12, 31)
        else:
            # 下个月的第一天减一天
            next_month = month + 1
            next_year = full_year
            if next_month > 12:
                next_month = 1
                next_year += 1
            expiry_date = date(next_year, next_month, 1) - timedelta(days=1)

        # 判断是否过期（当前日期应该小于到期日期）
        # 为了安全，我们允许合约在当前月份之后的一个月内仍然被认为是活跃的
        # 因为有些合约可能在到期月份仍然交易
        today = date.today()
        is_active = today <= expiry_date

        return is_active, expiry_date

    def verify_contract_active_by_price(self, contract_code: str) -> bool:
        """通过尝试获取价格来验证合约是否活跃。

        Args:
            contract_code: 合约代码。

        Returns:
            bool: 如果能获取到价格则返回 True，否则返回 False。
        """
        try:
            price = self.price_service.get_futures_spot_price(contract_code)
            return price is not None
        except Exception:
            return False

    def get_weighted_continuous_contracts(self) -> List[Dict[str, any]]:
        """从 akshare 获取所有加权连续合约信息。

        Returns:
            List[Dict]: 加权连续合约信息列表，每个字典包含：
                - symbol: 品种代码（如 'V0', 'P0'）
                - contract_code: 合约代码（连续合约代码，如 'V0', 'P0'）
                - contract_name: 合约名称（如 'PVC连续', '棕榈油连续'）
                - current_price: 当前价格（最新收盘价）
                - exchange: 交易所代码
        """
        contracts = []
        
        try:
            # 获取所有连续合约列表
            continuous_list = ak.futures_display_main_sina()
            
            if continuous_list.empty:
                logger.warning("从 akshare 获取的连续合约列表为空")
                return contracts
            
            logger.info(f"从 akshare 获取到 {len(continuous_list)} 个连续合约")
            
            from datetime import datetime, timedelta
            
            for _, row in continuous_list.iterrows():
                try:
                    symbol = str(row.get('symbol', '')).strip()
                    contract_name = str(row.get('name', '')).strip()
                    exchange = str(row.get('exchange', '')).strip()
                    
                    if not symbol:
                        continue
                    
                    # 获取连续合约的最新价格
                    current_price = None
                    try:
                        # 尝试获取最近一年的数据
                        end_date = datetime.now().strftime('%Y%m%d')
                        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
                        
                        data = ak.futures_main_sina(symbol=symbol, start_date=start_date, end_date=end_date)
                        
                        if not data.empty:
                            # 获取最新收盘价
                            current_price = float(data.iloc[-1]['收盘价'])
                    except Exception as e:
                        logger.debug(f"无法获取连续合约 {symbol} 的价格: {e}")
                        # 如果指定日期范围失败，尝试使用默认参数
                        try:
                            data = ak.futures_main_sina(symbol=symbol)
                            if not data.empty:
                                current_price = float(data.iloc[-1]['收盘价'])
                        except Exception as e2:
                            logger.debug(f"使用默认参数也无法获取连续合约 {symbol} 的价格: {e2}")
                    
                    # 获取品种中文名称（从连续合约名称中提取，或使用映射表）
                    variety_name = contract_name.replace('连续', '').strip()
                    # 如果名称中没有品种信息，尝试从symbol获取
                    if not variety_name or len(variety_name) < 2:
                        variety_name = FUTURES_SYMBOL_NAMES.get(symbol, symbol)
                        contract_name = f"{variety_name}连续"
                    
                    # 构建合约信息
                    contract_info = {
                        'symbol': symbol,
                        'contract_code': symbol.upper(),  # 连续合约代码如 V0, P0
                        'contract_name': contract_name,
                        'current_price': current_price,
                        'exchange': exchange,
                        'is_continuous': True,  # 标记为连续合约
                    }
                    
                    contracts.append(contract_info)
                    
                except Exception as e:
                    logger.warning(f"处理连续合约数据时出错: {e}, 行数据: {row.to_dict()}")
                    continue
            
            logger.info(f"成功解析 {len(contracts)} 个连续合约")
            return contracts
            
        except Exception as e:
            logger.error(f"从 akshare 获取连续合约列表失败: {str(e)}", exc_info=True)
            return contracts

    def get_all_futures_contracts(self, include_continuous: bool = False) -> List[Dict[str, any]]:
        """从 akshare 获取所有期货合约信息。

        Args:
            include_continuous: 是否包含加权连续合约（默认 False）。

        Returns:
            List[Dict]: 期货合约信息列表，每个字典包含：
                - symbol: 品种代码（如 'C', 'A'）
                - contract_code: 合约代码（如 'C2407', 'A2407'）
                - contract_name: 合约名称
                - current_price: 当前价格
                - spot_price: 现货价格
        """
        contracts = []
        
        try:
            # 方法1: 优先从实时行情获取所有活跃合约
            realtime_contracts = set()  # 记录从实时行情获取的合约代码，避免重复
            try:
                logger.info("尝试从实时行情获取所有活跃合约...")
                realtime_data = ak.futures_zh_realtime()
                
                if realtime_data is not None and not realtime_data.empty and 'symbol' in realtime_data.columns:
                    logger.info(f"从实时行情获取到 {len(realtime_data)} 个合约数据")
                    
                    # 处理实时行情数据
                    for _, row in realtime_data.iterrows():
                        try:
                            contract_code = str(row.get('symbol', '')).strip().upper()
                            
                            # 跳过连续合约代码（格式：1-2个字母 + 0，如 V0, P0, TA0）
                            # 正常合约代码格式：字母 + 数字 + 数字 + 数字 + 数字（如 TA2610）
                            # 判断：如果代码长度 <= 3 且以 0 结尾，则是连续合约
                            if not contract_code or len(contract_code) < 4:
                                continue
                            # 只跳过真正的连续合约（长度 <= 3 且以 0 结尾）
                            if len(contract_code) <= 3 and contract_code.endswith('0'):
                                continue
                            
                            # 检查合约是否活跃（未过期）
                            is_active, expiry_date = self.is_contract_active(contract_code)
                            if not is_active:
                                logger.debug(f"跳过已过期合约: {contract_code} (到期日期: {expiry_date})")
                                continue
                            
                            # 获取价格
                            current_price = None
                            for price_col in ['trade', 'close', 'settlement', 'current_price', '最新价', '现价']:
                                if price_col in row.index:
                                    price_value = row.get(price_col)
                                    if pd.notna(price_value) and price_value != 0:
                                        try:
                                            current_price = float(price_value)
                                            break
                                        except (ValueError, TypeError):
                                            continue
                            
                            # 如果没有价格，跳过
                            if current_price is None:
                                logger.debug(f"无法获取合约 {contract_code} 的价格，跳过")
                                continue
                            
                            # 提取品种代码（合约代码的前1-2个字符）
                            symbol = contract_code[:2] if len(contract_code) >= 2 and contract_code[1].isdigit() else contract_code[:1]
                            
                            # 获取合约名称（优先使用实时行情中的name字段）
                            contract_name = None
                            if 'name' in row.index:
                                name_value = row.get('name')
                                if pd.notna(name_value) and name_value:
                                    name_str = str(name_value).strip()
                                    # 如果名称包含"连续"，说明这是连续合约的名称，需要根据合约代码生成
                                    if '连续' in name_str:
                                        # 提取品种名称（去掉"连续"）
                                        variety_name = name_str.replace('连续', '').strip()
                                        # 从合约代码中提取年份月份部分（最后4位数字）
                                        import re
                                        year_month_match = re.search(r'(\d{4})$', contract_code)
                                        if year_month_match:
                                            year_month = year_month_match.group(1)
                                            contract_name = f"{variety_name}{year_month}"
                                        else:
                                            # 如果无法提取年份月份，直接拼接
                                            contract_name = f"{variety_name}{contract_code}"
                                    else:
                                        # 如果名称已经是完整合约名称（如 PTA2605），直接使用
                                        contract_name = name_str
                            
                            # 如果没有从实时行情获取到名称，使用映射表生成
                            if not contract_name:
                                # 获取品种中文名称
                                variety_name = FUTURES_SYMBOL_NAMES.get(symbol, symbol)
                                # 从合约代码中提取年份月份部分（最后4位数字）
                                import re
                                year_month_match = re.search(r'(\d{4})$', contract_code)
                                if year_month_match:
                                    year_month = year_month_match.group(1)
                                    contract_name = f"{variety_name}{year_month}"
                                else:
                                    # 如果无法提取年份月份，直接拼接
                                    contract_name = f"{variety_name}{contract_code}"
                            
                            # 构建合约信息
                            contract_info = {
                                'symbol': symbol,
                                'contract_code': contract_code,
                                'contract_name': contract_name,
                                'current_price': current_price,
                                'spot_price': None,  # 实时行情没有现货价格
                                'is_continuous': False,
                            }
                            
                            contracts.append(contract_info)
                            realtime_contracts.add(contract_code)
                            
                        except Exception as e:
                            logger.debug(f"处理实时行情合约数据时出错: {e}")
                            continue
                    
                    if contracts and len(contracts) > 0:
                        logger.info(f"从实时行情成功获取 {len(contracts)} 个活跃合约")
            except Exception as e:
                logger.warning(f"从实时行情获取合约失败，尝试备用方法: {str(e)[:100]}")
            
            # 方法2: 从各交易所获取2026年的合约信息
            try:
                logger.info("尝试从各交易所获取2026年合约信息...")
                exchanges = {
                    'shfe': '上海期货交易所',
                    'czce': '郑州商品交易所',
                    'cffex': '中国金融期货交易所',
                    'ine': '上海国际能源交易中心'
                }
                
                exchange_contracts = []
                for exchange_code, exchange_name in exchanges.items():
                    try:
                        func_name = f'futures_contract_info_{exchange_code}'
                        if hasattr(ak, func_name):
                            func = getattr(ak, func_name)
                            contracts = func()
                            
                            if not contracts.empty:
                                # 查找合约代码列
                                code_col = None
                                for col in contracts.columns:
                                    if '合约代码' in str(col) or '代码' in str(col) or 'contract' in str(col).lower():
                                        code_col = col
                                        break
                                
                                if code_col:
                                    # 筛选2026年的合约
                                    processed_contracts = set()  # 用于去重
                                    for _, row in contracts.iterrows():
                                        contract_code = str(row[code_col]).upper().strip()
                                        
                                        # 跳过无效的合约代码（如列名、空值等）
                                        if not contract_code or len(contract_code) < 4:
                                            continue
                                        if contract_code in ['合约代码', '代码', 'CONTRACT_CODE', 'CODE']:
                                            continue
                                        
                                        # 去重
                                        if contract_code in processed_contracts:
                                            continue
                                        processed_contracts.add(contract_code)
                                        
                                        # 跳过期权合约（包含-C-或-P-的）
                                        if '-C-' in contract_code or '-P-' in contract_code:
                                            continue
                                        
                                        # 检查是否是2026年的合约
                                        # 标准格式：字母+26+月份（如C2607, SC2603）
                                        if re.search(r'26\d{2}$', contract_code):
                                            # 检查合约是否活跃
                                            is_active, expiry_date = self.is_contract_active(contract_code)
                                            if is_active:
                                                # 提取品种代码
                                                symbol_match = re.match(r'^([A-Z]{1,3})', contract_code)
                                                symbol = symbol_match.group(1) if symbol_match else contract_code[:2]
                                                
                                                # 获取品种中文名称
                                                variety_name = FUTURES_SYMBOL_NAMES.get(symbol, symbol)
                                                
                                                # 生成合约名称
                                                year_month_match = re.search(r'(\d{4})$', contract_code)
                                                if year_month_match:
                                                    year_month = year_month_match.group(1)
                                                    contract_name = f"{variety_name}{year_month}"
                                                else:
                                                    contract_name = f"{variety_name}{contract_code}"
                                                
                                                # 尝试获取价格（但不强制要求）
                                                price = None
                                                try:
                                                    price = self.price_service.get_futures_spot_price(contract_code)
                                                except Exception as e:
                                                    logger.debug(f"无法获取合约 {contract_code} 的价格: {e}")
                                                
                                                # 即使无法获取价格，如果合约是活跃的，也添加（价格可以为None）
                                                exchange_contracts.append({
                                                    'symbol': symbol,
                                                    'contract_code': contract_code,
                                                    'contract_name': contract_name,
                                                    'current_price': price,  # 可能为None，后续价格更新任务会填充
                                                    'spot_price': None,
                                                    'is_continuous': False,
                                                })
                                                realtime_contracts.add(contract_code)
                    except Exception as e:
                        logger.debug(f"获取 {exchange_name} 合约信息失败: {e}")
                
                if exchange_contracts and len(exchange_contracts) > 0:
                    logger.info(f"从各交易所获取到 {len(exchange_contracts)} 个活跃合约")
                    # 确保contracts是列表
                    if not isinstance(contracts, list):
                        contracts = list(contracts) if contracts is not None else []
                    contracts.extend(exchange_contracts)
            except Exception as e:
                logger.warning(f"从各交易所获取合约失败: {str(e)[:100]}")
            
            # 方法3: 为所有品种生成2026年的主要合约月份，并验证是否活跃
            try:
                logger.info("尝试为所有品种生成2026年合约...")
                spot_data = ak.futures_spot_price()
                
                if not spot_data.empty:
                    all_symbols = spot_data['symbol'].unique().tolist()
                    # 主要交易月份
                    main_months = ['01', '03', '05', '07', '09', '11', '12']
                    
                    generated_contracts = []
                    for symbol in all_symbols:
                        for month in main_months:
                            contract_code = f"{symbol}26{month}".upper()
                            
                            # 跳过已经在实时行情或交易所数据中出现的合约
                            if contract_code in realtime_contracts:
                                continue
                            
                            # 检查合约是否活跃（未过期）
                            is_active, expiry_date = self.is_contract_active(contract_code)
                            if not is_active:
                                continue
                            
                            # 尝试获取价格验证合约是否真的活跃
                            price = None
                            try:
                                price = self.price_service.get_futures_spot_price(contract_code)
                            except Exception as e:
                                logger.debug(f"无法获取合约 {contract_code} 的价格: {e}")
                            
                            # 即使无法获取价格，如果合约是活跃的，也添加
                            # 获取品种中文名称
                            variety_name = FUTURES_SYMBOL_NAMES.get(symbol, symbol)
                            contract_name = f"{variety_name}26{month}"
                            
                            generated_contracts.append({
                                'symbol': symbol,
                                'contract_code': contract_code,
                                'contract_name': contract_name,
                                'current_price': price,
                                'spot_price': None,
                                'is_continuous': False,
                            })
                            realtime_contracts.add(contract_code)
                    
                    if generated_contracts:
                        logger.info(f"为所有品种生成了 {len(generated_contracts)} 个2026年合约")
                        if not isinstance(contracts, list):
                            contracts = list(contracts) if contracts is not None else []
                        contracts.extend(generated_contracts)
            except Exception as e:
                logger.warning(f"生成2026年合约失败: {str(e)[:100]}")
            
            # 方法4: 备用方法 - 从期货现货价格数据获取，但只添加未在实时行情中出现的品种
            spot_data = ak.futures_spot_price()
            
            if not spot_data.empty:
                logger.info(f"从期货现货价格数据获取到 {len(spot_data)} 个期货品种数据，补充实时行情未覆盖的品种")
                
                for _, row in spot_data.iterrows():
                    try:
                        symbol = str(row.get('symbol', '')).strip().upper()
                        dominant_contract = str(row.get('dominant_contract', '')).strip()
                        dominant_price = row.get('dominant_contract_price')
                        spot_price = row.get('spot_price')
                        
                        if not symbol or not dominant_contract:
                            continue
                        
                        # 确保合约代码是大写格式（如 C2407）
                        contract_code = dominant_contract.upper()
                        
                        # 如果这个合约已经在实时行情中出现，跳过
                        if contract_code in realtime_contracts:
                            continue
                        
                        # 检查合约是否活跃（未过期）
                        is_active, expiry_date = self.is_contract_active(contract_code)
                        if not is_active:
                            logger.debug(f"跳过已过期合约: {contract_code} (到期日期: {expiry_date})")
                            continue
                        
                        # 尝试通过价格验证合约是否真的活跃
                        # 如果能获取到实时价格，说明合约活跃
                        current_price = None
                        try:
                            # 尝试获取实时价格
                            realtime_price = self.price_service.get_futures_spot_price(contract_code)
                            if realtime_price is not None:
                                current_price = realtime_price
                        except Exception as e:
                            logger.debug(f"无法获取合约 {contract_code} 的实时价格: {e}")
                        
                        # 如果无法获取实时价格，使用主力合约价格（但需要再次验证）
                        if current_price is None:
                            if pd.notna(dominant_price):
                                try:
                                    current_price = float(dominant_price)
                                except (ValueError, TypeError):
                                    pass
                        
                        # 如果仍然没有价格，不强制要求（合约可能是新上市的，暂时没有价格数据）
                        # 只要合约是活跃的（未过期），就创建帖子，价格可以在后续更新
                        # 注释掉价格验证，允许创建没有价格的活跃合约
                        # if current_price is None:
                        #     # 尝试通过价格验证
                        #     if not self.verify_contract_active_by_price(contract_code):
                        #         logger.debug(f"无法获取合约 {contract_code} 的价格，可能已不活跃，跳过")
                        #         continue
                        
                        # 获取品种中文名称
                        variety_name = FUTURES_SYMBOL_NAMES.get(symbol, symbol)
                        # 生成合约名称，格式：品种名称 + 合约代码（如：玉米C2607）
                        contract_name = f"{variety_name}{contract_code}"
                        
                        # 构建合约信息
                        contract_info = {
                            'symbol': symbol,
                            'contract_code': contract_code,
                            'contract_name': contract_name,
                            'current_price': current_price,
                            'spot_price': float(spot_price) if pd.notna(spot_price) else None,
                            'is_continuous': False,  # 标记为主力合约
                        }
                        
                        contracts.append(contract_info)
                        
                    except Exception as e:
                        logger.warning(f"处理期货合约数据时出错: {e}, 行数据: {row.to_dict()}")
                        continue
            
            # 如果包含连续合约，添加连续合约
            continuous_count = 0
            if include_continuous:
                continuous_contracts = self.get_weighted_continuous_contracts()
                continuous_count = len(continuous_contracts)
                contracts.extend(continuous_contracts)
            
            # 确保contracts是列表
            if not isinstance(contracts, list):
                contracts = list(contracts) if contracts is not None else []
            
            dominant_count = len(contracts) - continuous_count
            logger.info(f"成功解析 {len(contracts)} 个期货合约（主力合约: {dominant_count}, 连续合约: {continuous_count}）")
            return contracts
            
        except Exception as e:
            logger.error(f"从 akshare 获取期货合约列表失败: {str(e)}", exc_info=True)
            return contracts

    def sync_futures_to_posts(
        self,
        author_id: int,
        update_existing: bool = False,
        include_continuous: bool = False
    ) -> Dict[str, int]:
        """同步期货合约到帖子。

        为每个期货合约创建一个帖子卡片（如果不存在）。
        如果合约已存在对应的帖子，则根据 update_existing 决定是否更新。

        Args:
            author_id: 作者用户ID（通常是系统管理员）。
            update_existing: 是否更新已存在的帖子（默认 False，只创建新帖子）。

        Returns:
            Dict: 同步结果统计：
                - total: 总合约数
                - created: 新创建的帖子数
                - updated: 更新的帖子数
                - skipped: 跳过的帖子数（已存在且不更新）
                - failed: 失败的帖子数
        """
        result = {
            'total': 0,
            'created': 0,
            'updated': 0,
            'skipped': 0,
            'failed': 0,
        }
        
        try:
            # 获取所有期货合约（可选择是否包含连续合约）
            contracts = self.get_all_futures_contracts(include_continuous=include_continuous)
            result['total'] = len(contracts)
            
            if not contracts:
                logger.warning("没有获取到任何期货合约，同步终止")
                return result
            
            logger.info(f"开始同步 {len(contracts)} 个期货合约到帖子...")
            
            # 获取所有已存在的帖子（按合约代码）
            existing_posts = {
                post.contract_code.upper(): post
                for post in self.db.query(Post).filter(
                    and_(Post.status == 1, Post.contract_code.isnot(None))
                ).all()
            }
            
            # 遍历每个合约，创建或更新帖子
            for contract in contracts:
                # 确保contract是字典
                if not isinstance(contract, dict):
                    logger.warning(f"跳过非字典类型的合约数据: {contract}")
                    result['failed'] += 1
                    continue
                
                contract_code = contract.get('contract_code')
                if not contract_code:
                    logger.warning(f"跳过无合约代码的合约: {contract}")
                    result['failed'] += 1
                    continue
                
                try:
                    # 检查是否已存在
                    if contract_code in existing_posts:
                        if update_existing:
                            # 更新现有帖子
                            post = existing_posts[contract_code]
                            
                            # 更新价格
                            if contract.get('current_price') is not None:
                                post.current_price = contract['current_price']
                            
                            # 更新标题和名称（使用新的合约名称）
                            contract_name = contract.get('contract_name', contract_code)
                            if contract_code.upper() in contract_name.upper():
                                post.title = contract_name
                            else:
                                post.title = f"{contract_name} ({contract_code})"
                            
                            post.updated_at = datetime.now(timezone.utc)
                            self.db.commit()
                            result['updated'] += 1
                            logger.debug(f"已更新帖子: {contract_code}, 新标题: {post.title}")
                        else:
                            # 跳过已存在的帖子
                            result['skipped'] += 1
                            logger.debug(f"跳过已存在的帖子: {contract_code}")
                        continue
                    
                    # 创建新帖子
                    current_price = contract.get('current_price')
                    
                    # 如果没有价格，设置一个默认的止损价（价格的 95%）
                    stop_loss = None
                    if current_price is not None:
                        stop_loss = current_price * 0.95
                    else:
                        # 如果没有价格，使用一个默认值（后续管理员可以修改）
                        stop_loss = 0.0
                    
                    # 创建帖子标题（使用合约名称）
                    contract_name = contract.get('contract_name', contract_code)
                    # 如果名称已经包含合约代码，直接使用；否则添加合约代码
                    if contract_code.upper() in contract_name.upper():
                        title = contract_name
                    else:
                        title = f"{contract_name} ({contract_code})"
                    
                    # 创建帖子内容（默认内容，管理员可以后续编辑）
                    content = f"期货合约 {contract_code} 的交易建议。\n\n"
                    content += f"品种代码: {contract['symbol']}\n"
                    if current_price is not None:
                        content += f"当前价格: {current_price}\n"
                    if contract.get('spot_price') is not None:
                        content += f"现货价格: {contract['spot_price']}\n"
                    content += "\n请管理员编辑此帖子的交易建议、止损价、止盈价等信息。"
                    
                    # 创建帖子
                    post = self.post_service.create_post(
                        author_id=author_id,
                        title=title,
                        contract_code=contract_code,
                        stop_loss=stop_loss,
                        content=content,
                        current_price=current_price,
                        direction='buy',  # 默认做多
                        suggestion="待管理员编辑建议",
                    )
                    
                    result['created'] += 1
                    logger.info(f"已创建新帖子: {contract_code} (post_id: {post.post_id})")
                    
                except Exception as e:
                    result['failed'] += 1
                    logger.error(f"处理合约 {contract_code} 时出错: {str(e)}", exc_info=True)
                    continue
            
            self.db.commit()
            
            logger.info(
                f"期货合约同步完成: "
                f"总数={result['total']}, "
                f"创建={result['created']}, "
                f"更新={result['updated']}, "
                f"跳过={result['skipped']}, "
                f"失败={result['failed']}"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"同步期货合约到帖子失败: {str(e)}", exc_info=True)
            result['failed'] = result['total']  # 标记为全部失败
            return result

    def get_post_by_contract_code(self, contract_code: str) -> Optional[Post]:
        """根据合约代码获取帖子。

        Args:
            contract_code: 合约代码。

        Returns:
            Optional[Post]: 帖子对象，如果不存在则返回 None。
        """
        return self.db.query(Post).filter(
            and_(
                Post.contract_code == contract_code.upper(),
                Post.status == 1
            )
        ).first()


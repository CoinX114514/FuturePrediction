"""期货命名工具。

统一帖子标题格式为三段式：「交易所」「品类」「代码」。
"""

import re
from typing import Optional

# 交易所代码 -> 中文名称（简短，用于标题）
EXCHANGE_NAMES = {
    'SHFE': '上期所',
    'DCE': '大商所',
    'CZCE': '郑商所',
    'CFFEX': '中金所',
    'INE': '上能源',
    'GFEX': '广期所',
}

# 品种代码 -> 品类中文名称
SYMBOL_CATEGORY_NAMES = {
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
    'OI': '菜油', 'RM': '菜粕', 'ZC': '动力煤', 'AP': '苹果', 'CJ': '红枣',
    'FG': '玻璃', 'CY': '棉纱', 'PL': '丙烯', 'SH': '烧碱', 'EC': '集运指数',
    'LG': '碳酸锂',  # 广期所碳酸锂
}


def extract_symbol(contract_code: str) -> str:
    """从合约代码中提取品种部分（仅字母）。
    
    例如：I2603 -> I, CU2601 -> CU, SS2606 -> SS。
    """
    if not contract_code:
        return ''
    match = re.match(r'^([A-Za-z]+)', str(contract_code).strip())
    return match.group(1).upper() if match else contract_code[:1].upper()


def get_exchange_name(exchange_code: Optional[str]) -> str:
    """获取交易所中文名称。"""
    if not exchange_code:
        return '未知'
    return EXCHANGE_NAMES.get(str(exchange_code).upper(), exchange_code)


def get_category_name(symbol: str) -> str:
    """获取品种品类中文名称。"""
    if not symbol:
        return '未知'
    return SYMBOL_CATEGORY_NAMES.get(symbol.upper(), symbol)


def format_post_title(contract_code: str, exchange_code: Optional[str] = None) -> str:
    """生成三段式帖子标题：「交易所」「品类」「代码」。
    
    例如：大商所 铁矿石 I2603、上期所 铜 CU2601。
    
    Args:
        contract_code: 合约代码，如 I2603、CU2601。
        exchange_code: 交易所代码（可选），如 DCE、SHFE。若不传则根据品种推断。
    
    Returns:
        格式化后的标题字符串。
    """
    contract_code = (contract_code or '').strip().upper()
    if not contract_code:
        return '未知合约'
    
    symbol = extract_symbol(contract_code)
    
    # 交易所：优先使用传入的 exchange_code，否则根据品种推断
    if exchange_code:
        exchange_name = get_exchange_name(exchange_code)
    else:
        exchange_name = _infer_exchange_name(symbol)
    
    category = get_category_name(symbol)
    
    return f"{exchange_name} {category} {contract_code}"


def _infer_exchange_name(symbol: str) -> str:
    """根据品种代码推断交易所名称。"""
    exchange_by_symbol = {
        'IF': '中金所', 'IH': '中金所', 'IC': '中金所', 'IM': '中金所',
        'T': '中金所', 'TF': '中金所', 'TS': '中金所', 'TL': '中金所',
        'C': '大商所', 'A': '大商所', 'M': '大商所', 'Y': '大商所', 'P': '大商所',
        'JD': '大商所', 'L': '大商所', 'V': '大商所', 'PP': '大商所', 'EB': '大商所',
        'EG': '大商所', 'I': '大商所', 'J': '大商所', 'JM': '大商所',
        'FB': '大商所', 'BB': '大商所', 'LG': '大商所',
        'CF': '郑商所', 'SR': '郑商所', 'TA': '郑商所', 'OI': '郑商所', 'MA': '郑商所',
        'FG': '郑商所', 'RM': '郑商所', 'ZC': '郑商所', 'SF': '郑商所', 'SM': '郑商所',
        'AP': '郑商所', 'CJ': '郑商所', 'UR': '郑商所', 'SA': '郑商所', 'PF': '郑商所',
        'PK': '郑商所', 'LH': '郑商所', 'RI': '郑商所', 'LR': '郑商所', 'JR': '郑商所',
        'PM': '郑商所', 'WH': '郑商所', 'CY': '郑商所', 'PL': '郑商所', 'SH': '郑商所',
        'CU': '上期所', 'AL': '上期所', 'ZN': '上期所', 'PB': '上期所', 'NI': '上期所',
        'SN': '上期所', 'AU': '上期所', 'AG': '上期所', 'RB': '上期所', 'HC': '上期所',
        'SS': '上期所', 'BU': '上期所', 'RU': '上期所', 'FU': '上期所', 'WR': '上期所',
        'SP': '上期所', 'AO': '上期所', 'BC': '上期所', 'BR': '上期所',
        'SC': '上能源', 'LU': '上能源', 'NR': '上能源', 'EC': '上能源',
        'SI': '广期所', 'LC': '广期所',
    }
    return exchange_by_symbol.get(symbol.upper(), '未知')

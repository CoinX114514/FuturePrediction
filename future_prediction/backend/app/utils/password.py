"""密码处理工具函数。

负责密码加密和验证。
"""

import bcrypt


def hash_password(password: str) -> str:
    """加密密码。

    Args:
        password: 明文密码。

    Returns:
        str: 加密后的密码哈希值。
    """
    # 确保密码是字节串
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # bcrypt 限制密码长度为 72 字节
    if len(password) > 72:
        password = password[:72]
    
    # 生成盐并加密密码
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password, salt)
    
    # 返回字符串格式的哈希值
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码。

    Args:
        plain_password: 明文密码。
        hashed_password: 加密后的密码哈希值。

    Returns:
        bool: 如果密码匹配返回 True，否则返回 False。
    """
    # 确保密码是字节串
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    # 确保哈希值是字节串
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    # bcrypt 限制密码长度为 72 字节
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    
    # 验证密码
    try:
        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception:
        return False


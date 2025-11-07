"""创建开发者账户脚本。

直接在数据库中创建开发者账户，用于测试。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.database.models import User
from app.utils.password import hash_password


def create_dev_user():
    """创建开发者账户。"""
    print("=" * 80)
    print("创建开发者账户")
    print("=" * 80)
    
    # 开发者账户信息
    username = "admin"
    password = "114514"
    phone_number = "13800000000"  # 使用一个测试手机号
    email = "admin@dev.local"  # 使用一个测试邮箱
    user_role = 3  # 超级管理员
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 检查用户是否已存在
        existing_user = db.query(User).filter(
            (User.phone_number == phone_number) | (User.email == email)
        ).first()
        
        if existing_user:
            print(f"\n用户已存在:")
            print(f"  用户ID: {existing_user.user_id}")
            print(f"  手机号: {existing_user.phone_number}")
            print(f"  邮箱: {existing_user.email}")
            print(f"  角色: {existing_user.user_role}")
            print(f"\n是否要更新密码？(y/n): ", end="")
            choice = input().strip().lower()
            
            if choice == 'y':
                # 更新密码
                existing_user.password_hash = hash_password(password)
                db.commit()
                print(f"\n✓ 密码已更新！")
                print(f"  用户名: {username}")
                print(f"  密码: {password}")
            else:
                print("\n取消更新。")
            return
        
        # 创建新用户
        print(f"\n创建新用户...")
        print(f"  用户名: {username}")
        print(f"  密码: {password}")
        print(f"  手机号: {phone_number}")
        print(f"  邮箱: {email}")
        print(f"  角色: 超级管理员 (user_role=3)")
        
        # 哈希密码
        password_hash = hash_password(password)
        
        # 创建用户对象
        new_user = User(
            phone_number=phone_number,
            email=email,
            password_hash=password_hash,
            user_role=user_role,
            nickname=username,
            is_active=True,
            prediction_count=0,
            daily_prediction_limit=999999,  # 开发者账户无限制
        )
        
        # 添加到数据库
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        print(f"\n✓ 用户创建成功！")
        print(f"  用户ID: {new_user.user_id}")
        print(f"  手机号: {new_user.phone_number}")
        print(f"  邮箱: {new_user.email}")
        print(f"  角色: {new_user.user_role} (超级管理员)")
        print(f"\n登录信息:")
        print(f"  手机号: {phone_number}")
        print(f"  密码: {password}")
        print(f"  或")
        print(f"  邮箱: {email}")
        print(f"  密码: {password}")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 创建用户失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    create_dev_user()


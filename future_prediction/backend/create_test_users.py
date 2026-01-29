"""创建测试账户脚本。

在数据库中创建所有类型的测试账户，用于测试权限管理。
"""

import sys
import os
from datetime import datetime, timedelta, timezone

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal
from app.database.models import User
from app.utils.password import hash_password


def create_test_users():
    """创建所有类型的测试账户。"""
    print("=" * 80)
    print("创建测试账户")
    print("=" * 80)
    
    # 定义测试账户信息
    test_users = [
        {
            "phone_number": "13800000001",
            "email": "normal@test.com",
            "nickname": "普通用户",
            "password": "123456",
            "user_role": 1,  # 普通用户
            "daily_prediction_limit": 5,
            "member_expire_time": None,
        },
        {
            "phone_number": "13800000002",
            "email": "member@test.com",
            "nickname": "VIP会员",
            "password": "123456",
            "user_role": 2,  # 会员
            "daily_prediction_limit": 999999,  # 会员无限制
            "member_expire_time": datetime.now(timezone.utc) + timedelta(days=365),  # 1年后过期
        },
        {
            "phone_number": "13800000003",
            "email": "admin@test.com",
            "nickname": "超级管理员",
            "password": "123456",
            "user_role": 3,  # 超级管理员
            "daily_prediction_limit": 999999,
            "member_expire_time": None,
        },
    ]
    
    # 创建数据库会话
    db = SessionLocal()
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    try:
        for user_data in test_users:
            phone_number = user_data["phone_number"]
            email = user_data["email"]
            
            # 检查用户是否已存在
            existing_user = db.query(User).filter(
                (User.phone_number == phone_number) | (User.email == email)
            ).first()
            
            if existing_user:
                print(f"\n用户已存在: {user_data['nickname']} ({phone_number})")
                print(f"  当前角色: {existing_user.user_role}")
                
                # 更新用户信息（包括密码和角色）
                existing_user.password_hash = hash_password(user_data["password"])
                existing_user.user_role = user_data["user_role"]
                existing_user.nickname = user_data["nickname"]
                existing_user.daily_prediction_limit = user_data["daily_prediction_limit"]
                existing_user.member_expire_time = user_data["member_expire_time"]
                existing_user.is_active = True
                
                db.commit()
                updated_count += 1
                print(f"  ✓ 用户信息已更新")
            else:
                # 创建新用户
                password_hash = hash_password(user_data["password"])
                
                new_user = User(
                    phone_number=phone_number,
                    email=email,
                    password_hash=password_hash,
                    user_role=user_data["user_role"],
                    nickname=user_data["nickname"],
                    is_active=True,
                    prediction_count=0,
                    daily_prediction_limit=user_data["daily_prediction_limit"],
                    member_expire_time=user_data["member_expire_time"],
                )
                
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                
                created_count += 1
                print(f"\n✓ 创建用户: {user_data['nickname']}")
                print(f"  用户ID: {new_user.user_id}")
        
        print("\n" + "=" * 80)
        print("创建结果汇总")
        print("=" * 80)
        print(f"  新建账户: {created_count} 个")
        print(f"  更新账户: {updated_count} 个")
        print(f"  跳过账户: {skipped_count} 个")
        
        print("\n" + "=" * 80)
        print("测试账户登录信息")
        print("=" * 80)
        
        role_names = {
            1: "普通用户",
            2: "VIP会员",
            3: "超级管理员",
        }
        
        for user_data in test_users:
            role_name = role_names[user_data["user_role"]]
            print(f"\n【{role_name}】")
            print(f"  昵称: {user_data['nickname']}")
            print(f"  手机号: {user_data['phone_number']}")
            print(f"  邮箱: {user_data['email']}")
            print(f"  密码: {user_data['password']}")
            print(f"  角色ID: {user_data['user_role']}")
            if user_data['member_expire_time']:
                print(f"  VIP到期: {user_data['member_expire_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n" + "=" * 80)
        print("权限说明")
        print("=" * 80)
        print("  普通用户 (role=1):")
        print("    - 每日预测限制: 5次")
        print("    - 可以查看和收藏帖子")
        print("    - 不能发布帖子（需要管理员权限）")
        print("\n  VIP会员 (role=2):")
        print("    - 每日预测限制: 无限制")
        print("    - 可以查看和收藏帖子")
        print("    - 不能发布帖子（需要管理员权限）")
        print("\n  超级管理员 (role=3):")
        print("    - 每日预测限制: 无限制")
        print("    - 可以查看和收藏帖子")
        print("    - 可以发布和管理帖子")
        print("    - 可以访问管理员发布页面")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 操作失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    create_test_users()

#!/usr/bin/env python3
"""创建样例帖子数据脚本。

在数据库中创建一些样例帖子，用于测试和展示。
"""

import sys
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.database.models import User
from app.services.post_service import PostService


def create_sample_posts():
    """创建样例帖子。"""
    db: Session = SessionLocal()
    
    try:
        # 查找管理员用户（用于作为帖子作者）
        admin_user = db.query(User).filter(User.user_role >= 3).first()
        
        if not admin_user:
            print("错误：未找到管理员用户，无法创建帖子")
            print("请先运行 create_test_users.py 创建测试用户")
            return
        
        print(f"使用管理员用户作为作者: {admin_user.nickname} (ID: {admin_user.user_id})")
        print("=" * 80)
        
        post_service = PostService(db)
        
        # 定义样例帖子数据
        sample_posts = [
            {
                "title": "沪深300股指期货(IF2312) 关键点位分析与操作建议",
                "contract_code": "IF2312",
                "stop_loss": 3520.0,
                "take_profit": 3620.0,
                "current_price": 3550.0,
                "suggestion": "建议在3550-3560区间分批尝试建立多单，止损位严格设置在3520下方",
                "content": """今日沪深300股指期货(IF2312)早盘小幅低开后震荡上行，目前站稳3550一线。

从技术面来看：
1. 日线级别MACD指标出现底部金叉，红柱开始放出，显示反弹动能增强。
2. KDJ指标在超卖区域形成金叉向上发散。
3. 30分钟级别突破下行趋势线压制。

基本面方面：
近期宏观政策利好频出，市场情绪有所回暖，北向资金出现净流入迹象。

操作建议：
建议激进投资者在3550-3560区间分批尝试建立多单。
止损位严格设置在3520下方。
第一目标位看至3620附近，若突破可进一步上看3650。

风险提示：
需关注午后成交量配合情况，若成交量无法有效放大，可能面临冲高回落风险。""",
            },
            {
                "title": "螺纹钢 RB2401 震荡下行趋势确立",
                "contract_code": "RB2401",
                "stop_loss": 3850.0,
                "take_profit": 3750.0,
                "current_price": 3800.0,
                "suggestion": "建议在3800附近建立空单，止损设置在3850上方，目标位3750",
                "content": """螺纹钢主力合约RB2401近期呈现震荡下行格局，技术面偏弱。

技术分析：
1. 日线级别均线系统呈现空头排列，5日均线压制明显。
2. 成交量持续萎缩，市场参与度不高。
3. 下方关键支撑位在3750附近，若跌破可能加速下行。

基本面分析：
钢材库存持续累积，下游需求疲软，现货价格承压。
钢厂开工率维持高位，供应压力较大。

操作策略：
建议在3800附近建立空单，止损设置在3850上方。
第一目标位3750，若有效跌破可继续持有至3700附近。

风险控制：
严格控制仓位，设置止损，避免逆势加仓。""",
            },
            {
                "title": "黄金 AU2402 避险情绪升温",
                "contract_code": "AU2402",
                "stop_loss": 485.0,
                "take_profit": 510.0,
                "current_price": 495.0,
                "suggestion": "建议在495附近建立多单，止损设置在485下方，目标位510",
                "content": """黄金期货AU2402合约受避险情绪推动，近期表现强势。

市场环境：
1. 国际地缘政治风险上升，避险资产受到追捧。
2. 美元指数走弱，利好黄金价格。
3. 通胀预期升温，黄金作为保值工具需求增加。

技术面分析：
1. 日线级别突破前期高点，形成上升趋势。
2. 成交量放大，资金流入明显。
3. 技术指标显示多头动能强劲。

操作建议：
建议在495附近建立多单，止损设置在485下方。
第一目标位510，若突破可继续持有至520附近。

注意事项：
关注国际金价走势和美元指数变化，及时调整仓位。""",
            },
            {
                "title": "铜 CU2401 震荡整理，等待方向选择",
                "contract_code": "CU2401",
                "stop_loss": 68500.0,
                "take_profit": 70500.0,
                "current_price": 69500.0,
                "suggestion": "建议在69500附近轻仓试多，止损设置在68500下方，目标位70500",
                "content": """沪铜主力合约CU2401近期在69000-70000区间震荡整理。

市场分析：
1. 宏观面多空交织，市场观望情绪浓厚。
2. 库存水平处于历史低位，对价格形成支撑。
3. 下游需求恢复缓慢，限制价格上涨空间。

技术形态：
1. 日线级别在关键支撑位69000附近获得支撑。
2. 成交量萎缩，市场等待方向选择。
3. 若突破70000阻力位，可能开启新一轮上涨。

交易策略：
建议在69500附近轻仓试多，止损设置在68500下方。
若有效突破70000，可加仓持有，目标位70500。

风险提示：
当前处于震荡区间，建议控制仓位，避免重仓操作。""",
            },
            {
                "title": "原油 SC2401 供需平衡，区间震荡",
                "contract_code": "SC2401",
                "stop_loss": 520.0,
                "take_profit": 560.0,
                "current_price": 540.0,
                "suggestion": "建议在540附近建立多单，止损设置在520下方，目标位560",
                "content": """上海原油期货SC2401合约近期在520-560区间震荡运行。

基本面分析：
1. OPEC+减产政策对市场形成支撑。
2. 全球经济复苏预期提振需求。
3. 美国原油库存下降，供应端偏紧。

技术面：
1. 日线级别在520附近获得强支撑。
2. 上方560阻力位压力较大。
3. 若突破560，可能开启新一轮上涨。

操作建议：
建议在540附近建立多单，止损设置在520下方。
第一目标位560，若突破可继续持有。

风险控制：
关注国际油价走势和地缘政治风险，及时调整策略。""",
            },
        ]
        
        print(f"开始创建 {len(sample_posts)} 个样例帖子...")
        print()
        
        created_count = 0
        for i, post_data in enumerate(sample_posts, 1):
            try:
                post = post_service.create_post(
                    author_id=admin_user.user_id,
                    title=post_data["title"],
                    contract_code=post_data["contract_code"],
                    stop_loss=post_data["stop_loss"],
                    take_profit=post_data.get("take_profit"),
                    current_price=post_data.get("current_price"),
                    suggestion=post_data.get("suggestion"),
                    content=post_data["content"],
                )
                created_count += 1
                print(f"✓ [{i}/{len(sample_posts)}] 创建成功: {post.title}")
                print(f"  合约代码: {post.contract_code}, 止损: {post.stop_loss}, 止盈: {post.take_profit}")
                print()
            except Exception as e:
                print(f"✗ [{i}/{len(sample_posts)}] 创建失败: {post_data['title']}")
                print(f"  错误: {str(e)}")
                print()
        
        print("=" * 80)
        print(f"完成！成功创建 {created_count} 个样例帖子")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 80)
    print("创建样例帖子数据")
    print("=" * 80)
    print()
    create_sample_posts()


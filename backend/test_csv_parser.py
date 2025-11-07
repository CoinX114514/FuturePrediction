"""测试CSV解析器。

使用LULU_daily.csv文件测试CSV解析功能。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.csv_parser import CSVParser


def test_lulu_csv():
    """测试解析LULU_daily.csv文件。"""
    print("=" * 80)
    print("CSV解析器测试 - LULU_daily.csv")
    print("=" * 80)
    
    # CSV文件路径
    csv_file_path = "LULU_daily.csv"
    
    if not os.path.exists(csv_file_path):
        print(f"错误：文件 {csv_file_path} 不存在")
        return
    
    # 读取文件
    print(f"\n1. 读取文件: {csv_file_path}")
    with open(csv_file_path, "rb") as f:
        file_contents = f.read()
    print(f"   文件大小: {len(file_contents)} 字节")
    
    # 创建解析器
    print("\n2. 创建CSV解析器")
    parser = CSVParser()
    
    # 解析CSV
    print("\n3. 解析CSV文件...")
    try:
        df = parser.parse_csv(file_contents)
        print(f"   ✓ 解析成功！")
        print(f"   总行数: {len(df)}")
        print(f"   列名: {df.columns.tolist()}")
    except Exception as e:
        print(f"   ✗ 解析失败: {e}")
        return
    
    # 显示前几行数据
    print("\n4. 前5行数据（CSV原始顺序）:")
    print("-" * 80)
    for idx, row in df.head(5).iterrows():
        print(f"   行 {idx + 1}: 日期={row['日期']}, 开盘={row['开盘']}, 收盘={row['收盘']}")
    
    # 显示后几行数据
    print("\n5. 后5行数据（CSV原始顺序）:")
    print("-" * 80)
    for idx, row in df.tail(5).iterrows():
        print(f"   行 {idx + 1}: 日期={row['日期']}, 开盘={row['开盘']}, 收盘={row['收盘']}")
    
    # 检查日期顺序
    print("\n6. 检查日期顺序:")
    print("-" * 80)
    dates = df['日期'].tolist()
    first_date = dates[0] if dates else None
    last_date = dates[-1] if dates else None
    print(f"   第一行日期: {first_date}")
    print(f"   最后一行日期: {last_date}")
    
    # 检查数据完整性
    print("\n7. 数据完整性检查:")
    print("-" * 80)
    print(f"   总行数: {len(df)}")
    print(f"   缺失值统计:")
    print(f"     日期: {df['日期'].isna().sum()} 个缺失")
    print(f"     开盘: {df['开盘'].isna().sum()} 个缺失")
    print(f"     最高: {df['最高'].isna().sum()} 个缺失")
    print(f"     最低: {df['最低'].isna().sum()} 个缺失")
    print(f"     收盘: {df['收盘'].isna().sum()} 个缺失")
    print(f"     成交量: {df['成交量'].isna().sum()} 个缺失")
    
    # 显示数据范围
    print("\n8. 数据范围:")
    print("-" * 80)
    print(f"   开盘价范围: {df['开盘'].min():.2f} - {df['开盘'].max():.2f}")
    print(f"   收盘价范围: {df['收盘'].min():.2f} - {df['收盘'].max():.2f}")
    print(f"   最高价范围: {df['最高'].min():.2f} - {df['最高'].max():.2f}")
    print(f"   最低价范围: {df['最低'].min():.2f} - {df['最低'].max():.2f}")
    # 成交量可能是字符串格式，需要转换
    try:
        volume_min = df['成交量'].astype(str).str.replace(',', '').astype(float).min()
        volume_max = df['成交量'].astype(str).str.replace(',', '').astype(float).max()
        print(f"   成交量范围: {volume_min:,.0f} - {volume_max:,.0f}")
    except:
        print(f"   成交量范围: 无法计算（可能是字符串格式）")
    
    # 转换为字典列表（模拟后端返回格式）
    print("\n9. 转换为字典列表（模拟后端返回格式）:")
    print("-" * 80)
    data_records = []
    for _, row in df.iterrows():
        # 处理成交量：可能是字符串格式（带逗号），需要转换
        volume = row["成交量"]
        if isinstance(volume, str):
            # 移除逗号和引号并转换为浮点数
            volume = float(volume.replace(',', '').replace('"', ''))
        else:
            volume = float(volume)
        
        record = {
            "日期": str(row["日期"]),
            "开盘": float(row["开盘"]),
            "最高": float(row["最高"]),
            "最低": float(row["最低"]),
            "收盘": float(row["收盘"]),
            "成交量": volume,
        }
        data_records.append(record)
    
    print(f"   转换成功，共 {len(data_records)} 条记录")
    print(f"\n   前3条记录:")
    for i, record in enumerate(data_records[:3], 1):
        print(f"     {i}. {record}")
    
    print(f"\n   后3条记录:")
    for i, record in enumerate(data_records[-3:], 1):
        print(f"     {i}. {record}")
    
    # 测试取前100条的逻辑（CSV是从新到旧，所以前100条是最新的）
    print("\n10. 测试取前100条数据（前端逻辑 - 最新的100条）:")
    print("-" * 80)
    recent_100 = data_records[:100] if len(data_records) >= 100 else data_records
    print(f"   取前100条（最新的）: 共 {len(recent_100)} 条")
    if recent_100:
        print(f"   第一条日期（最新）: {recent_100[0]['日期']}")
        print(f"   最后一条日期（第100条）: {recent_100[-1]['日期']}")
        print(f"\n   反转后（从早到晚，用于图表）:")
        reversed_100 = recent_100[::-1]
        print(f"   第一条日期（最早）: {reversed_100[0]['日期']}")
        print(f"   最后一条日期（最新）: {reversed_100[-1]['日期']}")
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)


if __name__ == "__main__":
    test_lulu_csv()


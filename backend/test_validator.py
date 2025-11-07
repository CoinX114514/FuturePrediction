"""测试数据验证器。

验证CSV解析和数据验证是否正确处理带逗号的成交量数据。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.csv_parser import CSVParser
from app.services.data_validator import DataValidator


def test_lulu_validation():
    """测试LULU_daily.csv的解析和验证。"""
    print("=" * 80)
    print("测试CSV解析和数据验证")
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
    
    # 解析CSV
    print("\n2. 解析CSV文件...")
    parser = CSVParser()
    try:
        df = parser.parse_csv(file_contents)
        print(f"   ✓ 解析成功！")
        print(f"   总行数: {len(df)}")
        print(f"   列名: {df.columns.tolist()}")
        
        # 检查成交量列
        if "成交量" in df.columns:
            print(f"\n   成交量列信息:")
            print(f"     类型: {df['成交量'].dtype}")
            print(f"     前5个值: {df['成交量'].head().tolist()}")
            print(f"     是否有逗号: {df['成交量'].astype(str).str.contains(',').any()}")
        else:
            print(f"   ✗ 未找到'成交量'列")
            print(f"   可用列: {df.columns.tolist()}")
    except Exception as e:
        print(f"   ✗ 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 验证数据
    print("\n3. 验证数据...")
    validator = DataValidator()
    try:
        validation_result = validator.validate_ohlcv(df)
        
        print(f"   验证结果: {'✓ 通过' if validation_result['valid'] else '✗ 失败'}")
        
        if validation_result['errors']:
            print(f"\n   错误 ({len(validation_result['errors'])} 个):")
            for error in validation_result['errors']:
                print(f"     - {error}")
        
        if validation_result['warnings']:
            print(f"\n   警告 ({len(validation_result['warnings'])} 个):")
            for warning in validation_result['warnings']:
                print(f"     - {warning}")
        
        # 检查成交量列转换后的值
        if "成交量" in df.columns:
            print(f"\n   成交量列转换后:")
            print(f"     类型: {df['成交量'].dtype}")
            print(f"     缺失值数量: {df['成交量'].isna().sum()}")
            print(f"     前5个值: {df['成交量'].head().tolist()}")
            print(f"     最小值: {df['成交量'].min()}")
            print(f"     最大值: {df['成交量'].max()}")
        
    except Exception as e:
        print(f"   ✗ 验证失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    test_lulu_validation()


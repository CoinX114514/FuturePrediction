"""排查铁矿石等合约现价为空：测试 Tushare 是否返回 I2603 数据。

若输出「您的token不对，请确认」：说明是 Tushare Token 未配置或无效，
不是 Tushare 没有铁矿石数据。请设置有效 TUSHARE_TOKEN 后再试。
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载 .env 中的 TUSHARE_TOKEN（若存在）
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
except ImportError:
    pass

from datetime import datetime

def main():
    from app.services.tushare_service import TushareService
    
    ts_svc = TushareService()
    contract_code = "I2603"
    
    print("=== 1. 按 ts_code 单独查询（I2603.DCE）===")
    ts_code = ts_svc.convert_contract_code_to_ts_code(contract_code)
    print(f"  ts_code = {ts_code}")
    
    df = ts_svc.get_futures_daily(ts_code=ts_code)
    if df is not None and not df.empty:
        print(f"  返回行数: {len(df)}")
        print(df.head().to_string())
        close = df.iloc[0].get('close') if 'close' in df.columns else None
        print(f"  收盘价: {close}")
    else:
        print("  无数据（若日志有「您的token不对」则为 Token 未配置或无效，请设置 TUSHARE_TOKEN）")
    
    print("\n=== 2. 不传 ts_code，拉全量当日行情 ===")
    df_all = ts_svc.get_futures_daily()
    if df_all is not None and not df_all.empty:
        print(f"  全量返回行数: {len(df_all)}")
        # 检查是否包含铁矿石
        mask = df_all['ts_code'].astype(str).str.contains('I2603', na=False)
        found = df_all[mask]
        if not found.empty:
            print(f"  包含 I2603 的行: {len(found)}")
            print(found[['ts_code', 'close', 'settle']].head().to_string())
        else:
            print("  全量结果中不包含 I2603（可能被条数截断或当日无该合约数据）")
    else:
        print("  全量无数据")
    
    print("\n=== 3. 直接调 get_futures_price('I2603') ===")
    price = ts_svc.get_futures_price(contract_code)
    print(f"  结果: {price}")


if __name__ == "__main__":
    main()

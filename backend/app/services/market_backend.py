"""统一选择行情数据源：Tushare 或本地 JSON。

设计原因：
- 生产环境标配 TUSHARE_TOKEN 时，K 线/现价应走 Tushare；若仍默认 json，会出现「本机直连 fut_daily 有数据、线上 K 线 404」。
- 仅当显式 ``MARKET_DATA_SOURCE=json`` 时强制本地 JSON（离线/合规场景）。
- 显式 ``MARKET_DATA_SOURCE=tushare`` 或「未设 mode 但已配置 Token」时用 Tushare；初始化失败回退 JSON。
"""

import logging
import os

logger = logging.getLogger(__name__)


def get_market_backend():
    """返回行情后端（与 MarketDataService / TushareService 方法兼容）。

    - ``MARKET_DATA_SOURCE=json``：始终本地 JSON。
    - ``MARKET_DATA_SOURCE=tushare``：尝试 Tushare，失败回退 JSON。
    - 未设置或为空：若存在非空 ``TUSHARE_TOKEN`` 则优先 Tushare，否则 JSON。

    Returns:
        MarketDataService | TushareService: 行情实现。
    """
    mode = (os.getenv("MARKET_DATA_SOURCE") or "").strip().lower()
    token = (os.getenv("TUSHARE_TOKEN") or "").strip()

    if mode == "json":
        from app.services.market_data_service import MarketDataService

        logger.info("[行情] 显式指定数据源=本地 JSON")
        return MarketDataService()

    use_tushare = mode == "tushare" or (not mode and bool(token))
    if use_tushare:
        try:
            from app.services.tushare_service import TushareService

            backend = TushareService()
            logger.info("[行情] 数据源=Tushare（MARKET_DATA_SOURCE=%r，Token已配置=%s）", mode or "(未设)", bool(token))
            return backend
        except Exception as e:
            logger.warning("[行情] Tushare 不可用，回退 JSON: %s", e)

    from app.services.market_data_service import MarketDataService

    logger.info("[行情] 数据源=本地 JSON（无可用 Tushare）")
    return MarketDataService()

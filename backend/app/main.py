"""FastAPI 主应用入口。

此模块包含 FastAPI 应用的配置和路由定义。
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import (
    auth,
    posts,
    drafts,
    collections,
    browse_history,
    admin_users,
    price_update,
    futures_sync,
    kline,
)

# 创建 FastAPI 应用实例
# 使用中文描述和标签以便于API文档显示
app = FastAPI(
    title="期货价格趋势预测 API",
    description="基于信号流的期货交易建议平台",
    version="0.2.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# 配置 CORS 中间件，允许前端跨域请求
# 在生产环境中，由于使用 Nginx 反向代理，所有请求都来自同一个源（Nginx）
# 因此允许所有来源是安全的（实际上请求已经通过 Nginx 代理）
import os

# 从环境变量读取允许的来源，如果没有设置则允许所有来源
# 开发环境可以设置特定来源，生产环境通过 Nginx 代理时允许所有来源
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # 生产环境通过 Nginx 代理，允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["用户认证"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["帖子"])
app.include_router(drafts.router, prefix="/api/v1/drafts", tags=["草稿"])
app.include_router(collections.router, prefix="/api/v1/collections", tags=["收藏"])
app.include_router(browse_history.router, prefix="/api/v1/browse-history", tags=["浏览历史"])
app.include_router(admin_users.router, prefix="/api/v1", tags=["管理员"])
app.include_router(price_update.router, prefix="/api/v1/price-update", tags=["价格更新"])
app.include_router(kline.router, prefix="/api/v1/kline", tags=["K线数据"])
app.include_router(futures_sync.router, prefix="/api/v1/futures-sync", tags=["期货合约同步"])


@app.get("/")
async def root():
    """根路径健康检查端点。

    Returns:
        dict: 包含 API 状态信息的字典。
    """
    return {"message": "期货价格趋势预测 API 服务运行中", "status": "healthy"}


@app.get("/api/health")
async def health_check():
    """健康检查端点。

    Returns:
        dict: 包含服务健康状态的字典。
    """
    return {"status": "healthy", "service": "期货价格趋势预测 API"}


@app.on_event("startup")
async def startup_event():
    """应用启动时执行。

    启动定时任务调度器并添加价格更新任务。
    所有初始化操作都在后台线程中执行，确保不阻塞服务器启动。
    """
    import os
    import logging
    import threading
    import time
    from app.services.scheduler_service import scheduler_service
    from app.services.price_update_service import PriceUpdateService

    logger = logging.getLogger(__name__)
    
    def init_scheduler_tasks():
        """在后台线程中初始化定时任务，避免阻塞服务器启动。"""
        try:
            # 从环境变量读取更新间隔（分钟），默认 5 分钟（与前端轮询一致，同步现价到主页与详情）
            update_interval = int(os.getenv("PRICE_UPDATE_INTERVAL_MINUTES", "5"))
            
            # 定义价格更新任务函数
            def update_prices_job():
                """价格更新任务函数。"""
                import datetime
                start_time = datetime.datetime.now()
                logger.info(f"[定时任务] 开始执行价格更新任务，时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                try:
                    # 创建数据库会话
                    from app.database.connection import SessionLocal
                    db = SessionLocal()
                    try:
                        price_service = PriceUpdateService(db)
                        result = price_service.update_all_posts_price()
                        
                        end_time = datetime.datetime.now()
                        duration = (end_time - start_time).total_seconds()
                        
                        logger.info(f"[定时任务] 价格更新完成: 总数={result['total']}, 成功={result['success']}, 失败={result['failed']}, 耗时={duration:.2f}秒")
                        
                        if result.get('error'):
                            logger.error(f"[定时任务] 更新过程中出现错误: {result['error']}")
                    finally:
                        db.close()
                except Exception as e:
                    end_time = datetime.datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    logger.error(f"[定时任务] 价格更新任务失败，耗时={duration:.2f}秒: {str(e)}", exc_info=True)
            
            # 启动调度器
            scheduler_service.start()
            
            # 添加价格更新任务
            try:
                scheduler_service.add_price_update_job(
                    update_func=update_prices_job,
                    interval_minutes=update_interval,
                    job_id="price_update_job"
                )
                logger.info(f"已启动价格更新定时任务，更新间隔: {update_interval} 分钟（现价同步到 DB，主页/详情/K 线图通过接口获取）")
                
                # 启动后立即执行一次价格更新（异步执行，不阻塞启动）
                logger.info("启动后立即执行首次价格更新（异步执行）...")
                
                def run_initial_update():
                    """在后台线程中执行首次价格更新。"""
                    try:
                        # 等待 2 秒，确保服务器完全启动
                        time.sleep(2)
                        update_prices_job()
                    except Exception as e:
                        logger.warning(f"首次价格更新失败（不影响后续定时任务）: {str(e)}")
                
                # 在后台线程中执行，不阻塞主线程
                update_thread = threading.Thread(target=run_initial_update, daemon=True)
                update_thread.start()
                logger.info("首次价格更新任务已在后台线程中启动")
            except Exception as e:
                logger.error(f"启动价格更新定时任务失败: {str(e)}", exc_info=True)
            
            # 添加期货合约同步任务（每天执行一次，在凌晨 2 点）
            try:
                from app.services.futures_sync_service import FuturesSyncService
                from apscheduler.triggers.cron import CronTrigger
                
                def sync_futures_job():
                    """期货合约同步任务函数。"""
                    import datetime
                    start_time = datetime.datetime.now()
                    logger.info(f"[定时任务] 开始执行期货合约同步任务，时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    try:
                        # 创建数据库会话
                        from app.database.connection import SessionLocal
                        from app.database.models import User
                        
                        db = SessionLocal()
                        try:
                            # 获取系统管理员用户（user_role >= 3）
                            admin_user = db.query(User).filter(User.user_role >= 3).first()
                            if not admin_user:
                                logger.error("[定时任务] 未找到管理员用户，无法执行期货合约同步")
                                return
                            
                            sync_service = FuturesSyncService(db)
                            result = sync_service.sync_futures_to_posts(
                                author_id=admin_user.user_id,
                                update_existing=False  # 只创建新合约，不更新已存在的
                            )
                            
                            end_time = datetime.datetime.now()
                            duration = (end_time - start_time).total_seconds()
                            
                            logger.info(
                                f"[定时任务] 期货合约同步完成: "
                                f"总数={result['total']}, "
                                f"创建={result['created']}, "
                                f"跳过={result['skipped']}, "
                                f"失败={result['failed']}, "
                                f"耗时={duration:.2f}秒"
                            )
                        finally:
                            db.close()
                    except Exception as e:
                        end_time = datetime.datetime.now()
                        duration = (end_time - start_time).total_seconds()
                        logger.error(f"[定时任务] 期货合约同步任务失败，耗时={duration:.2f}秒: {str(e)}", exc_info=True)
                
                # 每天凌晨 2 点执行一次
                scheduler_service.scheduler.add_job(
                    func=sync_futures_job,
                    trigger=CronTrigger(hour=2, minute=0),
                    id="futures_sync_job",
                    name="期货合约同步任务",
                    replace_existing=True,
                )
                logger.info("已启动期货合约同步定时任务，每天凌晨 2 点执行")
            except Exception as e:
                logger.error(f"启动期货合约同步定时任务失败: {str(e)}", exc_info=True)
            
            # 添加合约到期汰换任务（每天执行一次，在凌晨 3 点）
            try:
                from app.services.contract_expiry_service import ContractExpiryService
                from apscheduler.triggers.cron import CronTrigger
                
                def cleanup_expired_contracts_job():
                    """合约到期汰换任务函数。"""
                    import datetime
                    start_time = datetime.datetime.now()
                    logger.info(f"[定时任务] 开始执行合约到期汰换任务，时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    
                    try:
                        # 创建数据库会话
                        from app.database.connection import SessionLocal
                        
                        db = SessionLocal()
                        try:
                            expiry_service = ContractExpiryService(db)
                            result = expiry_service.cleanup_expired_contracts()
                            
                            end_time = datetime.datetime.now()
                            duration = (end_time - start_time).total_seconds()
                            
                            logger.info(
                                f"[定时任务] 合约到期汰换完成: "
                                f"检查总数={result['total_checked']}, "
                                f"到期数量={result['expired_count']}, "
                                f"删除数量={result['deleted_count']}, "
                                f"错误数量={result.get('error_count', 0)}, "
                                f"耗时={duration:.2f}秒"
                            )
                        finally:
                            db.close()
                    except Exception as e:
                        end_time = datetime.datetime.now()
                        duration = (end_time - start_time).total_seconds()
                        logger.error(f"[定时任务] 合约到期汰换任务失败，耗时={duration:.2f}秒: {str(e)}", exc_info=True)
                
                # 每天凌晨 3 点执行一次
                scheduler_service.scheduler.add_job(
                    func=cleanup_expired_contracts_job,
                    trigger=CronTrigger(hour=3, minute=0),
                    id="contract_expiry_cleanup_job",
                    name="合约到期汰换任务",
                    replace_existing=True,
                )
                logger.info("已启动合约到期汰换定时任务，每天凌晨 3 点执行")
            except Exception as e:
                logger.error(f"启动合约到期汰换定时任务失败: {str(e)}", exc_info=True)
        except Exception as e:
            logger.error(f"初始化定时任务时发生错误: {str(e)}", exc_info=True)
        
        # 在后台线程中执行所有初始化操作，确保不阻塞服务器启动
        init_thread = threading.Thread(target=init_scheduler_tasks, daemon=True)
        init_thread.start()
        logger.info("定时任务初始化已在后台线程中启动，服务器可以立即响应请求")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行。

    停止定时任务调度器。
    """
    import logging
    from app.services.scheduler_service import scheduler_service

    logger = logging.getLogger(__name__)
    
    # 停止调度器
    try:
        scheduler_service.stop()
        logger.info("定时任务调度器已停止")
    except Exception as e:
        logger.error(f"停止定时任务调度器失败: {str(e)}", exc_info=True)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器。

    捕获所有未处理的异常并返回友好的错误响应。
    确保错误响应也包含 CORS 头。

    Args:
        request: FastAPI 请求对象。
        exc: 异常对象。

    Returns:
        JSONResponse: 包含错误信息的 JSON 响应。
    """
    import traceback
    # 记录详细错误信息（在生产环境中应该记录到日志文件）
    print(f"全局异常处理器捕获错误: {type(exc).__name__}: {str(exc)}")
    traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "服务器内部错误",
            "message": str(exc),
            "detail": "请检查您的请求格式或联系管理员",
        },
        headers={
            "Access-Control-Allow-Origin": "*",  # 生产环境通过 Nginx 代理，允许所有来源
            "Access-Control-Allow-Credentials": "true",
        },
    )


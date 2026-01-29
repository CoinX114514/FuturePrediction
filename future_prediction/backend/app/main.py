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
# 在生产环境中应该限制允许的源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite 默认端口
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
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Credentials": "true",
        },
    )


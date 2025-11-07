#!/usr/bin/env python3
"""后端服务器启动脚本。

使用此脚本启动 FastAPI 开发服务器。
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发模式：自动重载
        log_level="info",
    )


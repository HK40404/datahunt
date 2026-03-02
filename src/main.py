"""
FastAPI 应用入口
"""
import logging

from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import PROJECT_LOGGER_NAME

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

# 初始化限流器
limiter = Limiter(key_func=get_remote_address)


def create_app() -> FastAPI:
    """创建 FastAPI 应用"""
    app = FastAPI(
        title="DataHunt API",
        description="Text-to-SQL API based on LangGraph",
        version="0.1.0",
    )

    # 添加限流器到 app state
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        """处理限流异常"""
        return {"error": "Too Many Requests", "detail": str(exc)}

    # 注册路由（延迟导入避免循环依赖）
    from api.query import router as query_router

    app.include_router(query_router, tags=["query"])

    @app.get("/health")
    async def health_check():
        """健康检查端点"""
        return {"status": "ok"}

    return app


# 创建应用实例
app = create_app()

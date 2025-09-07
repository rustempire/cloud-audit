import os
import time
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    lifespan = logging.getLogger("lifespan")

    # 记录应用的启动时间
    starting = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    lifespan.info(f"Application is starting at {starting}")

    # 记录环境变量的信息
    lifespan.info("Registered environments:")
    envs = {
        "PORT": os.getenv("PORT", "8000"),
        "CONSOLE_LOG_LEVEL": os.getenv("CONSOLE_LOG_LEVEL", "INFO"),
        "STORAGE_LOG_LEVEL": os.getenv("STORAGE_LOG_LEVEL", "DEBUG"),
        "LOG_BACKUP_COUNTS": os.getenv("LOG_BACKUP_COUNTS", "7"),
        "ROOT_LOG_LEVEL": os.getenv("ROOT_LOG_LEVEL", "DEBUG"),
        "LIFESPAN_LOG_LEVEL": os.getenv("LIFESPAN_LOG_LEVEL", "INFO"),
        "UVICORN_ERROR_LOG_LEVEL": os.getenv("UVICORN_ERROR_LOG_LEVEL", "ERROR"),
        "UVICORN_ACCESS_LOG_LEVEL": os.getenv("UVICORN_ACCESS_LOG_LEVEL", "INFO"),
    }
    for key, value in envs.items():
        lifespan.info(f">>> {key}: {value}")

    # 记录已加载的中间件
    lifespan.info("Registered middlewares:")
    for middleware in app.user_middleware:
        lifespan.info(f">>> {middleware.cls.__name__}")

    # 记录注册的路由信息
    lifespan.info("Registered routes:")
    for route in app.routes:
        path = getattr(route, "path", None)
        methods = getattr(route, "methods", None)
        if path and methods:
            lifespan.info(f">>> {', '.join(methods)} {path}")

    # 应用运行期间上下文
    yield

    # 记录应用的关闭时间
    shutting = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    lifespan.info(f"Application is shutting down at {shutting}")

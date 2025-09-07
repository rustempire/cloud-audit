import contextvars
import sys
from datetime import datetime
from pathlib import Path

from loguru import logger

request_context_ctx = contextvars.ContextVar("request_context", default={})


class RequestContextFilter:
    def __call__(self, record):
        # 获取请求上下文
        context = request_context_ctx.get()

        # 设置默认值
        record["extra"]["request_id"] = context.get("request_id", "-")
        record["extra"]["client_ip"] = context.get("client_ip", "-")
        record["extra"]["method"] = context.get("method", "-")
        record["extra"]["path"] = context.get("path", "-")
        record["extra"]["status_code"] = context.get("status_code", "-")
        record["extra"]["duration"] = context.get("duration", "-")

        return record


def init_logging(log_path, stdout_level, filewt_level):
    logger.remove()

    log_path = Path(log_path)
    log_path.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    logger.add(
        sys.stdout,
        colorize=True,
        level=stdout_level.upper(),
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "{message} | {extra}",
        filter=RequestContextFilter(),
    )

    logger.add(
        log_path / f"{today}.log",
        rotation="1 day",
        encoding="utf-8",
        level=filewt_level.upper(),
        enqueue=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "{message} | {extra}",
        filter=RequestContextFilter(),
    )

    return logger

import contextvars
import logging
import os

# 配置控制台日志级别
CONSOLE_LOG_LEVEL = os.getenv("CONSOLE_LOG_LEVEL", "INFO").upper()

# 配置存储日志级别
STORAGE_LOG_LEVEL = os.getenv("STORAGE_LOG_LEVEL", "INFO").upper()

# 配置日志备份数量
LOG_BACKUP_COUNTS = int(os.getenv("LOG_BACKUP_COUNTS", 7))

# 配置根日志级别
ROOT_LOG_LEVEL = os.getenv("ROOT_LOG_LEVEL", "DEBUG").upper()

# 配置生命周期日志级别
LIFESPAN_LOG_LEVEL = os.getenv("LIFESPAN_LOG_LEVEL", "INFO").upper()

# 配置Uvicorn错误日志的日志级别
UVICORN_ERROR_LOG_LEVEL = os.getenv("UVICORN_ERROR_LOG_LEVEL", "ERROR").upper()

# 配置Uvicorn访问日志的日志级别
UVICORN_ACCESS_LOG_LEVEL = os.getenv("UVICORN_ACCESS_LOG_LEVEL", "INFO").upper()

# 配置默认日志格式
DEFAULT_FORMATTER = (
    "%(asctime)s [%(levelname)s] "
    "RequestID:%(request_id)s | "
    "ClientIP:%(client_ip)s | "
    "Method:%(method)s | "
    "Path:%(path)s | "
    "ProcessID:%(process_id)s | "
    "UserAgent:%(user_agent)s | "
    "%(message)s"
)

request_context = contextvars.ContextVar("request_context", default={})


class DefaultFormatter(logging.Formatter):
    def format(self, record):
        record.process_id = getattr(record, "process_id", os.getpid())
        record.request_id = getattr(record, "request_id", "")
        record.client_ip = getattr(record, "client_ip", "")
        record.user_agent = getattr(record, "user_agent", "")
        record.method = getattr(record, "method", "")
        record.path = getattr(record, "path", "")
        return super().format(record)


class RequestContextFilter(logging.Filter):
    def filter(self, record):
        ctx = request_context.get()
        record.process_id = ctx.get("process_id", os.getpid())
        record.request_id = ctx.get("request_id", "")
        record.client_ip = ctx.get("client_ip", "")
        record.user_agent = ctx.get("user_agent", "")
        record.method = ctx.get("method", "")
        record.path = ctx.get("path", "")
        return True


log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": DefaultFormatter,
            "format": DEFAULT_FORMATTER,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "request_context": {
            "()": "logger.RequestContextFilter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": CONSOLE_LOG_LEVEL,
            "formatter": "default",
            "filters": ["request_context"],
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": STORAGE_LOG_LEVEL,
            "formatter": "default",
            "filters": ["request_context"],
            "filename": "logs/app.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": LOG_BACKUP_COUNTS,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "": {
            "level": ROOT_LOG_LEVEL,
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "lifespan": {
            "level": LIFESPAN_LOG_LEVEL,
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "uvicorn.error": {
            "level": UVICORN_ERROR_LOG_LEVEL,
            "handlers": ["file"],
            "filters": ["request_context"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": UVICORN_ACCESS_LOG_LEVEL,
            "handlers": [],
            "propagate": False,
        },
    },
}

import time
import uuid

from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from src.infrastructure.observability.logging import request_context_ctx


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 生成请求ID
        request_id = str(uuid.uuid4())

        # 获取客户端IP
        client_ip = self._get_client_ip(request)

        # 设置初始请求上下文
        context = {
            "request_id": request_id,
            "client_ip": client_ip,
            "method": request.method,
            "path": str(request.url.path),
            "status_code": "",
            "duration": "",
        }

        request_context_ctx.set(context)

        logger.info("HTTP REQUEST - START")

        start_time = time.time()

        try:
            response = await call_next(request)
            duration = (time.time() - start_time) * 1000
            context["status_code"] = response.status_code
            context["duration"] = f"{duration:.2f}ms"
            logger.info("HTTP REQUEST - DONE")
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            context["status_code"] = 500
            context["duration"] = f"{duration:.2f}ms"
            logger.error("HTTP REQUEST - FAIL", extra={"error": str(e)})
            raise

    def _get_client_ip(self, request):
        """获取客户端IP"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"

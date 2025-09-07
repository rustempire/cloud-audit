from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


class HttpException(HTTPException):
    def __init__(self, status_code: int, error: str, message: str, data=None):
        self.error = error
        self.message = message
        self.data = data or {}

        super().__init__(status_code=status_code, detail=message)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(HttpException)
    async def http_exception_handler(request: Request, exc: HttpException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "error": exc.error,
                "message": exc.message,
                "data": exc.data,
            },
        )

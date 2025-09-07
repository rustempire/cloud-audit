import uvicorn
from fastapi import FastAPI
from src.infrastructure.middleware.request_logger import RequestLoggerMiddleware
from src.presentation.http.controller.embedding import router
from src.presentation.http.error import register_exception_handlers

app = FastAPI()
app.add_middleware(RequestLoggerMiddleware)
register_exception_handlers(app)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=80, access_log=False)

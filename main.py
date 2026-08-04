import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.home.router import router as home_router
from api.users.router import router as users_router
from config import FAKE_ACCESS_TOKEN
from database import Base, engine
from exceptions import APIException, ErrorCode, api_exception_handler, validation_exception_handler

# 啟動時確保資料表存在（users router 的 import chain 已經讓 UserORM 註冊到 Base.metadata）
Base.metadata.create_all(bind=engine)

description = """
## 詳細說明
測試如何用Python撰寫API，然後產生出像樣的文件
"""

app = FastAPI(title= "FastAPI Test", version="1.0.0", description= description)

PUBLIC_PATHS = {"/", "/docs", "/redoc", "/openapi.json"}


@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    if request.url.path not in PUBLIC_PATHS:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.removeprefix("Bearer ").strip()
        if token != FAKE_ACCESS_TOKEN:
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "code": ErrorCode.UNAUTHORIZED.code_num,
                        "code_name": ErrorCode.UNAUTHORIZED.label,
                        "message": "Access Token 無效或未提供",
                    }
                },
            )
    return await call_next(request)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    print(f"{request.method} {request.url.path} - {response.status_code} - {duration:.1f}ms")
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home_router)
app.include_router(users_router)

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

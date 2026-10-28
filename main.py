import time

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.auth.router import router as auth_router
from api.home.router import router as home_router
from api.users.router import router as users_router
from api.orders.router import router as orders_router
from api.ws.router import router as ws_router
from api.redis_task.router import router as redis_task_router
from auth import decode_access_token
from database import Base, engine
from exceptions import APIException, ErrorCode, api_exception_handler, validation_exception_handler

# fastapi dev main.py 
# 它會啟動一個由 Uvicorn 驅動的伺服器，並且預設開啟 auto-reload 功能，也就是當你修改並儲存 main.py 檔案時，伺服器會自動重啟載入最新的程式碼，非常方便。
# ---------------------------------------------
# 啟動時確保資料表存在（auth/users router 的 import chain 已經讓 AccountORM、UserORM 註冊到 Base.metadata）
Base.metadata.create_all(bind=engine)

description = """
## 詳細說明
測試如何用Python撰寫API，然後產生出像樣的文件
"""

app = FastAPI(title= "FastAPI Test", version="1.0.0", description= description)

# 不需要帶token的路徑
PUBLIC_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/auth/register", "/auth/login", "/auth/all"}

# middleware 的本質是「攔截所有請求/回應」，本身是「所有請求都會經過的攔截層」，用途很廣，驗證只是常見的其中一種。
@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    if request.url.path not in PUBLIC_PATHS:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.removeprefix("Bearer ").strip()
        if decode_access_token(token) is None:
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

# middleware 的執行順序是「後寫的先執行」
# 註冊順序：CORSMiddleware > log_requests > verify_token_middleware
# 把CORS加在verify_token_middleware之前避免在送出preflight的時候沒帶token就被擋下來
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(ws_router)
app.include_router(redis_task_router)

app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

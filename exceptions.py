from enum import Enum

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ErrorCode(Enum):
    INVALID_AGE = (400001, "INVALID_AGE")

    UNAUTHORIZED = (401001, "UNAUTHORIZED")
    INVALID_CREDENTIALS = (401002, "INVALID_CREDENTIALS")

    FORBIDDEN = (403001, "FORBIDDEN")

    USER_NOT_FOUND = (404001, "USER_NOT_FOUND")
    ORDER_NOT_FOUND = (404002, "ORDER_NOT_FOUND")

    USER_ALREADY_EXISTS = (409001, "USER_ALREADY_EXISTS")
    USERNAME_ALREADY_EXISTS = (409002, "USERNAME_ALREADY_EXISTS")
    INVALID_ITEM_VOLUME = (409003, "INVALID_ITEM_VOLUME")

    VALIDATION_ERROR = (422001, "VALIDATION_ERROR")

    def __init__(self, code_num: int, label: str):
        self.code_num = code_num
        self.label = label


class APIException(Exception):
    def __init__(self, status_code: int, code: ErrorCode, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message


class Unauthorized(APIException):
    def __init__(self, message: str = "Access Token 無效或未提供"):
        super().__init__(401, ErrorCode.UNAUTHORIZED, message)


class Forbidden(APIException):
    def __init__(self, message: str = "無權存取此資源"):
        super().__init__(403, ErrorCode.FORBIDDEN, message)


async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code.code_num,
                "code_name": exc.code.label,
                "message": exc.message,
            }
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": ErrorCode.VALIDATION_ERROR.code_num,
                "code_name": ErrorCode.VALIDATION_ERROR.label,
                "message": "請求資料格式錯誤",
                "details": exc.errors(),
            }
        },
    )

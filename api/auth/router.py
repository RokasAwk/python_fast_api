from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import create_access_token
from database import get_db
from . import service
from .dependencies import get_current_account
from .exceptions import InvalidCredentials, UsernameAlreadyExists
from .models import AccountModel
from .schemas import LoginRequest, MeResponse, RegisterRequest, RegisterResponse, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    operation_id="register",
    summary="註冊帳號",
    description="建立一組登入用的帳號密碼，帳號不可重複。",
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if service.get_account_by_username(db, payload.username) is not None:
        raise UsernameAlreadyExists(payload.username)

    account = service.create_account(db, payload.username, payload.password)
    return {"message": "Success", "id": account.id, "username": account.username}


@router.post(
    "/login",
    response_model=TokenResponse,
    operation_id="login",
    summary="登入取得 access token",
    description="用帳號密碼登入，回傳可貼到 Swagger Authorize 使用的 JWT access token。",
)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    account = service.authenticate(db, payload.username, payload.password)
    if account is None:
        raise InvalidCredentials()

    access_token = create_access_token({"sub": str(account.id), "username": account.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=MeResponse,
    operation_id="get_current_account",
    summary="查詢目前登入的帳號",
    description="需要帶有效的 access token，回傳 token 對應的帳號身分。",
)
def me(current_account: AccountModel = Depends(get_current_account)):
    return {"id": current_account.id, "username": current_account.username}

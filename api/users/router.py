from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from config import security
from database import get_db
from . import service
from .dependencies import get_existing_user, get_existing_users
from .exceptions import InvalidAge, UserAlreadyExists
from .models import UserModel
from .schemas import CreateUserResponse, GetUserResponse, GetAllUserResponse, UpdateUserResponse, DeleteUserResponse, User

router = APIRouter(prefix="/user", tags=["Users"], dependencies=[Security(security)])


@router.post(
    "/create",
    response_model=CreateUserResponse,
    operation_id="create_user",
    summary="建立使用者",
    description="建立一個新的使用者，需要帶有效的 access token。若年齡為負數或姓名重複會回傳錯誤。",
)
def create_user(user: User, db: Session = Depends(get_db)):
    if user.age < 0:
        raise InvalidAge()

    if service.is_name_taken(db, user.name):
        raise UserAlreadyExists(user.name)

    created_user = service.create_user(db, user.name, user.age)
    return {
        "message": "Success",
        "id": created_user.id,
        "name": created_user.name,
        "age": created_user.age,
    }


@router.get(
    "/all",
    response_model=GetAllUserResponse,
    operation_id="get_users",
    summary="取得所有使用者",
    description="查詢所有使用者 id、姓名與年齡，需要帶有效的 access token。",
)
def get_users(users: list[UserModel] = Depends(get_existing_users)):
    return {"users": users}

@router.get(
    "/{user_id:int}",
    response_model=GetUserResponse,
    operation_id="get_user",
    summary="取得單一使用者",
    description="根據使用者 id 查詢姓名與年齡，需要帶有效的 access token。若 id 不存在會回傳 404。",
)
def get_user(user: UserModel = Depends(get_existing_user)):
    return {"id": user.id, "name": user.name, "age": user.age}


@router.post(
    "/update/{user_id:int}",
    response_model=UpdateUserResponse,
    operation_id="update_user",
    summary="更新使用者",
    description="更新既有的使用者資料，需要帶有效的 access token。若查無使用者、年齡為負數或姓名重複會回傳錯誤。",
)
def update_user(update_data: User, user: UserModel = Depends(get_existing_user), db: Session = Depends(get_db)):
    if update_data.age < 0:
        raise InvalidAge()

    if service.is_name_taken(db, update_data.name, exclude_id=user.id):
        raise UserAlreadyExists(update_data.name)

    updated_user = service.update_user(db, user.id, update_data.name, update_data.age)
    return {
        "message": "Success",
        "id": updated_user.id,
        "name": updated_user.name,
        "age": updated_user.age,
    }

@router.post(
    "/delete/{user_id:int}",
    response_model=DeleteUserResponse,
    operation_id="delete_user",
    summary="刪除單一使用者",
    description="根據使用者 id 刪除使用者，需要帶有效的 access token。若 id 不存在會回傳 404。",
)
def delete_user(user: UserModel = Depends(get_existing_user), db: Session = Depends(get_db)):
    service.update_user(db, id=user.id, isDel=1)
    return {"message": "Success",}

from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from . import service
from .exceptions import UserNotFound
from .models import UserModel


def get_existing_user(user_id: int, db: Session = Depends(get_db)) -> UserModel:
    user = service.get_user_by_id(db, user_id)
    if user is None:
        raise UserNotFound(user_id)
    return user


def get_existing_users(db: Session = Depends(get_db)) -> list[UserModel]:
    return service.get_all_users(db)

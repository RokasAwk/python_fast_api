from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from auth import decode_access_token
from config import security
from database import get_db
from exceptions import Unauthorized
from . import service
from .models import AccountModel


def get_current_account(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
    db: Session = Depends(get_db),
) -> AccountModel:
    if credentials is None:
        raise Unauthorized()

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise Unauthorized()

    try:
        account_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise Unauthorized()

    account = service.get_account_by_id(db, account_id)
    if account is None:
        raise Unauthorized()

    return AccountModel(id=account.id, username=account.username)

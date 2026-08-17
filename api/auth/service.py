from sqlalchemy.orm import Session

from auth import hash_password, verify_password
from .models import AccountModel, AccountORM


def _to_model(account: AccountORM) -> AccountModel:
    return AccountModel(id=account.id, username=account.username)


def get_account_by_username(db: Session, username: str) -> AccountORM | None:
    return db.query(AccountORM).filter(AccountORM.username == username).first()


def get_account_by_id(db: Session, account_id: int) -> AccountORM | None:
    return db.query(AccountORM).filter(AccountORM.id == account_id).first()


def create_account(db: Session, username: str, password: str) -> AccountModel:
    account = AccountORM(username=username, hashed_password=hash_password(password))
    db.add(account)
    db.commit() # 對資料庫做修改，最後要再補一行 db.commit() 才會生效
    db.refresh(account)
    return _to_model(account)


def authenticate(db: Session, username: str, password: str) -> AccountORM | None:
    account = get_account_by_username(db, username)
    if account is None or not verify_password(password, account.hashed_password):
        return None
    return account

def get_all_users(db: Session) -> list[AccountModel]:
    users = db.query(AccountORM).all()
    return [_to_model(user) for user in users]

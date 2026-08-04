from sqlalchemy.orm import Session

from .models import UserModel, UserORM


def _to_model(user: UserORM) -> UserModel:
    return UserModel(id=user.id, name=user.name, age=user.age, isDel=user.isDel)


def is_name_taken(db: Session, name: str, exclude_id: int | None = None) -> bool:
    # user.id != exclude_id只檢查非自己的名字，比對自己的新名字是否和其他人相同
    # 換句話說: 同名但那個人是你自己(id 相同)→ 放行;同名但那個人是別人(id 不同)
    # isDel != 1: 已刪除的使用者不算「名字被佔用」，允許新建同名資料
    query = db.query(UserORM).filter(UserORM.name == name, UserORM.isDel != 1)
    if exclude_id is not None:
        query = query.filter(UserORM.id != exclude_id)
    return db.query(query.exists()).scalar()


def create_user(db: Session, name: str, age: int) -> UserModel:
    user = UserORM(name=name, age=age, isDel=0)
    db.add(user)
    db.commit()
    db.refresh(user)
    return _to_model(user)


def get_user_by_id(db: Session, user_id: int) -> UserModel | None:
    user = db.query(UserORM).filter(UserORM.id == user_id, UserORM.isDel != 1).first()
    return _to_model(user) if user is not None else None


def get_all_users(db: Session) -> list[UserModel]:
    users = db.query(UserORM).filter(UserORM.isDel != 1).all()
    return [_to_model(user) for user in users]


def update_user(db: Session, id: int, name: str | None = None, age: int | None = None, isDel: int | None = None) -> UserModel:
    user = db.query(UserORM).filter(UserORM.id == id).first()
    if name is not None:
        user.name = name
    if age is not None:
        user.age = age
    if isDel is not None:
        user.isDel = isDel
    db.commit()
    db.refresh(user)
    return _to_model(user)

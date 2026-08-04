from dataclasses import dataclass

from sqlalchemy import Column, Integer, String

from database import Base


@dataclass
class UserModel:
    id: int
    name: str
    age: int
    isDel : int


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    isDel = Column(Integer, nullable=False, default=0)

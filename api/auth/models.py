from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Integer, String, func

from database import Base


@dataclass
class AccountModel:
    id: int
    username: str


class AccountORM(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

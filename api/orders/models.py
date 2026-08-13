from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, func

from database import Base


@dataclass
class OrderModel:
    id: int
    userId: int
    itemType: int # 1: 食品 2: 3C產品 3: 醫療用品 4: 日用品 5: 化學材料
    itemTypeDisplayName: str
    itemName: str
    itemVolume: int
    status: int # 0: 已成立 1: 已確認 2: 揀貨中 3: 出貨中 4: 運送中 5: 已完成 6: 取消 7: 異常
    createdTime: datetime


class OrderORM(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    itemType = Column(Integer, nullable=False)
    itemTypeDisplayName = Column(String(50), nullable=False)
    itemName = Column(String(100), nullable=False)
    itemVolume = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=0)
    createdTime = Column(DateTime, server_default=func.now())

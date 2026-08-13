from sqlalchemy.orm import Session

from api.auth.models import AccountORM
from .models import OrderModel, OrderORM
from .schemas import CreateOrderRequest

ITEM_TYPE_DISPLAY_NAMES = {
    1: "食品",
    2: "3C產品",
    3: "醫療用品",
    4: "日用品",
    5: "化學材料",
}


def _get_item_type_display_name(item_type: int) -> str:
    return ITEM_TYPE_DISPLAY_NAMES.get(item_type, "未知類型")


def _to_model(order: OrderORM) -> OrderModel:
    return OrderModel(
        id=order.id,
        userId=order.userId,
        itemType=order.itemType,
        itemTypeDisplayName=order.itemTypeDisplayName,
        itemName=order.itemName,
        itemVolume=order.itemVolume,
        status=order.status,
        createdTime=order.createdTime,
    )


def create_order(db: Session, orderItem: CreateOrderRequest) -> OrderModel:
    order = OrderORM(
        userId=orderItem.user_id,
        itemType=orderItem.item_type,
        itemTypeDisplayName=_get_item_type_display_name(orderItem.item_type),
        itemName=orderItem.item_name,
        itemVolume=orderItem.item_volume,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return _to_model(order)

def get_user_orders(db: Session, userId: int) -> list[OrderModel]:

    account = db.query(AccountORM).filter(AccountORM.id == userId).first()
    orders = account.orders if account is not None else []

    return [_to_model(order) for order in orders]

def get_user_single_order(db: Session, userId: int, orderId: int) -> OrderModel | None:

    order = db.query(OrderORM).filter(OrderORM.userId == userId, OrderORM.id == orderId).first()

    return _to_model(order) if order is not None else None

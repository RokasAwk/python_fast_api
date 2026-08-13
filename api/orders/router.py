from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from api.auth.dependencies import get_current_account
from api.auth.models import AccountModel
from config import security
from database import get_db
from exceptions import Forbidden
from . import service
from .exceptions import ItemVolumeInValidExists, OrderNotFound
from .schemas import CreateOrderResponse, CreateOrderRequest, GetUserOrdersResponse, GetUserSingleOrderResponse


router = APIRouter(prefix="/order", tags=["Order"], dependencies=[Security(security)])


@router.post(
    "/create",
    response_model=CreateOrderResponse,
    summary="建立訂單",
    description="建立一筆訂單，每筆訂單有獨立的 id 可供查詢。",
)

def createOrder(
    payload: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_account: AccountModel = Depends(get_current_account),
):
    if payload.user_id != current_account.id:
        raise Forbidden("無權為其他使用者建立訂單")

    if payload.item_volume <= 0:
        raise ItemVolumeInValidExists()

    account = service.create_order(db, payload)
    return {
        "message": "Success",
        "order_id": account.id,
        "user_id": account.userId,
        "item_type": account.itemType,
        "item_type_display_name": account.itemTypeDisplayName,
        "item_name": account.itemName,
        "item_volume": account.itemVolume,
        "created_time": int(account.createdTime.timestamp()),
        "status": account.status,
    }

@router.post(
    "/user/{user_id:int}",
    response_model=GetUserOrdersResponse,
    summary="查詢使用者的所有訂單",
    description="利用 user id 查詢該使用者的所有訂單。",
)

def getUserOrders(
    user_id: int,
    db: Session = Depends(get_db),
    current_account: AccountModel = Depends(get_current_account),
):
    if user_id != current_account.id:
        raise Forbidden("無權存取其他使用者的訂單")

    orders = service.get_user_orders(db, user_id)

    return {
        "message": "Success",
        "orders": [
            {
                "order_id": order.id,
                "user_id": order.userId,
                "item_type": order.itemType,
                "item_type_display_name": order.itemTypeDisplayName,
                "item_name": order.itemName,
                "item_volume": order.itemVolume,
                "created_time": int(order.createdTime.timestamp()),
                "status": order.status,
            }
            for order in orders
        ],
    }

@router.post(
    "/{order_id:int}",
    response_model=GetUserSingleOrderResponse,
    summary="查詢單筆訂單",
    description="利用 order id 查詢該筆訂單，並且檢查 order id 是否為使用者本人的訂單。",
)

def getSingleOrder(
    order_id: int,
    db: Session = Depends(get_db),
    current_account: AccountModel = Depends(get_current_account),
):
    order = service.get_user_single_order(db, current_account.id, order_id)
    if order is None:
        raise OrderNotFound()

    return {
        "message": "Success",
        "order": {
            "order_id": order.id,
            "user_id": order.userId,
            "item_type": order.itemType,
            "item_type_display_name": order.itemTypeDisplayName,
            "item_name": order.itemName,
            "item_volume": order.itemVolume,
            "created_time": int(order.createdTime.timestamp()),
            "status": order.status,
        }
    }
from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session

from config import security
from database import get_db
from . import service
from .exceptions import ItemVolumeInValidExists
from .schemas import CreateOrderResponse, CreateOrderRequest


router = APIRouter(prefix="/order", tags=["Order"], dependencies=[Security(security)])


@router.post(
    "/create",
    response_model=CreateOrderResponse,
    summary="建立訂單",
    description="建立一筆訂單，每筆訂單有獨立的 id 可供查詢。",
)

def createOrder(payload: CreateOrderRequest, db: Session = Depends(get_db)):
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
        "status": account.status,
    }

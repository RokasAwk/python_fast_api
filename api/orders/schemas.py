from pydantic import BaseModel
from .models import OrderModel

class OrderItem(BaseModel):
    order_id: int
    user_id: int
    item_type: int # 1: 食品 2: 3C產品 3: 醫療用品 4: 日用品 5: 化學材料
    item_type_display_name: str
    item_name: str
    item_volume: int
    status: int # 0: 已成立 1: 已確認 2: 揀貨中 3: 出貨中 4: 運送中 5: 已完成 6: 取消 7: 異常

class CreateOrderResponse(BaseModel):
    message: str
    order_id: int
    user_id: int
    item_type: int # 1: 食品 2: 3C產品 3: 醫療用品 4: 日用品 5: 化學材料
    item_type_display_name: str
    item_name: str
    item_volume: int
    status: int # 0: 已成立 1: 已確認 2: 揀貨中 3: 出貨中 4: 運送中 5: 已完成 6: 取消 7: 異常

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Success",
                "order_id": 100001,
                "user_id": 1,
                "item_type": 1,
                "item_type_display_name": "食品",
                "item_name": "泡麵",
                "item_volume": 10,
                "status": 0
            }
        }
    }

class CreateOrderRequest(BaseModel):
    user_id: int
    item_type: int # 1: 食品 2: 3C產品 3: 醫療用品 4: 日用品 5: 化學材料
    item_name: str
    item_volume: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1, 
                "item_type": 1, 
                "item_name": "泡麵",
                "item_volume": 10
            }
        }
    }

class GetUserOrdersResponse(BaseModel):
    message: str
    orders: list[OrderItem]

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Success",
                "orders": [
                    {
                        "order_id": 100001,
                        "user_id": 1,
                        "item_type": 1,
                        "item_type_display_name": "食品",
                        "item_name": "泡麵",
                        "item_volume": 10,
                        "status": 0
                    },
                    {
                        "order_id": 100002,
                        "user_id": 1,
                        "item_type": 1,
                        "item_type_display_name": "食品",
                        "item_name": "餅乾",
                        "item_volume": 5,
                        "status": 0
                    }
                ]
            }
        }
    }

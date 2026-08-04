from pydantic import BaseModel


class HomeResponse(BaseModel):
    message: str

    model_config = {
        "json_schema_extra": {
            "example": {"message": "歡迎使用我的API"}
        }
    }

from fastapi import APIRouter

from .schemas import HomeResponse

router = APIRouter()


@router.get(
    "/",
    response_model=HomeResponse,
    summary="首頁",
    description="API 服務的歡迎訊息，可用來確認服務是否正常運作。",
)
def home():
    return {"message": "歡迎使用我的API"}

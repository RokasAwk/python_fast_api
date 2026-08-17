import asyncio
import logging
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, Query, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from api.auth import service as auth_service
from api.auth.models import AccountModel
from auth import decode_access_token
from database import get_db

router = APIRouter()

# 設定 logger
logger = logging.getLogger("uvicorn")


class ConnectionManager:
    """管理所有已連線的 WebSocket，用於廣播訊息"""

    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


# 背景任務函數
async def run_background_task(task_id: str):
    """執行背景任務：每秒完成 10%，共 10 秒"""
    for progress in range(10, 110, 10):  # 10, 20, 30, ... 100
        await asyncio.sleep(1)  # 等待 1 秒

        # 透過 WebSocket 廣播進度
        message = f"任務 {task_id} 進度: {progress}%"
        await manager.broadcast(message)

        logger.info(message)

    # 任務完成通知
    completion_message = f"任務 {task_id} 已完成！"
    await manager.broadcast(completion_message)
    logger.info(completion_message)


@router.post("/start-task")
async def start_task(background_tasks: BackgroundTasks):
    """啟動背景任務並回傳任務 ID"""
    task_id = "TASK-001"  # 固定任務 ID

    # 使用 FastAPI BackgroundTasks 啟動背景任務
    background_tasks.add_task(run_background_task, task_id)

    current_time = datetime.now().strftime("%H:%M:%S")
    logger.info(f"[{current_time}] 啟動背景任務: {task_id}")

    return {"task_id": task_id, "message": "背景任務已啟動"}



async def get_current_account_ws(
    websocket: WebSocket,
    token: str | None = Query(None),
    db: Session = Depends(get_db),
) -> AccountModel | None:
    if token is None:
        return None

    payload = decode_access_token(token)
    if payload is None:
        return None

    try:
        account_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        return None

    account = auth_service.get_account_by_id(db, account_id)
    if account is None:
        return None

    return AccountModel(id=account.id, username=account.username)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    account: AccountModel | None = Depends(get_current_account_ws),
):
    if account is None:
        # 1008 = Policy Violation，用來表示身份驗證失敗
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)

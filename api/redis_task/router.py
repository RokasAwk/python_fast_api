from fastapi import APIRouter, Security
from config import security
from api.redis_task.tasks import add, app as celery_app

router = APIRouter(prefix="/task", tags=["Task"], dependencies=[Security(security)])


@router.post(
    "/{x}/{y}", 
    summary="建立加法Task",
    description="建立x+y的加法Task。",
    )
def create_task(x: int, y: int):
    task = add.delay(x, y)
    return {"task_id": task.id}


@router.get(
    "/status/{task_id}",
    summary="追蹤加法Task的進度",
    description="追蹤x+y的加法Task進度。",
    )
def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "pending"}
    elif task.state == "SUCCESS":
        return {"status": "completed", "result": task.result}
    else:
        return {"status": "failed", "error": task.info}
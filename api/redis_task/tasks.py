# tasks.py

import time
from celery import Celery
from config import settings

app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url
)

@app.task
def add(x, y):
    print("Starting a long-running task...")
    time.sleep(10)  # 模擬耗時操作（同步阻塞，但只會阻塞這個 worker）
    print("Task completed.")
    return x + y
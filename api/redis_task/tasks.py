# tasks.py

import os
import time
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@app.task
def add(x, y):
    print("Starting a long-running task...")
    time.sleep(10)  # 模擬耗時操作（同步阻塞，但只會阻塞這個 worker）
    print("Task completed.")
    return x + y
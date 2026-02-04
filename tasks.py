from celery import Celery
from crawler_engine import run_crawler_task
import asyncio

celery_app = Celery(
    "spider_tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@celery_app.task
def execute_crawler(url):

    return asyncio.run(run_crawler_task(url))

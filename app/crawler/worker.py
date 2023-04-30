from celery import Celery

from app.core.config import settings

worker = Celery(
    "app.crawler",
    broker=settings.WORKER_BROKER_DSN,
    backend=settings.WORKER_BACKEND_DSN,
)

worker.autodiscover_tasks(
    packages=[
        "app.crawler.schedule_update_feed",
        "app.crawler.update_feed",
        "app.crawler.update_feed_item",
    ]
)

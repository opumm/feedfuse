from celery import Celery

from app.core.config import settings

worker = Celery(
    "app.crawler",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

worker.autodiscover_tasks(
    packages=[
        "app.crawler.schedule_update_feed",
        "app.crawler.update_feed",
        "app.crawler.update_feed_item",
    ]
)

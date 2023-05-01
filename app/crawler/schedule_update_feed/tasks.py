import logging

from asgiref.sync import async_to_sync

from app.core.config import settings
from app.crawler.utils import fetch_feed
from app.crawler.worker import worker


@worker.task(bind=True, name="schedule_update_feed")
def schedule_update_feed(self):
    """Send Task to Update Feed.

    Steps:
        - Get all feeds where update is enabled.
        - Send task to "update_feed" for each of these feeds.

    Retry: No, it waits for the next scheduled run.

    Back-off: No, as it does not have retry.

    Drop: Yes, immediately after first fail.

    """
    try:
        feeds = async_to_sync(fetch_feed)()
        for feed in feeds:
            worker.send_task(
                "update_feed",
                kwargs={
                    "feed_id": feed.id,
                    "url": feed.url,
                    "modified_at": feed.modified_at,
                },
            )
    except Exception as exc:
        logging.error("failed to run schedule_update_feed task: %s", str(exc))


@worker.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Scheduler - Runs periodically to create update feed tasks

    Using Celery beat to create a cron-like job creator
    that creates and push jobs in the broker which is picked
    up by the Feed parser worker.

    """
    interval = settings.WORKER_INTERVAL_SECONDS
    sender.add_periodic_task(
        interval,
        schedule_update_feed.s(),
        name=f"schedule feed updates every {interval} seconds",
    )

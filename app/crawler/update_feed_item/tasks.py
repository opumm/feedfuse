import logging

from asgiref.sync import async_to_sync

from app.core.config import settings
from app.crawler.utils import (
    create_item_in_db,
    get_item_from_db,
    parse_datetime_string,
    update_item_in_db,
)
from app.crawler.worker import worker
from app.schemas.items import CreateItemSchema, UpdateItemSchema


@worker.task(
    bind=True, name="update_feed_item", max_retries=settings.WORKER_MAX_RETRIES
)
def update_feed_item(self, feed_id: int, item: dict):
    """Entry Loader - Insert Feed Entry into the Database.

    Steps:
        - Find feed entry by the ID (from the source).
        - Drop if feed entry exists for the ID of the item.
        - Insert new feed entry.

    Retry: Yes, retry on failure or exception.

    Back-off: Yes, waits for fixed time before retry.

    Drop: Yes, immediately after max retries or already existing feed entries.

    """
    try:
        existing_item = async_to_sync(get_item_from_db)(item["id"])
        if existing_item:
            updated_item = UpdateItemSchema(
                title=item["title"], url=item["link"], description=item["summary"]
            )
            async_to_sync(update_item_in_db)(existing_item.id, updated_item)
            return True
        else:
            new_item = CreateItemSchema(
                title=item["title"],
                url=item["link"],
                guid=item["id"],
                description=item["summary"],
                feed_id=feed_id,
                published_at=parse_datetime_string(item["published"]),
            )
            async_to_sync(create_item_in_db)(new_item)
            return True

    except Exception as exc:
        logging.error("failed to run update_feed_item task: %s", str(exc))
        raise self.retry(exc=exc, countdown=settings.WORKER_RETRY_INTERVAL_SECONDS)

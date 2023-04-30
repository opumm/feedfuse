import logging

import feedparser
from asgiref.sync import async_to_sync
from celery.exceptions import MaxRetriesExceededError
from feedparser import FeedParserDict

from app.core.config import settings
from app.crawler.utils import (
    parse_datetime_string,
    pause_feed_update,
    update_feed_in_db,
)
from app.crawler.worker import worker
from app.schemas.feeds import UpdateFeedSchema


def get_feed_details(url, last_modified=None) -> FeedParserDict | None:
    """
    Fetches a feed and returns the parsed result.

    If the feed has not been modified since the last time it was fetched
    (as indicated by the last_modified argument), the function returns None.
    """
    feed = feedparser.parse(url, modified=last_modified)
    if feed.status == 304:  # Not Modified
        return None

    if feed["bozo"]:
        raise Exception(f"Failed to parse feed from URL {url}")
    else:
        return feed


@worker.task(bind=True, name="update_feed", max_retries=settings.SCRAPPER_MAX_RETRIES)
def update_feed(self, feed_id: int, url: str, modified_at: str):
    """Feed Parser - Update Feed and Send Task to Update Feed Entry.

    Steps:
        - Count if retry attemps. If max retry is reached:
            - Drop message and stop the flow.
            - Disable update for the feed.
        - Get feed information from Database.
        - Parse RSS Feed and items using the URL.
        - Drop message if last built timestamp from RSS feed <= DB value.
        - Update DB value for last built timestamp.
        - Send task to "update_feed_entry" for each of these feed items.

    Retry: Yes, retry on failure or exception.

    Back-off: Yes, waits for fixed time before retry.

    Drop: Yes, immediately after max retries or RSS feed not updated at source.

    """
    try:
        if self.request.retries >= settings.SCRAPPER_MAX_RETRIES:
            raise MaxRetriesExceededError

        remote_feed = get_feed_details(url, modified_at)
        if remote_feed:
            new_feed = UpdateFeedSchema(
                title=remote_feed.feed.title,
                description=remote_feed.feed.description,
                last_built_at=parse_datetime_string(remote_feed.feed.updated),
                modified_at=remote_feed.modified,
            )
            async_to_sync(update_feed_in_db)(feed_id, new_feed)
            for item in remote_feed.entries:
                worker.send_task("update_feed_item", args=[feed_id, item])

    except MaxRetriesExceededError:
        async_to_sync(pause_feed_update)(feed_id)

    except Exception as exc:
        logging.error("failed to run update_feed task: %s", str(exc))
        raise self.retry(exc=exc, countdown=settings.SCRAPPER_RETRY_INTERVAL_SECONDS)

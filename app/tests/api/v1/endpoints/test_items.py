import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.schemas.items import CreateItemSchema, ItemQueryParams
from app.schemas.feeds import CreateFeedSchema
from app import crud


@pytest.mark.asyncio
async def test_get_items(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    # create feed
    url = "https://www.example.com/feed"
    feed_data = CreateFeedSchema(url=url)

    response = await client.post(
        app.url_path_for("create_feed"),
        json=feed_data.dict(),
        headers=default_user_headers,
    )
    assert response.status_code == 201
    response_data = response.json()
    feed_id = response_data["id"]

    new_item = CreateItemSchema(
        title="Dummy Title",
        url="https://www.dummyurl.com/1",
        guid="dummy_guid",
        feed_id=feed_id,
        description="This is a dummy item.",
        published_at="2023-05-01 19:06:27.000000",
    )

    new_item.feed_id = feed_id
    db_item = await crud.items.create_item(session, new_item)

    # get items
    response = await client.get(
        app.url_path_for("get_items"), headers=default_user_headers
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["title"] == new_item.title
    assert response_data[0]["url"] == new_item.url
    assert response_data[0]["guid"] == new_item.guid


@pytest.mark.asyncio
async def test_mark_as_read(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    # create feed
    url = "https://www.example.com/feed"
    feed_data = CreateFeedSchema(url=url)

    response = await client.post(
        app.url_path_for("create_feed"),
        json=feed_data.dict(),
        headers=default_user_headers,
    )
    assert response.status_code == 201
    response_data = response.json()
    feed_id = response_data["id"]

    new_item = CreateItemSchema(
        title="Dummy Title",
        url="https://www.dummyurl.com/1",
        guid="dummy_guid",
        feed_id=feed_id,
        description="This is a dummy item.",
        published_at="2023-05-01 19:06:27.000000",
    )

    new_item.feed_id = feed_id
    db_item = await crud.items.create_item(session, new_item)

    query_unread = "status=unread&sort=updated_at&order=desc"

    # get items
    response = await client.get(
        app.url_path_for("get_items"),
        params=query_unread,
        headers=default_user_headers,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1

    # mark item as read
    response = await client.post(
        app.url_path_for("update_item", item_id=db_item.id),
        params="mark_as_read=true",
        headers=default_user_headers,
    )
    assert response.status_code == 200

    # get items with unread
    response = await client.get(
        app.url_path_for("get_items"),
        params=query_unread,
        headers=default_user_headers,
    )
    assert response.status_code == 404

    # get items with read
    query_unread = "status=read&sort=updated_at&order=desc"
    response = await client.get(
        app.url_path_for("get_items"),
        params=query_unread,
        headers=default_user_headers,
    )
    assert response.status_code == 200
    assert len(response_data) == 1

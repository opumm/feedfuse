import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


from app.main import app
from app.schemas.feeds import CreateFeedSchema
from app import crud

url = "https://www.example.com/feed"
feed = CreateFeedSchema(url=url)


@pytest.mark.asyncio
async def test_create_feed(client: AsyncClient, default_user_headers):
    # create feed
    response = await client.post(
        app.url_path_for("create_feed"), json=feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["url"] == url


@pytest.mark.asyncio
async def test_create_feed_duplicate(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    # Create a feed.
    response = await client.post(
        app.url_path_for("create_feed"), json=feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201

    # Try to create the same feed again.
    response = await client.post(
        app.url_path_for("create_feed"), json=feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201
    content = response.json()
    assert content["url"] == url

    # Check that the feed is still added to the database only once.
    feeds = await crud.feeds.get_feeds(session)
    assert len(feeds) == 1


@pytest.mark.asyncio
async def test_get_feeds(client: AsyncClient, default_user_headers):
    # create feed
    response = await client.post(
        app.url_path_for("create_feed"), json=feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201

    # get feeds
    response = await client.get(
        app.url_path_for("get_feeds"), headers=default_user_headers
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]["url"] == url


@pytest.mark.asyncio
async def test_get_feed_by_id(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    # create feed
    response = await client.post(
        app.url_path_for("create_feed"), json=feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201
    response_data = response.json()
    feed_id = response_data["id"]

    # get feed by id
    response = await client.get(
        app.url_path_for("get_feed_by_id", feed_id=feed_id),
        headers=default_user_headers,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["url"] == url


@pytest.mark.asyncio
async def test_unsubscribe_feeds(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    # Create a feed.
    response = await client.post(
        app.url_path_for("create_feed"), json=feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201
    response_data = response.json()
    feed_id = response_data["id"]

    # get feeds
    response = await client.get(
        app.url_path_for("get_feeds"), headers=default_user_headers
    )
    assert response.status_code == 200

    # Check that we are getting only subscribed feed.
    response_data = response.json()
    assert len(response_data) == 1

    # Unsubscribe feed
    response = await client.delete(
        app.url_path_for("unsubscribe_feed", feed_id=feed_id),
        headers=default_user_headers,
    )
    assert response.status_code == 204

    # get feeds again
    response = await client.get(
        app.url_path_for("get_feeds"), headers=default_user_headers
    )
    assert response.status_code == 200

    # Check that we are getting only subscribed feed.
    response_data = response.json()
    assert len(response_data) == 0


@pytest.mark.asyncio
async def test_get_subscribed_feeds(
    client: AsyncClient, default_user_headers, session: AsyncSession
):
    # Create a feed.
    url_1 = "https://www.example.com/feed_1"
    _feed = CreateFeedSchema(url=url_1)
    response = await client.post(
        app.url_path_for("create_feed"), json=_feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201

    # Create a feed.
    url_2 = "https://www.example.com/feed_2"
    _feed = CreateFeedSchema(url=url_2)
    response = await client.post(
        app.url_path_for("create_feed"), json=_feed.dict(), headers=default_user_headers
    )
    assert response.status_code == 201
    response_data = response.json()
    feed_id = response_data["id"]

    # get feeds
    response = await client.get(
        app.url_path_for("get_feeds"), headers=default_user_headers
    )
    assert response.status_code == 200

    # Check that we are getting only subscribed feed.
    response_data = response.json()
    assert len(response_data) == 2

    # Unsubscribe feed
    response = await client.delete(
        app.url_path_for("unsubscribe_feed", feed_id=feed_id),
        headers=default_user_headers,
    )
    assert response.status_code == 204

    # get feeds again
    response = await client.get(
        app.url_path_for("get_feeds"), headers=default_user_headers
    )
    assert response.status_code == 200

    # Check that we are getting only subscribed feed.
    response_data = response.json()
    assert len(response_data) == 1

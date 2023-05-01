import asyncio
from collections.abc import AsyncGenerator
from datetime import timedelta

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.security import create_access_token
from app.main import app
from app.db.base_class import Base
from app.models.users import User

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

POSTGRES_IMAGE = "postgres:15"
POSTGRES_CONTAINER_PORT = 5432

default_user_id = 1234
default_user_email = "test_user@ff.com"
default_user_password = "p@ssword"
access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
default_user_access_token = create_access_token(
    default_user_id, expires_delta=access_token_expires
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_db_setup_sessionmaker():
    # always drop and create test db tables between tests session
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture(autouse=True)
async def session(test_db_setup_sessionmaker) -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

        # delete all data from all tables after test
        for name, table in Base.metadata.tables.items():
            await session.execute(delete(table))
        await session.commit()


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        client.headers.update({"Host": "localhost"})
        yield client


@pytest_asyncio.fixture
async def default_user(test_db_setup_sessionmaker) -> User:
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.email == default_user_email)
        )
        user = result.scalars().first()
        if user is None:
            new_user = User(
                email=default_user_email,
                password=default_user_password,
            )
            new_user.id = default_user_id
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        return user


@pytest.fixture
def default_user_headers(default_user: User):
    return {"Authorization": f"Bearer {default_user_access_token}"}

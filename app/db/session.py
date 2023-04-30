from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def async_session_generator():
    engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session


async def get_async_session():
    async_session = async_session_generator()
    async with async_session() as session:
        yield session


@asynccontextmanager
async def get_session():
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

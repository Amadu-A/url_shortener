from httpx import AsyncClient, ASGITransport
from src.database.models import Base
from src.main import app, get_session

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession


import pytest


engine = create_async_engine(
    url="sqlite+aiosqlite:///.test.db"
)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():
    async with new_session() as session:
        yield session


@pytest.fixture(scope="session")
def session_factory():
    return new_session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

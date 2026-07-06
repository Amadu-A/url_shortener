import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    url=os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5433/url_shortener_db",
    ),
    pool_size=20,
    max_overflow=30,
)

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)



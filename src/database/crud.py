from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ShortURL
from src.exceptions import SlugAlreadyExistsError


async def add_slug_to_db(
    slug: str,
    long_url: str,
    session: AsyncSession,
):
    new_slug = ShortURL(
        slug=slug,
        long_url=long_url,
    )
    session.add(new_slug)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise SlugAlreadyExistsError(
            f"The slug '{slug}' already exists in the database."
        )


async def get_long_url_by_slug(slug: str, session: AsyncSession) -> str | None:
    query = select(ShortURL).filter_by(slug=slug)
    result = await session.execute(query)
    new_slug = result.scalar_one_or_none()
    return new_slug.long_url if new_slug else None


async def increment_clicks(slug: str, session: AsyncSession) -> None:
    """Атомарные инкремент кликов, чтобы не терять клики при параллельных запросах"""
    query = (
        update(ShortURL)
        .where(ShortURL.slug == slug)
        .values(clicks=ShortURL.clicks + 1)
    )
    await session.execute(query)
    await session.commit()


async def get_clicks_by_slug(slug: str, session: AsyncSession) -> int | None:
    query = select(ShortURL).filter_by(slug=slug)
    result = await session.execute(query)
    short_url = result.scalar_one_or_none()
    return short_url.clicks if short_url else None

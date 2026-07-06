from sqlalchemy.ext.asyncio import AsyncSession

from src.shortener import generate_random_string
from src.database.crud import add_slug_to_db, get_long_url_by_slug
from src.exceptions import NoLongUrlProvidedError, SlugAlreadyExistsError


async def generate_short_url(
    long_url: str,
    session: AsyncSession,
) -> str:
    async def _generate_slug_and_add_to_db() -> str:
        slug = generate_random_string()
        await add_slug_to_db(slug, long_url, session)
        return slug

    for _ in range(5):  # Try up to 5 times to generate a unique slug
        try:
            return await _generate_slug_and_add_to_db()
        except SlugAlreadyExistsError as ex:
            if _ == 4:  # If it's the last attempt, raise the error
                raise SlugAlreadyExistsError("Failed to generate a unique slug after 5 attempts.") from ex
    raise SlugAlreadyExistsError("Failed to generate a unique slug after 5 attempts.")


async def get_url_by_slug(slug: str, session: AsyncSession) -> str | None:
    long_url = await get_long_url_by_slug(slug, session)
    if not long_url:
        raise NoLongUrlProvidedError("No long URL found for the provided slug.")
    return long_url
